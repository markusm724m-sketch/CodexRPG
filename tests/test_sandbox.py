from codexrpg.quest import Quest, QuestLog, QuestStatus
from codexrpg.npc import NPC, NPCRole, get_npc, list_npcs
from codexrpg.crafting import CraftingSystem, Recipe, GatheringSystem, HEALING_RECIPE, HEALING_POTION
from codexrpg.item import Item, ItemType, ItemRarity


def test_quest_lifecycle():
    quest = Quest(
        id="fetch_herbs",
        title="Gather Herbs",
        description="Collect 5 herbs",
        giver_id="npc_1",
        objective="Bring 5 healing herbs"
    )
    assert quest.status == QuestStatus.AVAILABLE
    assert quest.accept() is True
    assert quest.status == QuestStatus.ACTIVE
    assert quest.complete() is True
    assert quest.status == QuestStatus.COMPLETED


def test_quest_log():
    log = QuestLog()
    q1 = Quest("q1", "Quest 1", "Desc", "npc_1", "Objective 1")
    q2 = Quest("q2", "Quest 2", "Desc", "npc_2", "Objective 2")
    
    log.add_quest(q1)
    log.add_quest(q2)
    
    assert len(log.get_available_quests()) == 2
    log.accept_quest("q1")
    assert len(log.get_active_quests()) == 1
    assert len(log.get_available_quests()) == 1


def test_npc_merchants():
    npc = NPC(
        id="merchant_1",
        name="Trader",
        role=NPCRole.MERCHANT,
        dialogue="Welcome, friend!"
    )
    npc.buy_prices["herb_common"] = 15
    npc.sell_inventory.append(HEALING_POTION)
    
    assert npc.talk() == "Welcome, friend!"
    assert npc.buy_from_player("herb_common") == 15
    assert npc.buy_from_player("unknown") == -1
    assert npc.sell_to_player("potion_heal") == HEALING_POTION


def test_crafting_system():
    craft = CraftingSystem()
    craft.register_recipe(HEALING_RECIPE)
    
    assert HEALING_RECIPE.id not in craft.learned_recipes
    craft.learn_recipe(HEALING_RECIPE.id)
    assert HEALING_RECIPE.id in craft.learned_recipes
    
    # Can't craft without ingredients
    inv = []
    assert craft.can_craft(HEALING_RECIPE.id, inv) is False
    
    # Add ingredients
    herb = Item("herb_common", "Common Herb", item_type=ItemType.INGREDIENT)
    water = Item("water_pure", "Pure Water", item_type=ItemType.INGREDIENT)
    inv.extend([herb, herb, water])
    
    assert craft.can_craft(HEALING_RECIPE.id, inv) is True
    result = craft.craft(HEALING_RECIPE.id, inv)
    assert result.id == "potion_heal"
    assert len(inv) == 0


def test_gathering_system():
    gather = GatheringSystem()
    herb = Item("herb_rare", "Rare Herb", rarity=ItemRarity.RARE)
    gather.add_resource("forest", herb, max_qty=3)
    
    resources = gather.list_resources("forest")
    assert len(resources) == 1
    
    item1 = gather.gather("forest", "herb_rare")
    assert item1 is not None
    assert item1.id == "herb_rare"
    
    # Gather twice more
    gather.gather("forest", "herb_rare")
    gather.gather("forest", "herb_rare")
    
    # Now exhausted
    assert gather.gather("forest", "herb_rare") is None


def test_default_npcs_exist():
    npcs = list_npcs()
    assert "blacksmith_oak" in npcs
    assert "alchemist_zara" in npcs
    assert "merchant_tudor" in npcs
    assert "villager_mae" in npcs
    
    blacksmith = get_npc("blacksmith_oak")
    assert blacksmith.role == NPCRole.BLACKSMITH
