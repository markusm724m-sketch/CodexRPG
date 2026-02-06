import argparse
from .game import Game

import argparse
from .game import Game
from .world import World
from .player import Player
from .item import Item, ItemType, ItemRarity
from .character_class import list_classes, get_class_by_id
from .npc import list_npcs, get_npc, NPCRole
from .quest import Quest
from .crafting import GatheringSystem, CraftingSystem, HEALING_RECIPE
from .reputation import Faction
from .events import EventType
from .homestead import HomesteadType


def main():
    parser = argparse.ArgumentParser(prog="codexrpg")
    sub = parser.add_subparsers(dest="cmd")

    start = sub.add_parser("start", help="Start the game")
    start.add_argument("--title", default="CodexRPG")

    gen = sub.add_parser("gen-world", help="Generate a world")
    gen.add_argument("--width", type=int)
    gen.add_argument("--height", type=int)
    gen.add_argument("--seed")

    classes = sub.add_parser("classes", help="List available character classes")

    player = sub.add_parser("create-player", help="Create a player")
    player.add_argument("name", nargs="?", default="Hero")
    player.add_argument("--class", dest="character_class", choices=list(list_classes().keys()), default="warrior")

    npcs = sub.add_parser("npcs", help="List NPCs in the world")

    npc_interact = sub.add_parser("talk-npc", help="Talk to an NPC")
    npc_interact.add_argument("npc_id")

    quests = sub.add_parser("quests", help="List all available quests")

    gather = sub.add_parser("gather", help="Gather resources from location")
    gather.add_argument("location", nargs="?", default="forest")
    gather.add_argument("--item", default="herb_common")

    craft_list = sub.add_parser("craft-list", help="List known recipes")

    craft = sub.add_parser("craft", help="Craft an item")
    craft.add_argument("recipe_id")

    # New: Reputation commands
    rep = sub.add_parser("reputation", help="Check faction reputation")
    rep.add_argument("faction", nargs="?", default="all")
    
    # New: Events commands
    events = sub.add_parser("events", help="Check world events")
    events.add_argument("--trigger", nargs="?", const="random")
    
    # New: Homestead commands
    home = sub.add_parser("home", help="Manage homestead")
    home.add_argument("action", nargs="?", default="info")
    home.add_argument("--name")
    home.add_argument("--type")
    
    # New: Homes list
    homes = sub.add_parser("homes", help="List all homesteads")

    save = sub.add_parser("save", help="Save a minimal game state")
    save.add_argument("path", nargs="?", default="save.json")

    args = parser.parse_args()

    if args.cmd == "start":
        g = Game(args.title)
        print(g.start())
    elif args.cmd == "gen-world":
        w = World(width=args.width, height=args.height)
        grid = w.generate(seed=args.seed)
        print("World generated:")
        for row in grid:
            print(" ".join(row))
    elif args.cmd == "classes":
        print("Available Character Classes:")
        for class_id, cls in list_classes().items():
            print(f"  {class_id.upper()}: {cls.name} - {cls.description}")
            print(f"    HP: {cls.base_hp}, DMG: {cls.base_damage}, DEF: {cls.base_defense}")
    elif args.cmd == "create-player":
        char_class = get_class_by_id(args.character_class)
        p = Player(args.name, character_class=char_class)
        info = p.get_info()
        print(f"Player created: {p.name}")
        print(f"  Class: {p.character_class.name}")
        print(f"  HP: {p.max_hp}, DMG: {p.damage}, DEF: {p.defense}, Gold: {p.gold}")
        print(f"  Skills: {', '.join([s.name for s in p.skill_tree.list_skills()])}")
    elif args.cmd == "npcs":
        print("NPCs in the world:")
        for npc_id, npc in list_npcs().items():
            print(f"  [{npc_id}] {npc.name} ({npc.role.value})")
            print(f"      Location: {npc.location} | {npc.dialogue}")
    elif args.cmd == "talk-npc":
        npc = get_npc(args.npc_id)
        if npc:
            print(f"{npc.name}: {npc.talk()}")
        else:
            print(f"NPC '{args.npc_id}' not found.")
    elif args.cmd == "quests":
        print("Available Quests:")
        print("  [fetch_herbs] Gather 5 herbs - Reward: 100 gold")
        print("  [defeat_bandits] Defeat bandits near the road - Reward: 250 gold")
        print("  [explore_ruins] Explore ancient ruins - Reward: 500 gold")
    elif args.cmd == "gather":
        print(f"Gathering at {args.location}...")
        print(f"  Found: 1x {args.item} (+10 gold)")
    elif args.cmd == "craft-list":
        print("Available Recipes:")
        print("  [craft_healing_potion] Healing Potion - Ingredients: herb_common(2), water_pure(1)")
        print("  [craft_iron_sword] Iron Sword - Ingredients: ore_iron(5), coal(2)")
    elif args.cmd == "craft":
        print(f"Crafting {args.recipe_id}...")
        print("  Success! You crafted an item.")
    elif args.cmd == "reputation":
        print("Faction Reputation:")
        for faction in Faction:
            print(f"  {faction.value}: [Neutral]")
    elif args.cmd == "events":
        if args.trigger:
            if args.trigger == "random":
                print("A random event triggers!")
                print("  [treasure_found] Hidden Treasure discovered at forest...")
            else:
                print(f"Triggering event: {args.trigger}")
        else:
            print("Active World Events:")
            print("  [event_1] Bandit Attack at road - Reward: 50 gold")
            print("  [event_2] Festival in town - Free celebration!")
    elif args.cmd == "home":
        if args.action == "info":
            print("Your Homestead:")
            print("  Name: Cozy Cottage")
            print("  Type: cottage")
            print("  Location: village")
            print("  Level: 1")
            print("  Storage: 5 items")
            print("  Residents: 0")
        elif args.action == "upgrade":
            print("Homestead upgraded to level 2!")
        elif args.action == "build":
            print(f"Building new homestead: {args.name} ({args.type})")
    elif args.cmd == "homes":
        print("Your Homesteads:")
        print("  1. Cozy Cottage (cottage) @ village - Level 1")
        print("  2. Mountain Tower (tower) @ mountains - Level 2")
    elif args.cmd == "save":
        from .save import save_game
        state = {"note": "minimal save"}
        save_game(args.path, state)
        print(f"Saved to {args.path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
