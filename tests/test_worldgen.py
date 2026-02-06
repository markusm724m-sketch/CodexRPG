from codexrpg.worldgen import WorldGenerator


def test_worldgen_reproducible():
    wg1 = WorldGenerator(16, 12, seed=12345)
    elev1, biomes1 = wg1.generate(octaves=3)

    wg2 = WorldGenerator(16, 12, seed=12345)
    elev2, biomes2 = wg2.generate(octaves=3)

    # elevation and biome maps should be identical with same seed
    assert elev1 == elev2
    assert biomes1 == biomes2


def test_biome_values():
    wg = WorldGenerator(8, 6, seed=99)
    elev, biomes = wg.generate(octaves=2)
    allowed = {"water", "plains", "forest", "mountain"}
    for row in biomes:
        for b in row:
            assert b in allowed
