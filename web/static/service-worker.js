const CACHE_NAME = 'codexrpg-v1';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/game.js',
  '/index.html'
];

// Install Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Activate Service Worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Strategy: Network First, fallback to Cache
self.addEventListener('fetch', event => {
  const { request } = event;

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // API calls: Always try network
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Update cache
          const cache = caches.open(CACHE_NAME);
          cache.then(c => c.put(request, response.clone()));
          return response;
        })
        .catch(() => {
          // Fallback to cache for offline
          return caches.match(request) || new Response('Offline - please connect to internet');
        })
    );
    return;
  }

  // Static assets: Cache first
  event.respondWith(
    caches.match(request).then(response => {
      if (response) return response;

      return fetch(request).then(response => {
        if (!response || response.status !== 200) return response;

        const cache = caches.open(CACHE_NAME);
        cache.then(c => c.put(request, response.clone()));
        return response;
      });
    })
  );
});

// Periodic sync for background updates (when online)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-game-state') {
    event.waitUntil(
      fetch('/api/player/info')
        .then(response => response.json())
        .then(data => {
          // Game state will be synced
          return Promise.resolve();
        })
    );
  }
});
