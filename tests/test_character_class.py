from codexrpg.character_class import get_class_by_id, list_classes, WARRIOR, MAGE
from codexrpg.skills import Skill, SkillTree
from codexrpg.player import Player


def test_character_classes_exist():
    classes = list_classes()
    assert "warrior" in classes
    assert "mage" in classes
    assert "rogue" in classes
    assert "paladin" in classes


def test_warrior_stats():
    warrior = get_class_by_id("warrior")
    assert warrior.name == "Warrior"
    assert warrior.base_hp == 120
    assert warrior.base_damage == 15
    assert warrior.base_defense == 10


def test_mage_stats():
    mage = get_class_by_id("mage")
    assert mage.name == "Mage"
    assert mage.base_hp == 70
    assert mage.base_damage == 8


def test_skill_tree():
    tree = SkillTree()
    skill1 = Skill("test1", "Test Skill 1")
    skill2 = Skill("test2", "Test Skill 2", damage_bonus=5)
    
    tree.add_skill(skill1)
    assert len(tree.list_skills()) == 1
    
    tree.add_skill(skill2)
    assert len(tree.list_skills()) == 2
    
    found = tree.get_skill_by_id("test2")
    assert found.name == "Test Skill 2"
    assert found.damage_bonus == 5


def test_player_with_class():
    warrior = get_class_by_id("warrior")
    p = Player("Test Warrior", character_class=warrior)
    
    assert p.character_class.name == "Warrior"
    assert p.max_hp == 120
    assert p.damage == 15
    assert p.defense == 10
    # Should have starting skills
    assert len(p.skill_tree.list_skills()) > 0


def test_player_defense_reduces_damage():
    mage = get_class_by_id("mage")
    p = Player("Test Mage", character_class=mage)
    initial_hp = p.hp
    
    # Deal 20 damage to mage with 3 defense
    # Actual damage should be 20 - 3 = 17
    p.take_damage(20)
    assert p.hp == initial_hp - 17
