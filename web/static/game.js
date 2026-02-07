const API_URL = 'http://localhost:5000/api';

let gameActive = false;
let currentPlayer = null;

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
        
        const mapContainer = document.getElementById('world-map');
        mapContainer.innerHTML = '';
        
        // Biome emoji mapping
        const biomeEmoji = {
            'plains': '🟩',
            'forest': '🟢',
            'mountain': '⛰️',
            'lake': '🌊'
        };
        
        world.grid.forEach(row => {
            row.forEach(biome => {
                const cell = document.createElement('div');
                cell.className = `map-cell biome-${biome}`;
                cell.textContent = biomeEmoji[biome] || '?';
                mapContainer.appendChild(cell);
            });
        });
    } catch (error) {
        console.error('Error loading world:', error);
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
