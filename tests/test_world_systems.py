from codexrpg.reputation import ReputationSystem, Faction
from codexrpg.events import EventSystem, EventType
from codexrpg.homestead import HomesteadSystem, HomesteadType, Homestead
from codexrpg.player import Player
from codexrpg.character_class import get_class_by_id
from codexrpg.item import Item, ItemType


def test_reputation_system():
    rep = ReputationSystem()
    
    # Initially neutral with all factions
    assert rep.get_reputation(Faction.MERCHANTS_GUILD) == 0
    assert rep.get_faction_status(Faction.MERCHANTS_GUILD) == "Neutral"
    
    # Add reputation
    rep.add_reputation(Faction.MERCHANTS_GUILD, 300)
    assert rep.get_reputation(Faction.MERCHANTS_GUILD) == 300
    assert rep.is_friendly_with(Faction.MERCHANTS_GUILD)
    assert rep.get_faction_status(Faction.MERCHANTS_GUILD) == "Friendly"
    
    # Go hostile
    rep.add_reputation(Faction.ROYAL_GUARD, -600)
    assert rep.is_hostile_with(Faction.ROYAL_GUARD)
    
    # Cap at limits
    rep.add_reputation(Faction.MERCHANTS_GUILD, 1000)
    assert rep.get_reputation(Faction.MERCHANTS_GUILD) == 1000


def test_event_system():
    events = EventSystem()
    
    # Trigger event
    event = events.trigger_event(EventType.TREASURE_FOUND, "forest")
    assert event.title == "Hidden Treasure"
    assert event.active
    assert event.reward == 200
    
    # Resolve event
    events.resolve_event(event.id)
    assert not events.get_event(event.id).active
    
    # Get active events
    event2 = events.trigger_event(EventType.BANDIT_ENCOUNTER, "road")
    active = events.get_active_events()
    assert len(active) == 1  # only event2 is active
    
    # Random event
    random_event = events.random_event("village")
    assert random_event.location == "village"
    assert random_event.active


def test_homestead_system():
    homes = HomesteadSystem()
    
    # Create homestead
    home = homes.create_homestead("home1", "My House", HomesteadType.COTTAGE, "village")
    assert home.name == "My House"
    assert home.level == 1
    
    # Storage
    item = Item("key", "Golden Key", item_type=ItemType.QUEST)
    home.add_storage_item(item)
    assert len(home.storage) == 1
    
    # Gold and upgrade
    home.gold_stored = 500
    assert home.upgrade(500)
    assert home.level == 2
    assert home.gold_stored == 0
    
    # Residents
    home.add_resident("npc_1")
    assert "npc_1" in home.npcs_living_here
    
    # Multiple homesteads
    home2 = homes.create_homestead("home2", "Tower", HomesteadType.TOWER, "mountains")
    assert len(homes.list_homesteads()) == 2
    
    # Switch active
    assert homes.get_active_homestead().name == "My House"
    homes.set_active_homestead("home2")
    assert homes.get_active_homestead().name == "Tower"


def test_player_with_sandbox_systems():
    player = Player("Aventurer", character_class=get_class_by_id("rogue"))
    
    # Has all sandbox systems
    assert player.reputation is not None
    assert player.events is not None
    assert player.homesteads is not None
    
    # Started with a home
    assert len(player.homesteads.list_homesteads()) == 1
    home = player.homesteads.get_active_homestead()
    assert home.name == "Cozy Cottage"
    
    # Can trigger events
    event = player.events.random_event()
    assert event.active
    
    # Can build reputation
    player.reputation.add_reputation(Faction.NATURE_DRUIDS, 100)
    assert player.reputation.get_reputation(Faction.NATURE_DRUIDS) == 100
    
    # Player info includes homestead details
    info = player.get_info()
    assert info["homesteads"] >= 1
    assert info["current_home"]["name"] == "Cozy Cottage"
    assert info["active_events"] >= 0


def test_homestead_info():
    home = Homestead(
        id="test",
        name="Test Home",
        homestead_type=HomesteadType.ESTATE,
        level=3,
        gold_stored=250
    )
    home.add_resident("villager_mae")
    
    info = home.get_info()
    assert info["name"] == "Test Home"
    assert info["type"] == "estate"
    assert info["level"] == 3
    assert info["gold"] == 250
    assert info["residents"] == 1
