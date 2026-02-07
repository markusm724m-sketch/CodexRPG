# CodexRPG Setup & Installation Guide

## System Requirements

- **Python**: 3.10 or higher
- **OS**: Linux, macOS, or Windows
- **RAM**: 50MB minimum
- **Disk**: 20MB

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/markusm724m-sketch/CodexRPG.git
cd CodexRPG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask - Web server
- Flask-CORS - Cross-origin requests
- pytest - Testing framework

## Running the Game

### Option A: Web Interface (Recommended)

**Start the server:**

```bash
cd web
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
```

**Open in browser:**
- Navigate to `http://localhost:5000`
- Create character and play!

**Troubleshooting:**
- Port 5000 in use? Change in web/app.py: `app.run(port=5001)`
- Windows + Firewall? May need to allow Python through Windows Defender

### Option B: CLI Commands

```bash
export PYTHONPATH=src  # Linux/Mac
set PYTHONPATH=src     # Windows (PowerShell)

# Create player
python -m codexrpg.cli create-player "Hero" --class warrior

# List NPCs
python -m codexrpg.cli npcs

# Generate world
python -m codexrpg.cli gen-world --width 10 --height 10
```

## Testing

```bash
export PYTHONPATH=src
pytest -v
```

Expected: **23 tests pass** ✅

## Windows Steps (Detailed)

### Step 1: Install Python

1. Download from https://www.python.org/downloads/
2. **Check** "Add Python to PATH"
3. Install for all users

### Step 2: Clone Repository

```powershell
git clone https://github.com/markusm724m-sketch/CodexRPG.git
cd CodexRPG
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run Web Server

```powershell
cd web
python app.py
```

### Step 5: Open Game

1. Open browser (Chrome, Firefox, Edge)
2. Go to: `http://localhost:5000`
3. Create your character

### Batch File (Optional)

Create `start-game.bat`:

```batch
@echo off
cd /d "%~dp0web"
python app.py
pause
```

Run by double-clicking `start-game.bat`

## macOS Steps (Detailed)

### Step 1: Install Python

Using Homebrew (recommended):

```bash
brew install python@3.10
```

Or download from https://www.python.org/downloads/

### Step 2: Clone Repository

```bash
git clone https://github.com/markusm724m-sketch/CodexRPG.git
cd CodexRPG
```

### Step 3: Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Game

```bash
cd web
python app.py
```

Visit `http://localhost:5000` in your browser

## Linux Steps (Detailed)

### Debian/Ubuntu

```bash
# Install Python
sudo apt-get install python3.10 python3-pip

# Clone repo
git clone https://github.com/markusm724m-sketch/CodexRPG.git
cd CodexRPG

# Install dependencies
pip install -r requirements.txt

# Run game
cd web
python3 app.py
```

### Fedora/RHEL

```bash
sudo dnf install python3.10 python3-pip
git clone https://github.com/markusm724m-sketch/CodexRPG.git
cd CodexRPG
pip install -r requirements.txt
cd web
python3 app.py
```

## API Endpoints (For Developers)

The Flask app provides REST API:

```
GET  /                    - Web interface
GET  /api/classes         - Available character classes
POST /api/player/create   - Create new player
GET  /api/player/info     - Get player status
POST /api/player/action   - Execute action (gather, rest, trigger_event)
GET  /api/world/info      - Get world map
GET  /api/npcs            - List all NPCs
GET  /api/npc/<id>        - Get NPC details
GET  /api/quests          - List available quests
GET  /api/reputation      - Get faction reputation
GET  /api/homestead       - Get active homestead
GET  /api/homesteads      - List all homesteads
```

Example API call:

```bash
curl -X POST http://localhost:5000/api/player/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Hero","class":"warrior"}'
```

## Deployment (Production)

For production, use WSGI server instead of Flask dev server:

```bash
pip install gunicorn
cd web
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### "Address already in use"
- Kill existing Flask: `pkill -f "python app.py"`
- Or use different port in app.py

### "ModuleNotFoundError: No module named 'flask'"
- Run: `pip install flask flask-cors`

### "Port 5000 not accessible"
- Windows Firewall: Allow Python.exe
- macOS: Try `python3` instead of `python`
- Linux: May need sudo for ports < 1024

### "Cannot connect to localhost:5000"
- Verify Flask started (no errors)
- Try `http://127.0.0.1:5000` instead
- Check firewall settings

## Next Steps

1. **Play the Game**: Create character, explore, complete quests
2. **Read Code**: See `src/codexrpg/` for game logic
3. **Contribute**: Check `docs/CONTRIBUTING.md`
4. **Report Issues**: Use GitHub issues

## Support

- GitHub: https://github.com/markusm724m-sketch/CodexRPG
- Issues: https://github.com/markusm724m-sketch/CodexRPG/issues
