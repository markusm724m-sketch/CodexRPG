from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
from .item import Item, ItemType


class NPCRole(Enum):
    MERCHANT = "merchant"
    BLACKSMITH = "blacksmith"
    ALCHEMIST = "alchemist"
    VILLAGER = "villager"
    QUEST_GIVER = "quest_giver"


@dataclass
class NPC:
    """Non-player character in the sandbox world."""
    id: str
    name: str
    role: NPCRole
    location: str = "town"
    dialogue: str = "Hello, traveler!"
    
    # Merchant inventory
    buy_prices: Dict[str, int] = None  # item_id -> price they pay
    sell_inventory: List[Item] = None  # items they have for sale
    
    def __post_init__(self):
        if self.buy_prices is None:
            self.buy_prices = {}
        if self.sell_inventory is None:
            self.sell_inventory = []
    
    def talk(self) -> str:
        return self.dialogue
    
    def buy_from_player(self, player_item_id: str) -> int:
        """Return purchase price for item, or -1 if not buying."""
        return self.buy_prices.get(player_item_id, -1)
    
    def sell_to_player(self, item_id: str) -> Item:
        """Return item from inventory by id."""
        for item in self.sell_inventory:
            if item.id == item_id:
                return item
        return None
    
    def list_for_sale(self) -> List[Item]:
        return list(self.sell_inventory)


# Example NPCs for sandbox world
BLACKSMITH = NPC(
    id="blacksmith_oak",
    name="Gruk Oakforge",
    role=NPCRole.BLACKSMITH,
    location="blacksmith_forge",
    dialogue="Need weapons or armor? I can forge the finest..."
)

ALCHEMIST = NPC(
    id="alchemist_zara",
    name="Zara Mistwood",
    role=NPCRole.ALCHEMIST,
    location="alchemy_shop",
    dialogue="Looking for potions? I have exactly what you need."
)

MERCHANT = NPC(
    id="merchant_tudor",
    name="Tudor the Wanderer",
    role=NPCRole.MERCHANT,
    location="market_square",
    dialogue="Best deals in all the realm!"
)

VILLAGER = NPC(
    id="villager_mae",
    name="Mae the Farmer",
    role=NPCRole.VILLAGER,
    location="farm",
    dialogue="Just tending my crops..."
)

NPCS = {
    "blacksmith_oak": BLACKSMITH,
    "alchemist_zara": ALCHEMIST,
    "merchant_tudor": MERCHANT,
    "villager_mae": VILLAGER,
}


def get_npc(npc_id: str) -> NPC:
    return NPCS.get(npc_id)


def list_npcs() -> dict:
    return NPCS
