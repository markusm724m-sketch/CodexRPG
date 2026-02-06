from dataclasses import dataclass
from enum import Enum
from typing import List, Callable
import random


class EventType(Enum):
    BANDIT_ENCOUNTER = "bandit_encounter"
    TREASURE_FOUND = "treasure_found"
    NPC_LOST = "npc_lost"
    WEATHER_CHANGE = "weather_change"
    FESTIVAL = "festival"
    MONSTER_SPAWN = "monster_spawn"
    TRAVELER_DISTRESS = "traveler_distress"


@dataclass
class WorldEvent:
    """A dynamic event that occurs in the world."""
    id: str
    event_type: EventType
    title: str
    description: str
    location: str
    active: bool = True
    reward: int = 0  # gold or exp
    
    def resolve(self):
        self.active = False


class EventSystem:
    """Manages dynamic world events."""
    def __init__(self):
        self.events: dict[str, WorldEvent] = {}
        self.event_counter = 0
    
    def trigger_event(self, event_type: EventType, location: str = "world") -> WorldEvent:
        """Trigger a random event of given type."""
        self.event_counter += 1
        event_id = f"event_{self.event_counter}"
        
        title, description, reward = self._get_event_details(event_type)
        
        event = WorldEvent(
            id=event_id,
            event_type=event_type,
            title=title,
            description=description,
            location=location,
            reward=reward
        )
        self.events[event_id] = event
        return event
    
    def _get_event_details(self, event_type: EventType) -> tuple:
        """Return (title, description, reward) for event type."""
        details = {
            EventType.BANDIT_ENCOUNTER: (
                "Bandits on the Road",
                "A group of bandits blocks your path!",
                50
            ),
            EventType.TREASURE_FOUND: (
                "Hidden Treasure",
                "You found a glimmering chest!",
                200
            ),
            EventType.NPC_LOST: (
                "Lost Traveler",
                "A traveler seems lost and confused.",
                75
            ),
            EventType.WEATHER_CHANGE: (
                "Storm Approaching",
                "Dark clouds gather overhead.",
                0
            ),
            EventType.FESTIVAL: (
                "Town Festival",
                "A celebration has started in town!",
                100
            ),
            EventType.MONSTER_SPAWN: (
                "Strange Creature",
                "An unusual beast emerges from the shadows.",
                150
            ),
            EventType.TRAVELER_DISTRESS: (
                "Help Needed",
                "Someone calls for assistance!",
                80
            ),
        }
        return details.get(event_type, ("Unknown Event", "Something happened.", 0))
    
    def get_event(self, event_id: str) -> WorldEvent:
        return self.events.get(event_id)
    
    def get_active_events(self, location: str = None) -> List[WorldEvent]:
        """Get all active events, optionally filtered by location."""
        events = [e for e in self.events.values() if e.active]
        if location:
            events = [e for e in events if e.location == location]
        return events
    
    def resolve_event(self, event_id: str):
        """Mark event as resolved."""
        if event_id in self.events:
            self.events[event_id].resolve()
    
    def random_event(self, location: str = "world") -> WorldEvent:
        """Generate a completely random event."""
        event_type = random.choice(list(EventType))
        return self.trigger_event(event_type, location)
