from typing import List, Optional
from .item import Item
from .config import DEFAULT_CONFIG
from .skills import SkillTree
from .character_class import CharacterClass, WARRIOR
from .quest import QuestLog
from .crafting import CraftingSystem
from .reputation import ReputationSystem, Faction
from .events import EventSystem
from .homestead import HomesteadSystem, create_starter_home


class Player:
    def __init__(self, name: str = "Hero", character_class: CharacterClass = None, max_hp: int = None):
        self.name = name
        self.character_class = character_class or WARRIOR
        self.max_hp = max_hp or self.character_class.base_hp
        self.hp = self.max_hp
        self.damage = self.character_class.base_damage
        self.defense = self.character_class.base_defense
        self.gold = 0  # currency
        self.inventory: List[Item] = []
        self.skill_tree = SkillTree()
        self.quest_log = QuestLog()
        self.crafting = CraftingSystem()
        
        # New sandbox systems
        self.reputation = ReputationSystem()
        self.events = EventSystem()
        self.homesteads = HomesteadSystem()
        
        # Create starter home
        starter_home = create_starter_home()
        self.homesteads.create_homestead(
            starter_home.id,
            starter_home.name,
            starter_home.homestead_type,
            starter_home.location
        )
        
        # Learn starting skills from class
        for skill in self.character_class.starting_skills:
            self.skill_tree.add_skill(skill)

    def take_damage(self, amount: int) -> int:
        # Apply defense reduction
        reduced_damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - reduced_damage)
        return self.hp

    def add_item(self, item: Item):
        self.inventory.append(item)
    
    def remove_item(self, item: Item) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def add_gold(self, amount: int):
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def is_alive(self) -> bool:
        return self.hp > 0
    
    def get_info(self) -> dict:
        """Return player info as dictionary."""
        active_home = self.homesteads.get_active_homestead()
        home_info = active_home.get_info() if active_home else None
        
        return {
            "name": self.name,
            "class": self.character_class.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "defense": self.defense,
            "gold": self.gold,
            "skills": [s.name for s in self.skill_tree.list_skills()],
            "inventory_size": len(self.inventory),
            "active_quests": len(self.quest_log.get_active_quests()),
            "homesteads": len(self.homesteads.list_homesteads()),
            "current_home": home_info,
            "active_events": len(self.events.get_active_events())
        }
