// Use current origin so PWA/mobile installs and remote hosts work.
// Falls back to localhost:5000 for legacy dev setups.
const API_URL = (typeof window !== 'undefined' && window.location && window.location.origin
    ? window.location.origin
    : 'http://localhost:5000') + '/api';

let gameActive = false;
let currentPlayer = null;
let canvas, ctx, tileSize = 60, worldGrid = null, animFrame = null;
// Camera and player movement
let camera = { x: 0, y: 0 };
let playerWorldPos = { x: 0, y: 0 }; // in tile coords (float)
let playerTarget = null;
let npcs = [];
// Particles
let particles = [];
// Audio
let audioCtx = null;

// Sprite & animation
let playerSprite = null;
let npcSprite = null;
let spritesLoaded = false;
let playerAnim = { counter: 0, speed: 8, frames: 4 };
let npcAnim = { counter: 0, speed: 12, frames: 4 };
// Audio buffers
let audioBuffers = {};

// On page load
document.addEventListener('DOMContentLoaded', () => {
    loadClasses();
    
    // Change class info on select
    document.getElementById('player-class').addEventListener('change', (e) => {
        updateClassInfo(e.target.value);
    });
    
    // Trigger class info on load
    updateClassInfo('warrior');
});

// Update class info when selected
async function updateClassInfo(classId) {
    try {
        const response = await fetch(`${API_URL}/classes`);
        const data = await response.json();
        const selectedClass = data.classes.find(c => c.id === classId);
        
        if (selectedClass) {
            const info = `
                <strong>${selectedClass.name}</strong><br>
                HP: ${selectedClass.hp} | DMG: ${selectedClass.damage} | DEF: ${selectedClass.defense}<br>
                Skills: ${selectedClass.skills.join(', ')}
            `;
            document.getElementById('class-info').innerHTML = info;
        }
    } catch (error) {
        console.error('Error loading class info:', error);
    }
}

// Load classes
async function loadClasses() {
    try {
        const response = await fetch(`${API_URL}/classes`);
        const data = await response.json();
        // Pre-loaded in HTML
    } catch (error) {
        console.error('Error loading classes:', error);
    }
}

// Create player
async function createPlayer() {
    const name = document.getElementById('player-name').value || 'Adventurer';
    const classId = document.getElementById('player-class').value || 'warrior';
    
    try {
        const response = await fetch(`${API_URL}/player/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, class: classId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentPlayer = data.player;
            gameActive = true;
            
            // Switch to game screen
            document.getElementById('screen-creation').classList.remove('active');
            document.getElementById('screen-game').classList.add('active');
            
            // Update UI
            updatePlayerUI();
            loadNPCs();
            loadQuests();
            loadWorld();
            updateReputation();
            loadHomestead();
        }
    } catch (error) {
        alert('Error creating player: ' + error.message);
    }
}

// Update player UI
async function updatePlayerUI() {
    try {
        const response = await fetch(`${API_URL}/player/info`);
        const player = await response.json();
        currentPlayer = player;
        
        // Update display
        document.getElementById('player-name-display').textContent = player.name;
        document.getElementById('player-class-display').textContent = player.class;
        document.getElementById('hp-value').textContent = `${player.hp}/${player.max_hp}`;
        document.getElementById('hp-bar').style.width = `${(player.hp / player.max_hp) * 100}%`;
        document.getElementById('gold-value').textContent = player.gold;
        document.getElementById('damage-value').textContent = player.damage;
        document.getElementById('defense-value').textContent = player.defense;
        document.getElementById('inventory-count').textContent = `Items: ${player.inventory_size}`;
        
        // Update skills
        const skillsList = document.getElementById('skills-list');
        skillsList.innerHTML = player.skills.map(skill => 
            `<div class="skill-item">⚔ ${skill}</div>`
        ).join('');
    } catch (error) {
        console.error('Error updating player UI:', error);
    }
}

// Player action
async function playerAction(action) {
    try {
        const response = await fetch(`${API_URL}/player/action`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show result
            const resultBox = document.getElementById('action-result');
            resultBox.innerHTML = `✓ ${data.message}`;
            resultBox.style.display = 'block';
            setTimeout(() => { resultBox.style.display = 'none'; }, 3000);
            
            // Update UI
            updatePlayerUI();
            
            // Log event if trigger_event
            if (action === 'trigger_event' && data.event) {
                addEventToLog(data.event);
            }
        }
    } catch (error) {
        console.error('Error performing action:', error);
    }
}

// Switch tab
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const tabContent = document.getElementById(`tab-${tabName}`);
    if (tabContent) {
        tabContent.classList.add('active');
    }
    
    // Mark button as active
    event.target.classList.add('active');
}

// Load world
async function loadWorld() {
    try {
        const response = await fetch(`${API_URL}/world/info`);
        const world = await response.json();

        // initialize canvas on first load
        worldGrid = world.grid;
        initWorldCanvas();
        drawWorldCanvas();
    } catch (error) {
        console.error('Error loading world:', error);
    }
}

function initWorldCanvas() {
    canvas = document.getElementById('world-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    // compute tile size based on canvas size and grid
    const rows = worldGrid.length;
    const cols = worldGrid[0].length;
    const size = Math.min(Math.floor(canvas.width / cols), Math.floor(canvas.height / rows));
    tileSize = size;

    // text style for NPC labels
    ctx.font = '12px sans-serif';

    // Start animation loop
    if (!animFrame) animFrame = requestAnimationFrame(animateCanvas);

    // Attach input handlers
    canvas.addEventListener('click', onCanvasClick);
    window.addEventListener('keydown', onKeyDown);

    // initialize player world pos at center
    playerWorldPos.x = Math.floor(worldGrid[0].length / 2);
    playerWorldPos.y = Math.floor(worldGrid.length / 2);

    // center camera on player
    camera.x = playerWorldPos.x * tileSize - canvas.width/2 + tileSize/2;
    camera.y = playerWorldPos.y * tileSize - canvas.height/2 + tileSize/2;

    // Setup audio context lazily (user gesture may be required on mobile)
    try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { audioCtx = null; }

    // load sprite and audio assets (non-blocking)
    loadAssets();
}

function drawWorldCanvas() {
    if (!ctx || !worldGrid) return;
    const rows = worldGrid.length;
    const cols = worldGrid[0].length;

    // clear
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // draw tiles relative to camera
    for (let r=0; r<rows; r++) {
        for (let c=0; c<cols; c++) {
            const biome = worldGrid[r][c];
            const x = c * tileSize - camera.x;
            const y = r * tileSize - camera.y;
            drawTile(biome, x, y, tileSize);
        }
    }

    // draw NPCs
    drawNPCs();

    // draw particles
    drawParticles();

    // draw player at world position
    drawPlayerSprite(playerWorldPos.x, playerWorldPos.y);
}

function drawTile(biome, x, y, size) {
    // Simple stylized tiles
    switch (biome) {
        case 'forest':
            ctx.fillStyle = '#0b6623';
            ctx.fillRect(x, y, size, size);
            // trees
            ctx.fillStyle = '#0a3';
            ctx.beginPath(); ctx.moveTo(x+size/2, y+6); ctx.lineTo(x+6, y+size-6); ctx.lineTo(x+size-6, y+size-6); ctx.fill();
            break;
        case 'mountain':
            ctx.fillStyle = '#4b5563'; ctx.fillRect(x,y,size,size);
            ctx.fillStyle = '#9aa4ad'; ctx.beginPath(); ctx.moveTo(x+6,y+size-6); ctx.lineTo(x+size/2,y+8); ctx.lineTo(x+size-6,y+size-6); ctx.fill();
            break;
        case 'lake':
            ctx.fillStyle = '#083d77'; ctx.fillRect(x,y,size,size);
            ctx.fillStyle = '#1e90ff'; ctx.fillRect(x+4,y+4,size-8,size-8);
            break;
        default:
            // plains
            ctx.fillStyle = '#6aa84f'; ctx.fillRect(x,y,size,size);
            break;
    }
    // tile border
    ctx.strokeStyle = 'rgba(0,0,0,0.2)'; ctx.strokeRect(x+0.5,y+0.5,size-1,size-1);
}

function drawPlayerSprite(col, row) {
    if (!ctx) return;
    const centerX = col * tileSize + tileSize/2 - camera.x;
    const centerY = row * tileSize + tileSize/2 - camera.y;

    // if sprite loaded, draw animated frame
    if (playerSprite && playerSprite.complete && playerSprite.naturalWidth) {
        playerAnim.counter++;
        const frame = Math.floor(playerAnim.counter / playerAnim.speed) % playerAnim.frames;
        const frameW = playerSprite.naturalWidth / playerAnim.frames;
        const frameH = playerSprite.naturalHeight;
        const sx = frame * frameW;
        const sy = 0;
        const dw = tileSize * 0.9;
        const dh = tileSize * 0.9;
        ctx.drawImage(playerSprite, sx, sy, frameW, frameH, centerX - dw/2, centerY - dh/2, dw, dh);
        return;
    }

    // fallback: simple circle player
    const x = centerX;
    const y = centerY;
    ctx.beginPath();
    ctx.fillStyle = '#ffcc00';
    ctx.arc(x, y, tileSize*0.28, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle = '#8b5a00'; ctx.stroke();
}

function animateCanvas() {
    updateSimulation();
    drawWorldCanvas();
    animFrame = requestAnimationFrame(animateCanvas);
}

function updateSimulation() {
    // Move player towards target if any
    if (playerTarget) {
        const dx = playerTarget.x - playerWorldPos.x;
        const dy = playerTarget.y - playerWorldPos.y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        const speed = 0.08; // tiles per frame
        if (dist < 0.05) {
            playerWorldPos.x = playerTarget.x;
            playerWorldPos.y = playerTarget.y;
            playerTarget = null;
            spawnParticles(playerWorldPos.x, playerWorldPos.y, 8);
        } else {
            playerWorldPos.x += (dx/dist) * speed;
            playerWorldPos.y += (dy/dist) * speed;
        }
    }

    // update camera to follow player smoothly
    const targetCamX = playerWorldPos.x * tileSize - canvas.width/2 + tileSize/2;
    const targetCamY = playerWorldPos.y * tileSize - canvas.height/2 + tileSize/2;
    camera.x += (targetCamX - camera.x) * 0.12;
    camera.y += (targetCamY - camera.y) * 0.12;

    // update particles
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy; p.life -= 1;
        p.vy += 0.04; // gravity
        if (p.life <= 0) particles.splice(i,1);
    }
}

function onCanvasClick(ev) {
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const cx = ev.clientX - rect.left;
    const cy = ev.clientY - rect.top;

    // convert to world tile coords
    const worldX = (cx + camera.x) / tileSize;
    const worldY = (cy + camera.y) / tileSize;
    playerTarget = { x: Math.floor(worldX + 0.5), y: Math.floor(worldY + 0.5) };

    // play click sound and spawn small feedback particles
    playClickSound();
    spawnParticles(worldX, worldY, 6);
}

function onKeyDown(ev) {
    if (!gameActive) return;
    // simple WASD movement
    const key = ev.key.toLowerCase();
    let nx = Math.round(playerWorldPos.x);
    let ny = Math.round(playerWorldPos.y);
    if (key === 'w' || key === 'arrowup') ny -= 1;
    if (key === 's' || key === 'arrowdown') ny += 1;
    if (key === 'a' || key === 'arrowleft') nx -= 1;
    if (key === 'd' || key === 'arrowright') nx += 1;
    if (nx !== Math.round(playerWorldPos.x) || ny !== Math.round(playerWorldPos.y)) {
        // clamp
        nx = Math.max(0, Math.min(worldGrid[0].length-1, nx));
        ny = Math.max(0, Math.min(worldGrid.length-1, ny));
        playerTarget = { x: nx, y: ny };
    }
}

function spawnParticles(tileX, tileY, count) {
    for (let i=0;i<count;i++) {
        const angle = Math.random()*Math.PI*2;
        const speed = Math.random()*1.8 + 0.4;
        particles.push({
            x: tileX * tileSize + tileSize/2,
            y: tileY * tileSize + tileSize/2,
            vx: Math.cos(angle)*speed*0.4,
            vy: Math.sin(angle)*speed*0.4 - 1.0,
            life: 30 + Math.floor(Math.random()*20),
            color: ['#ffd54f','#ff8a65','#a7ffeb'][Math.floor(Math.random()*3)]
        });
    }
}

function drawParticles() {
    if (!ctx) return;
    particles.forEach(p => {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.life/50);
        ctx.beginPath();
        ctx.arc(p.x - camera.x, p.y - camera.y, 3, 0, Math.PI*2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
    });
}

function drawNPCs() {
    if (!ctx || !npcs) return;
    npcs.forEach(npc => {
        const centerX = npc.x * tileSize + tileSize/2 - camera.x;
        const centerY = npc.y * tileSize + tileSize/2 - camera.y;
        if (npcSprite && npcSprite.complete && npcSprite.naturalWidth) {
            npcAnim.counter++;
            const frame = Math.floor(npcAnim.counter / npcAnim.speed) % npcAnim.frames;
            const frameW = npcSprite.naturalWidth / npcAnim.frames;
            const frameH = npcSprite.naturalHeight;
            const sx = frame * frameW;
            const dw = tileSize * 0.8;
            const dh = tileSize * 0.8;
            ctx.drawImage(npcSprite, sx, 0, frameW, frameH, centerX - dw/2, centerY - dh/2, dw, dh);
            return;
        }
        // simple NPC square fallback
        const x = centerX;
        const y = centerY;
        ctx.fillStyle = '#d1c4e9';
        ctx.fillRect(x-12, y-12, 24, 24);
        ctx.fillStyle = '#3e2723';
        ctx.fillText(npc.name[0] || 'N', x-4, y+6);
    });
}

function playClickSound() {
    // ensure audio context exists
    if (!audioCtx) {
        try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { audioCtx = null; }
    }
    if (!audioCtx) return;

    // if buffer loaded, play it
    if (audioBuffers.click) {
        const src = audioCtx.createBufferSource();
        src.buffer = audioBuffers.click;
        const g = audioCtx.createGain(); g.gain.value = 0.12;
        src.connect(g); g.connect(audioCtx.destination);
        src.start();
        return;
    }

    // fallback to simple oscillator
    const o = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(800, audioCtx.currentTime);
    g.gain.setValueAtTime(0.08, audioCtx.currentTime);
    o.connect(g); g.connect(audioCtx.destination);
    o.start(); o.stop(audioCtx.currentTime + 0.08);
}

async function loadAssets() {
    // load player/npc sprite sheets if present
    try {
        playerSprite = new Image();
        playerSprite.src = '/static/sprites/player.png';
        npcSprite = new Image();
        npcSprite.src = '/static/sprites/npc.png';
        // try load audio click
        if (audioCtx) {
            try {
                const resp = await fetch('/static/sfx/click.wav');
                if (resp.ok) {
                    const arr = await resp.arrayBuffer();
                    audioBuffers.click = await audioCtx.decodeAudioData(arr.slice(0));
                }
            } catch (e) {
                console.debug('No click.wav available or failed decode', e);
            }
        }
    } catch (e) {
        console.warn('Asset loading failed or files missing', e);
    } finally {
        // set a short timeout to mark spritesLoaded when images have at least started
        setTimeout(() => { spritesLoaded = true; }, 200);
    }
}

// Load NPCs
async function loadNPCs() {
    try {
        const response = await fetch(`${API_URL}/npcs`);
        const data = await response.json();
        
        const npcsList = document.getElementById('npcs-list');
        npcsList.innerHTML = '';
        
        data.npcs.forEach(npc => {
            const npcCard = document.createElement('div');
            npcCard.className = 'npc-card';
            npcCard.innerHTML = `
                <div class="npc-name">${npc.name}</div>
                <div class="npc-role">${npc.role.toUpperCase()}</div>
                <div class="npc-dialogue">"${npc.dialogue}"</div>
            `;
            npcsList.appendChild(npcCard);
        });
        // populate in-world NPCs with positions (near center)
        npcs = data.npcs.map((n, idx) => ({
            id: n.id || idx,
            name: n.name,
            role: n.role,
            x: Math.floor(worldGrid[0].length/2 + (idx%3) - 1),
            y: Math.floor(worldGrid.length/2 + Math.floor(idx/3) - 1)
        }));
    } catch (error) {
        console.error('Error loading NPCs:', error);
    }
}

// Load quests
async function loadQuests() {
    try {
        const response = await fetch(`${API_URL}/quests`);
        const data = await response.json();
        
        const questsList = document.getElementById('quests-list');
        questsList.innerHTML = '';
        
        data.quests.forEach(quest => {
            const questCard = document.createElement('div');
            questCard.className = 'quest-card';
            questCard.innerHTML = `
                <div class="quest-title">${quest.title}</div>
                <div class="quest-reward">💰 Reward: ${quest.reward} gold</div>
            `;
            questsList.appendChild(questCard);
        });
    } catch (error) {
        console.error('Error loading quests:', error);
    }
}

// Update reputation
async function updateReputation() {
    try {
        const response = await fetch(`${API_URL}/reputation`);
        const data = await response.json();
        
        const repList = document.getElementById('reputation-list');
        repList.innerHTML = '';
        
        Object.entries(data.reputation).forEach(([faction, info]) => {
            const item = document.createElement('div');
            item.className = 'faction-item';
            const factionName = faction.replace(/_/g, ' ').toUpperCase();
            item.innerHTML = `
                <span class="faction-name">${factionName}</span>
                <span class="faction-status">${info.status}</span>
            `;
            repList.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading reputation:', error);
    }
}

// Load homestead
async function loadHomestead() {
    try {
        const response = await fetch(`${API_URL}/homestead`);
        const home = await response.json();
        
        const homeInfo = document.getElementById('home-info');
        homeInfo.innerHTML = `
            <div class="home-details">
                <div class="detail-row">
                    <span class="detail-label">Name:</span>
                    <span class="detail-value">${home.name}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Type:</span>
                    <span class="detail-value">${home.type}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Level:</span>
                    <span class="detail-value">${home.level}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Location:</span>
                    <span class="detail-value">${home.location}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Storage Items:</span>
                    <span class="detail-value">${home.storage_items}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Residents:</span>
                    <span class="detail-value">${home.residents}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Stored Gold:</span>
                    <span class="detail-value">${home.gold}</span>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading homestead:', error);
    }
}

// Add event to log
function addEventToLog(event) {
    const eventsList = document.getElementById('events-log');
    const eventItem = document.createElement('div');
    eventItem.className = 'event-item';
    eventItem.textContent = `${event.title} (+${event.reward} gold)`;
    eventsList.insertBefore(eventItem, eventsList.firstChild);
    
    // Keep only last 5 events
    while (eventsList.children.length > 5) {
        eventsList.removeChild(eventsList.lastChild);
    }
}

// Reset game
function resetGame() {
    if (confirm('Create a new character? (Current progress will be lost)')) {
        gameActive = false;
        currentPlayer = null;
        
        // Reset form
        document.getElementById('player-name').value = 'Adventurer';
        document.getElementById('player-class').value = 'warrior';
        
        // Switch to creation screen
        document.getElementById('screen-game').classList.remove('active');
        document.getElementById('screen-creation').classList.add('active');
        
        updateClassInfo('warrior');
    }
}

// Periodically update player info
setInterval(() => {
    if (gameActive) {
        updatePlayerUI();
    }
}, 5000);
