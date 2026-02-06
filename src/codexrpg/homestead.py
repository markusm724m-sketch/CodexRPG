from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
from .item import Item


class HomesteadType(Enum):
    """Types of player homesteads."""
    COTTAGE = "cottage"
    TOWER = "tower"
    CAVE = "cave"
    TAVERN = "tavern"
    ESTATE = "estate"


@dataclass
class Homestead:
    """A player's personal base/home."""
    id: str
    name: str
    homestead_type: HomesteadType
    location: str = "unknown"
    level: int = 1  # upgrade level
    storage: List[Item] = field(default_factory=list)
    npcs_living_here: List[str] = field(default_factory=list)  # NPC IDs
    gold_stored: int = 0
    
    def add_storage_item(self, item: Item):
        """Store item in homestead."""
        self.storage.append(item)
    
    def remove_storage_item(self, item: Item) -> bool:
        """Remove item from storage."""
        if item in self.storage:
            self.storage.remove(item)
            return True
        return False
    
    def upgrade(self, gold_cost: int = 500) -> bool:
        """Upgrade the homestead."""
        if self.gold_stored >= gold_cost:
            self.gold_stored -= gold_cost
            self.level += 1
            return True
        return False
    
    def add_resident(self, npc_id: str):
        """Add an NPC resident (companion/worker)."""
        if npc_id not in self.npcs_living_here:
            self.npcs_living_here.append(npc_id)
    
    def get_info(self) -> dict:
        """Get homestead information."""
        return {
            "name": self.name,
            "type": self.homestead_type.value,
            "location": self.location,
            "level": self.level,
            "storage_items": len(self.storage),
            "gold": self.gold_stored,
            "residents": len(self.npcs_living_here)
        }


class HomesteadSystem:
    """Manages player homesteads and properties."""
    def __init__(self):
        self.homesteads: Dict[str, Homestead] = {}
        self.active_homestead_id: str = None
    
    def create_homestead(self, homestead_id: str, name: str, 
                        homestead_type: HomesteadType, location: str = "world") -> Homestead:
        """Create a new homestead."""
        homestead = Homestead(
            id=homestead_id,
            name=name,
            homestead_type=homestead_type,
            location=location
        )
        self.homesteads[homestead_id] = homestead
        if not self.active_homestead_id:
            self.active_homestead_id = homestead_id
        return homestead
    
    def get_homestead(self, homestead_id: str) -> Homestead:
        """Get homestead by ID."""
        return self.homesteads.get(homestead_id)
    
    def set_active_homestead(self, homestead_id: str) -> bool:
        """Set the active homestead."""
        if homestead_id in self.homesteads:
            self.active_homestead_id = homestead_id
            return True
        return False
    
    def get_active_homestead(self) -> Homestead:
        """Get the currently active homestead."""
        if self.active_homestead_id:
            return self.homesteads.get(self.active_homestead_id)
        return None
    
    def list_homesteads(self) -> List[Homestead]:
        """List all player homesteads."""
        return list(self.homesteads.values())
    
    def teleport_to_homestead(self, homestead_id: str) -> bool:
        """"Teleport" (travel) to a homestead."""
        if homestead_id in self.homesteads:
            self.active_homestead_id = homestead_id
            return True
        return False


# Example homestead creation helper
def create_starter_home() -> Homestead:
    """Create a starter cottage for new players."""
    return Homestead(
        id="home_cottage_1",
        name="Cozy Cottage",
        homestead_type=HomesteadType.COTTAGE,
        location="village",
        level=1,
        gold_stored=100
    )
