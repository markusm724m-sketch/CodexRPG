from codexrpg.world import World


def test_world_generate():
    w = World(3, 2)
    grid = w.generate(seed=42)
    assert len(grid) == 2
    assert len(grid[0]) == 3
    # biomes should be strings from config
    assert all(isinstance(cell, str) for row in grid for cell in row)
