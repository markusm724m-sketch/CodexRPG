# Mobile & APK Build Guide

## Playing on Mobile

### Option A: Progressive Web App (Recommended - No Installation)

The web interface is fully responsive and works on any mobile browser!

#### Android (Chrome)
1. Open `http://localhost:5000` in Chrome
2. Tap menu (⋮) → "Install app" or "Add to Home screen"
3. App will be installed with offline support

#### iOS (Safari)
1. Open `http://localhost:5000` in Safari
2. Tap Share → "Add to Home Screen"
3. App installs to home screen
4. Works offline!

### Option B: Native APK (Advanced)

Build a native Android APK from the Flask game server.

#### Requirements
- Python 3.10+
- Java JDK 11+
- Android SDK (optional, buildozer handles it)
- Linux/macOS (Windows needs WSL2)

#### Method 1: Using Buildozer (Recommended)

**1. Install dependencies (Linux/Debian):**

```bash
sudo apt-get install -y \
  build-essential \
  git \
  python3-dev \
  python3-pip \
  libffi-dev \
  libssl-dev \
  zlib1g-dev \
  openjdk-11-jdk
```

**2. Install Buildozer:**

```bash
pip install buildozer cython
```

**3. Create buildozer config:**

```bash
cd /workspaces/CodexRPG
buildozer init
```

This creates `buildozer.spec`. Edit it:

```ini
[app]
title = CodexRPG
package.name = codexrpg
package.domain = org.codexrpg

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = python3,kivy,requests

permissions = INTERNET,ACCESS_NETWORK_STATE

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
```

**4. Build APK:**

```bash
buildozer android debug
```

Output: `bin/codexrpg-1.0-debug.apk`

**5. Install on device:**

```bash
# Via ADB (Android Debug Bridge)
adb install bin/codexrpg-1.0-debug.apk

# Or manually: copy APK to phone and open it
```

#### Method 2: Using Kivy + WebView

Create a wrapper that embeds the web interface:

**1. Install Kivy:**

```bash
pip install kivy kivy-garden
```

**2. Create main.py:**

```python
from kivy.app import App
from kivy.garden.androidbrowser import AndroidBrowser
from kivy.uix.boxlayout import BoxLayout

class CodexRPGApp(App):
    def build(self):
        layout = BoxLayout()
        browser = AndroidBrowser()
        browser.go('http://localhost:5000')
        layout.add_widget(browser)
        return layout

if __name__ == '__main__':
    CodexRPGApp().run()
```

**3. Build with buildozer (same as above)**

#### Method 3: Cloud APK Builder

Use free online tools without local setup:

1. Visit: https://www.phonegap.com/
2. Upload your Flask app as zip
3. Get APK emailed to you

### Testing APK

#### On Device (Recommended)
1. Enable "Unknown sources" in Settings
2. Download APK file
3. Tap to install
4. Grant permissions
5. Launch and play!

#### In Emulator
```bash
# Install Android Studio
# Create emulator
# Then: adb install app.apk
```

### Running Local Server on Phone

For development, expose Flask server to local network:

**1. Find your PC IP:**

Linux/Mac:
```bash
ifconfig | grep "inet "
```

Windows:
```cmd
ipconfig | grep IPv4
```

Example: `192.168.1.100`

**2. Run Flask with network address:**

```bash
cd web
python app.py
```

Look for: `Running on http://0.0.0.0:5000`

**3. On phone, open:**

```
http://192.168.1.100:5000
```

### Offline Mode

The Progressive Web App caches game assets so you can:
- Play offline (limited features)
- Sync when connected
- Continue game automatically

Cached data includes:
- UI (HTML/CSS/JS)
- Game classes and NPCs
- Last player state

### Features by Platform

| Feature | PC | Web | PWA | APK |
|---------|----|----|-----|-----|
| Full game | ✓ | ✓ | ✓ | ✓ |
| Offline | ✗ | ✗ | ✓ | ✓ |
| Home screen | ✗ | ✗ | ✓ | ✓ |
| Native feel | ✗ | ✗ | ✓ | ✓ |
| App store | ✗ | ✗ | ✗ | ✓ |

### Publishing to Play Store

1. Build release APK (not debug)
2. Sign APK with private key
3. Upload to Google Play Console
4. Fill store listing
5. Submit for review

Process takes 2-3 days.

### Troubleshooting

**"Address in use" error:**
```bash
# Kill existing Flask
pkill -f "python app.py"

# Or use different port
# Edit web/app.py: app.run(port=8000)
```

**"Cannot connect" from phone:**
1. Verify phone on same WiFi as PC
2. Check firewall allows port 5000
3. Try IP instead of localhost
4. Disable VPN

**APK too large:**
- Remove unused assets from buildozer.spec
- Use `buildozer android release` for optimized build

**App crashes on startup:**
- Check Logcat: `adb logcat`
- Verify all dependencies installed
- Rebuild with `buildozer android debug`

### Next Steps

1. **Test PWA first** - no setup needed
2. **Build APK** if you need native app
3. **Publish to Play Store** for distribution
4. **Add notifications & sound** for mobile experience

---

**Quick Start (PWA - 30 seconds):**
1. Start Flask: `cd web && python app.py`
2. On phone: Open `http://192.168.x.x:5000` in Chrome
3. Tap menu → "Install app"
4. Play!
