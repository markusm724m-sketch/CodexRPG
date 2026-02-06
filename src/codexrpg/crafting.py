from dataclasses import dataclass
from typing import List, Dict
from .item import Item, ItemType, ItemRarity


@dataclass
class Recipe:
    """Crafting recipe."""
    id: str
    name: str
    ingredients: Dict[str, int]  # item_id -> quantity
    result: Item
    complexity: int = 1  # 1-5


class CraftingSystem:
    """Handles crafting for the player."""
    def __init__(self):
        self.recipes: Dict[str, Recipe] = {}
        self.learned_recipes: List[str] = []
    
    def register_recipe(self, recipe: Recipe):
        self.recipes[recipe.id] = recipe
    
    def learn_recipe(self, recipe_id: str) -> bool:
        if recipe_id in self.recipes and recipe_id not in self.learned_recipes:
            self.learned_recipes.append(recipe_id)
            return True
        return False
    
    def can_craft(self, recipe_id: str, inventory: List[Item]) -> bool:
        """Check if player has ingredients for recipe."""
        if recipe_id not in self.learned_recipes:
            return False
        
        recipe = self.recipes.get(recipe_id)
        if not recipe:
            return False
        
        inv_count = {}
        for item in inventory:
            inv_count[item.id] = inv_count.get(item.id, 0) + 1
        
        for ingredient_id, quantity in recipe.ingredients.items():
            if inv_count.get(ingredient_id, 0) < quantity:
                return False
        return True
    
    def craft(self, recipe_id: str, inventory: List[Item]) -> Item:
        """Craft an item and remove ingredients from inventory."""
        if not self.can_craft(recipe_id, inventory):
            return None
        
        recipe = self.recipes[recipe_id]
        
        # Remove ingredients
        remaining = dict(recipe.ingredients)
        i = 0
        while i < len(inventory) and remaining:
            item = inventory[i]
            if item.id in remaining and remaining[item.id] > 0:
                remaining[item.id] -= 1
                inventory.pop(i)
                if remaining[item.id] == 0:
                    del remaining[item.id]
            else:
                i += 1
        
        return recipe.result


# Default recipes
HEALING_POTION = Item(
    id="potion_heal",
    name="Healing Potion",
    description="Restores 50 HP",
    item_type=ItemType.POTION,
    rarity=ItemRarity.COMMON,
    value=50
)

IRON_SWORD = Item(
    id="sword_iron",
    name="Iron Sword",
    description="A sturdy steel blade",
    item_type=ItemType.WEAPON,
    rarity=ItemRarity.UNCOMMON,
    value=150
)

HEALING_RECIPE = Recipe(
    id="craft_healing_potion",
    name="Craft Healing Potion",
    ingredients={"herb_common": 2, "water_pure": 1},
    result=HEALING_POTION,
    complexity=1
)

SWORD_RECIPE = Recipe(
    id="craft_iron_sword",
    name="Forge Iron Sword",
    ingredients={"ore_iron": 5, "coal": 2},
    result=IRON_SWORD,
    complexity=3
)


class GatheringSystem:
    """Handles collecting resources from the environment."""
    def __init__(self):
        self.resource_pools = {}
    
    def add_resource(self, location: str, item: Item, max_qty: int = 999):
        if location not in self.resource_pools:
            self.resource_pools[location] = {}
        self.resource_pools[location][item.id] = {"item": item, "qty": max_qty}
    
    def gather(self, location: str, item_id: str) -> Item:
        """Attempt to gather item from location."""
        if location not in self.resource_pools:
            return None
        
        resource = self.resource_pools[location].get(item_id)
        if resource and resource["qty"] > 0:
            resource["qty"] -= 1
            return resource["item"]
        return None
    
    def list_resources(self, location: str) -> List[Item]:
        """List available resources at location."""
        if location not in self.resource_pools:
            return []
        return [r["item"] for r in self.resource_pools[location].values() if r["qty"] > 0]
