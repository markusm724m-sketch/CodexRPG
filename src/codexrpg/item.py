from dataclasses import dataclass
from enum import Enum


class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    INGREDIENT = "ingredient"
    QUEST = "quest"


@dataclass
class Item:
    id: str
    name: str
    description: str = ""
    item_type: ItemType = ItemType.INGREDIENT
    rarity: ItemRarity = ItemRarity.COMMON
    value: int = 10  # gold/currency value
    sellable: bool = True
    
    def __hash__(self):
        return hash(self.id)
