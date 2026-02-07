"""
CodexRPG Mobile Wrapper
Runs Flask server and shows game in Kivy WebView
"""

import os
import sys
import threading
import time

# Add web directory to path
web_dir = os.path.join(os.path.dirname(__file__), 'web')
sys.path.insert(0, web_dir)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Change to web directory for Flask
os.chdir(web_dir)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

# Set window properties
Window.size = (1080, 1920)  # Mobile resolution

class CodexRPGApp(App):
    """Main app container"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'CodexRPG - Fantasy Sandbox'
        self.server_ready = False
        
    def build(self):
        """Build the app UI"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Status label
        self.status_label = Label(
            text='Starting game server...',
            size_hint_y=0.3,
            color=(1, 0.55, 0, 1)  # Orange
        )
        layout.add_widget(self.status_label)
        
        # Progress indicator
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=0.1
        )
        layout.add_widget(self.progress)
        
        # Info label
        self.info_label = Label(
            text='Loading Flask server...',
            size_hint_y=0.3,
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.info_label)
        
        # Start Flask server in background
        self.start_server()
        
        # Schedule check for server readiness
        Clock.schedule_interval(self.check_server, 0.5)
        
        return layout
    
    def start_server(self):
        """Start Flask server in background thread"""
        def run_flask():
            try:
                # Import and run Flask app
                from app import app
                app.run(
                    host='0.0.0.0',
                    port=5000,
                    debug=False,
                    use_reloader=False,
                    use_debugger=False
                )
            except Exception as e:
                print(f'Flask error: {e}')
        
        thread = threading.Thread(target=run_flask, daemon=True)
        thread.start()
    
    def check_server(self, dt):
        """Check if Flask server is ready"""
        if self.server_ready:
            return False  # Stop checking
        
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            
            if result == 0:
                self.server_ready = True
                self.load_game()
                return False
            else:
                # Update progress
                progress = min(100, self.progress.value + 10)
                self.progress.value = progress
                self.status_label.text = f'Initializing... {int(progress)}%'
                return True
        except Exception as e:
            print(f'Connection check error: {e}')
            return True
    
    def load_game(self):
        """Load game in WebView"""
        try:
            from kivy.uix.webview import WebView
            
            # Update UI
            self.status_label.text = '✓ Game Ready!'
            self.progress.value = 100
            self.info_label.text = 'Loading game interface...'
            
            # Schedule switching to WebView
            Clock.schedule_once(self.switch_to_webview, 1.0)
        except ImportError:
            self.info_label.text = 'WebView module not available'
            self.load_web_interface()
    
    def load_web_interface(self):
        """Fallback: Open in browser"""
        import webbrowser
        try:
            webbrowser.open('http://127.0.0.1:5000')
        except Exception as e:
            print(f'Error opening browser: {e}')
    
    def switch_to_webview(self, dt):
        """Switch to WebView"""
        try:
            from kivy.uix.webview import WebView
            from kivy.uix.verticalscrollview import VerticalScrollView
            
            # Clear existing widgets
            root = self.root
            root.clear_widgets()
            
            # Create WebView
            webview = WebView(url='http://127.0.0.1:5000')
            root.add_widget(webview)
        except Exception as e:
            print(f'WebView error: {e}')
            self.info_label.text = f'Error: {str(e)}\nOpen http://127.0.0.1:5000 in browser'


if __name__ == '__main__':
    # On Android, setup proper paths
    if hasattr(sys, 'base_prefix'):
        # Virtual environment detected
        pass
    
    app = CodexRPGApp()
    app.run()
