from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class Faction(Enum):
    """Game factions for reputation tracking."""
    MERCHANTS_GUILD = "merchants_guild"
    BLACKSMITH_UNION = "blacksmith_union"
    NATURE_DRUIDS = "nature_druids"
    ROYAL_GUARD = "royal_guard"


@dataclass
class FactionReputation:
    """Tracks reputation with a single faction."""
    faction: Faction
    reputation: int = 0  # -1000 to 1000
    
    def is_friendly(self) -> bool:
        return self.reputation > 200
    
    def is_hostile(self) -> bool:
        return self.reputation < -200
    
    def add_reputation(self, amount: int):
        # Clamp between -1000 and 1000
        self.reputation = max(-1000, min(1000, self.reputation + amount))


class ReputationSystem:
    """Manages player reputation with all factions."""
    def __init__(self):
        self.factions: Dict[Faction, FactionReputation] = {
            faction: FactionReputation(faction) for faction in Faction
        }
    
    def add_reputation(self, faction: Faction, amount: int):
        """Add reputation points with a faction."""
        if faction in self.factions:
            self.factions[faction].add_reputation(amount)
    
    def get_reputation(self, faction: Faction) -> int:
        """Get current reputation with faction."""
        if faction in self.factions:
            return self.factions[faction].reputation
        return 0
    
    def is_friendly_with(self, faction: Faction) -> bool:
        """Check if friendly with faction."""
        if faction in self.factions:
            return self.factions[faction].is_friendly()
        return False
    
    def is_hostile_with(self, faction: Faction) -> bool:
        """Check if hostile with faction."""
        if faction in self.factions:
            return self.factions[faction].is_hostile()
        return False
    
    def get_faction_status(self, faction: Faction) -> str:
        """Get human-readable faction status."""
        rep = self.get_reputation(faction)
        if rep > 500:
            return "Honored"
        elif rep > 200:
            return "Friendly"
        elif rep > 0:
            return "Favorable"
        elif rep > -200:
            return "Neutral"
        elif rep > -500:
            return "Unfavorable"
        else:
            return "Hostile"
    
    def get_all_reputations(self) -> Dict[str, int]:
        """Get all faction reputations as dict."""
        return {
            faction.value: rep.reputation 
            for faction, rep in self.factions.items()
        }
