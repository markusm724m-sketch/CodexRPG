from dataclasses import dataclass
from typing import List


@dataclass
class Skill:
    """Base skill class with name, description, and effects."""
    id: str
    name: str
    description: str = ""
    damage_bonus: int = 0
    defense_bonus: int = 0
    cost: int = 0  # e.g. mana or stamina


class SkillTree:
    """Container for skills learned by a character."""
    def __init__(self):
        self.skills: List[Skill] = []

    def add_skill(self, skill: Skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def remove_skill(self, skill: Skill):
        if skill in self.skills:
            self.skills.remove(skill)

    def get_skill_by_id(self, skill_id: str) -> Skill:
        for skill in self.skills:
            if skill.id == skill_id:
                return skill
        return None

    def list_skills(self) -> List[Skill]:
        return list(self.skills)


# Примеры базовых навыков четырёх архетипов
WARRIOR_SKILLS = [
    Skill("slash", "Slash", "Basic melee attack", damage_bonus=10),
    Skill("cleave", "Cleave", "Heavy attack on multiple foes", damage_bonus=20),
]

MAGE_SKILLS = [
    Skill("fireball", "Fireball", "Cast a ball of fire", damage_bonus=15, cost=30),
    Skill("shield", "Mage Shield", "Magical barrier", defense_bonus=15, cost=20),
]

ROGUE_SKILLS = [
    Skill("backstab", "Backstab", "Quick precise strike", damage_bonus=12),
    Skill("dodge", "Dodge", "Evade incoming attacks", defense_bonus=10),
]

PALADIN_SKILLS = [
    Skill("smite", "Holy Smite", "Divine strike", damage_bonus=15),
    Skill("blessing", "Holy Blessing", "Heal and protect", defense_bonus=12, cost=20),
]
