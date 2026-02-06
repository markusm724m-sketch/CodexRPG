from codexrpg import Game


def test_game_start_stop():
    g = Game("TestWorld")
    assert g.start() == "TestWorld started"
    assert g.running is True
    assert g.stop() == "TestWorld stopped"
    assert g.running is False
