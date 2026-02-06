from dataclasses import dataclass
from typing import List
from .skills import Skill, SkillTree, WARRIOR_SKILLS, MAGE_SKILLS, ROGUE_SKILLS, PALADIN_SKILLS


@dataclass
class CharacterClass:
    """Represents a character class with attributes and starting skills."""
    id: str
    name: str
    description: str = ""
    base_hp: int = 100
    base_damage: int = 10
    base_defense: int = 5
    starting_skills: List[Skill] = None

    def __post_init__(self):
        if self.starting_skills is None:
            self.starting_skills = []


# Four main classes for medieval fantasy isekai
WARRIOR = CharacterClass(
    id="warrior",
    name="Warrior",
    description="Strong melee fighter with heavy armour",
    base_hp=120,
    base_damage=15,
    base_defense=10,
    starting_skills=WARRIOR_SKILLS
)

MAGE = CharacterClass(
    id="mage",
    name="Mage",
    description="Spellcaster with elemental magic",
    base_hp=70,
    base_damage=8,
    base_defense=3,
    starting_skills=MAGE_SKILLS
)

ROGUE = CharacterClass(
    id="rogue",
    name="Rogue",
    description="Quick and deadly assassin",
    base_hp=85,
    base_damage=12,
    base_defense=6,
    starting_skills=ROGUE_SKILLS
)

PALADIN = CharacterClass(
    id="paladin",
    name="Paladin",
    description="Holy warrior with divine blessings",
    base_hp=110,
    base_damage=13,
    base_defense=12,
    starting_skills=PALADIN_SKILLS
)

CLASSES = {
    "warrior": WARRIOR,
    "mage": MAGE,
    "rogue": ROGUE,
    "paladin": PALADIN,
}


def get_class_by_id(class_id: str) -> CharacterClass:
    return CLASSES.get(class_id)


def list_classes() -> dict:
    return CLASSES
