"""Advanced world generator using layered value-noise.

Produces an elevation map and classifies biomes by thresholds.
"""
from typing import List, Tuple
import random


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def bilinear_interp(v00: float, v10: float, v01: float, v11: float, tx: float, ty: float) -> float:
    ix0 = lerp(v00, v10, tx)
    ix1 = lerp(v01, v11, tx)
    return lerp(ix0, ix1, ty)


class WorldGenerator:
    def __init__(self, width: int = 64, height: int = 64, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed
        self._rng = random.Random(seed)

    def _random_grid(self, gw: int, gh: int) -> List[List[float]]:
        return [[self._rng.random() for _ in range(gw + 1)] for _ in range(gh + 1)]

    def _sample_grid(self, grid: List[List[float]], x: float, y: float, gw: int, gh: int) -> float:
        # x,y are in [0, gw), [0, gh)
        ix = int(x)
        iy = int(y)
        tx = x - ix
        ty = y - iy
        v00 = grid[iy][ix]
        v10 = grid[iy][ix + 1]
        v01 = grid[iy + 1][ix]
        v11 = grid[iy + 1][ix + 1]
        return bilinear_interp(v00, v10, v01, v11, tx, ty)

    def elevation_map(self, octaves: int = 4, persistence: float = 0.5, base_freq: int = 4) -> List[List[float]]:
        """Generate elevation map using layered value noise.

        Returns a 2D list of floats in range [0, 1].
        """
        out = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        max_amp = 0.0
        amp = 1.0
        freq = base_freq

        for o in range(octaves):
            gw = max(1, freq)
            gh = max(1, freq)
            grid = self._random_grid(gw, gh)
            for y in range(self.height):
                for x in range(self.width):
                    sx = (x / self.width) * gw
                    sy = (y / self.height) * gh
                    val = self._sample_grid(grid, sx, sy, gw, gh)
                    out[y][x] += val * amp
            max_amp += amp
            amp *= persistence
            freq *= 2

        # normalize
        for y in range(self.height):
            for x in range(self.width):
                out[y][x] = max(0.0, min(1.0, out[y][x] / max_amp))
        return out

    def biome_map(self, elevation: List[List[float]] = None) -> List[List[str]]:
        """Classify elevation into biomes.

        Biomes: water, plains, forest, mountain
        """
        if elevation is None:
            elevation = self.elevation_map()
        biomes = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                e = elevation[y][x]
                if e < 0.25:
                    row.append("water")
                elif e < 0.45:
                    row.append("plains")
                elif e < 0.75:
                    row.append("forest")
                else:
                    row.append("mountain")
            biomes.append(row)
        return biomes

    def generate(self, octaves: int = 4, persistence: float = 0.5, base_freq: int = 4) -> Tuple[List[List[float]], List[List[str]]]:
        elevation = self.elevation_map(octaves=octaves, persistence=persistence, base_freq=base_freq)
        biomes = self.biome_map(elevation)
        return elevation, biomes
