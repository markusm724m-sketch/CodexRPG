// Use current origin so PWA/mobile installs and remote hosts work.
// Falls back to localhost:5000 for legacy dev setups.
const API_URL = (typeof window !== 'undefined' && window.location && window.location.origin
    ? window.location.origin
    : 'http://localhost:5000') + '/api';

let gameActive = false;
let currentPlayer = null;
let canvas, ctx, tileSize = 60, worldGrid = null, animFrame = null;

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

    // Start animation loop
    if (!animFrame) animFrame = requestAnimationFrame(animateCanvas);
}

function drawWorldCanvas() {
    if (!ctx || !worldGrid) return;
    const rows = worldGrid.length;
    const cols = worldGrid[0].length;

    // clear
    ctx.clearRect(0,0,canvas.width,canvas.height);

    for (let r=0; r<rows; r++) {
        for (let c=0; c<cols; c++) {
            const biome = worldGrid[r][c];
            const x = c * tileSize;
            const y = r * tileSize;
            drawTile(biome, x, y, tileSize);
        }
    }

    // draw player sprite roughly at center for demo
    drawPlayerSprite(Math.floor(cols/2), Math.floor(rows/2));
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
    const x = col * tileSize + tileSize/2;
    const y = row * tileSize + tileSize/2;

    // simple circle player
    ctx.beginPath();
    ctx.fillStyle = '#ffcc00';
    ctx.arc(x, y, tileSize*0.28, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle = '#8b5a00'; ctx.stroke();
}

function animateCanvas() {
    drawWorldCanvas();
    animFrame = requestAnimationFrame(animateCanvas);
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
