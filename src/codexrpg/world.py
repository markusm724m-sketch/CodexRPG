import random
from .config import DEFAULT_CONFIG

class World:
    """Simple world generator producing a grid of biomes."""
    def __init__(self, width=None, height=None):
        cfg = DEFAULT_CONFIG["world"]
        self.width = width or cfg["width"]
        self.height = height or cfg["height"]
        self.grid = []

    def generate(self, seed=None):
        rnd = random.Random(seed)
        biomes = DEFAULT_CONFIG["world"]["biomes"]
        self.grid = [[rnd.choice(biomes) for _ in range(self.width)] for _ in range(self.height)]
        return self.grid
