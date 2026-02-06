class Game:
    """Basic game skeleton for CodexRPG."""
    def __init__(self, title: str = "CodexRPG"):
        self.title = title
        self.running = False

    def start(self):
        self.running = True
        return f"{self.title} started"

    def stop(self):
        self.running = False
        return f"{self.title} stopped"
