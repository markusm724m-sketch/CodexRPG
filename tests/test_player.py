from codexrpg.player import Player
from codexrpg.item import Item
from codexrpg.character_class import get_class_by_id


def test_player_inventory_and_hp():
    # Use default warrior class
    p = Player("Test", character_class=get_class_by_id("warrior"))
    initial_hp = p.max_hp
    assert p.hp == initial_hp
    p.take_damage(10)
    # Damage reduced by defense: max(1, 10 - 10) = 1
    assert p.hp == initial_hp - 1
    item = Item("potion", "Health Potion")
    p.add_item(item)
    assert p.inventory[0].name == "Health Potion"
    assert p.is_alive() is True
    p.take_damage(200)  # Kill the player
    assert p.is_alive() is False


def test_player_default_class():
    p = Player("Default Hero")
    # Should default to Warrior
    assert p.character_class.id == "warrior"
    assert p.character_class.name == "Warrior"
