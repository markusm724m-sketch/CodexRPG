# CodexRPG
Fantasy Isekai RPG Sandbox Game

## 🚀 Quick Start

### Option 1: Web Interface (PC & Mobile) ⭐

**Play on PC:**
```bash
pip install -r requirements.txt
cd web && python app.py
# Open: http://localhost:5000
```

**Play on Mobile:**
1. Find your PC IP (Windows: `ipconfig` / Mac/Linux: `ifconfig`)
2. On phone: Open `http://192.168.x.x:5000` in Chrome/Safari
3. Tap menu → "Install app" 
4. Works offline! ✓

**Build Native APK:**
See [MOBILE.md](MOBILE.md) for Android APK guide

### Option 2: CLI Commands

```bash
export PYTHONPATH=src  # Linux/Mac
python -m codexrpg.cli create-player "Hero" --class warrior
python -m codexrpg.cli npcs
python -m codexrpg.cli gen-world --width 10 --height 10
```

## 📁 Project Structure

```
src/codexrpg/          - Core game engine
├── game.py            - Game loop
├── player.py          - Player system
├── world.py           - World generation
├── character_class.py - Classes & abilities
├── skills.py          - Skill system
├── item.py            - Inventory items
├── npc.py             - NPCs & dialogue
├── quest.py           - Quest system
├── crafting.py        - Crafting & gathering
├── reputation.py      - Faction reputation
├── events.py          - Random world events
├── homestead.py       - Player housing
└── systems/           - Combat & inventory

web/                   - Flask web interface
├── app.py             - REST API
├── templates/         - HTML pages
└── static/            - CSS & JavaScript

tests/                 - Unit tests (23 tests)
```

## 🎮 Features

### Core Systems
- **4 Character Classes**: Warrior, Mage, Rogue, Paladin
- **Unique Skills**: Each class has starting abilities
- **Combat System**: Damage, defense, HP management
- **Inventory System**: Collect and manage items

### Sandbox Features ⭐
- **Dynamic Quests**: Tasks from NPCs with rewards
- **NPC System**: 4 types - merchants, blacksmiths, alchemists, villagers
- **Crafting**: Learn recipes and craft items from ingredients
- **Resource Gathering**: Collect herbs, ore, and more
- **Faction Reputation**: Build bonds with 4 factions
- **World Events**: Treasure finds, bandits, festivals!
- **Player Homesteads**: Own houses, upgrade them, store items
- **Trading**: Buy and sell with NPCs
- **World Map**: 10x10 procedurally generated biomes

## 🧪 Testing

```bash
export PYTHONPATH=src
pytest -v
```

✅ **Result: 23/23 tests pass**

## 📖 Documentation

- `SETUP.md` - Detailed installation guide
- `MOBILE.md` - Mobile & APK build guide ⭐
- `docs/CONTRIBUTING.md` - How to contribute
- `docs/ROADMAP.md` - Development plans

## 🎨 Technology Stack

- **Backend**: Python 3.10+, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Mobile**: Progressive Web App (PWA) - Offline support
- **APK**: Kivy, Buildozer (optional)
- **Database**: In-memory (session-based)
- **Testing**: pytest

## 📱 Multi-Platform Support

| Platform | Support | Status |
|----------|---------|--------|
| **Windows PC** | Direct | ✅ Working |
| **Mac/Linux PC** | Direct | ✅ Working |
| **Android Browser** | PWA | ✅ Working |
| **iOS Safari** | PWA | ✅ Working |
| **Android APK** | Native app | 📖 Guide available |

**PWA Features (Progressive Web App):**
- ✅ Install to home screen
- ✅ Works offline
- ✅ Fast loading
- ✅ No app store needed

## 🌟 Game Systems

### Player Stats
- HP (scales by class)
- Damage (scales by class) 
- Defense (scales by class)
- Gold (currency)
- Experience (todo)

### Classes
| Class | HP | DMG | DEF | Theme |
|-------|----|----|-----|--------|
| Warrior | 120 | 15 | 10 | Melee fighter |
| Mage | 70 | 8 | 3 | Spellcaster |
| Rogue | 85 | 12 | 6 | Quick striker |
| Paladin | 110 | 13 | 12 | Holy warrior |

### NPCs (4 types)
- Merchants: Buy/sell items
- Blacksmiths: Forge weapons
- Alchemists: Sell potions
- Villagers: Give quests

### Factions (Reputation)
- Merchants Guild
- Blacksmith Union
- Nature Druids
- Royal Guard

## 💡 How to Play

1. **Create a Character**: Choose a name and class
2. **Explore the World**: View the map and NPCs
3. **Gather Resources**: Collect items and gold
4. **Complete Quests**: Get rewards from NPCs
5. **Craft Items**: Combine resources into new items
6. **Build Reputation**: Increase standing with factions
7. **Manage Your Home**: Store items and residents
8. **Trigger Events**: Random world encounters

## 🚀 Performance

- Fast load times (< 1 second)
- Lightweight dependencies (Flask only)
- 1635 lines of core code
- 23 comprehensive unit tests
- Web interface runs on localhost:5000

## 📝 License

See LICENSE file.

## 🎯 Future Plans

- Multiplayer support
- Database persistence
- More NPCs and quests
- Advanced graphics (Pygame)
- Mobile app
- Sound and music
