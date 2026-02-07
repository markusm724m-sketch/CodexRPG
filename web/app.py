import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from codexrpg.player import Player
from codexrpg.character_class import get_class_by_id, list_classes
from codexrpg.world import World
from codexrpg.npc import list_npcs, get_npc
from codexrpg.quest import Quest
from codexrpg.events import EventType
from codexrpg.reputation import Faction
from codexrpg.item import Item, ItemType

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
CORS(app)

# Global game state (in production use database)
game_state = {
    'player': None,
    'world': None
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/classes', methods=['GET'])
def get_classes():
    classes = list_classes()
    return jsonify({
        'classes': [
            {
                'id': cid,
                'name': c.name,
                'description': c.description,
                'hp': c.base_hp,
                'damage': c.base_damage,
                'defense': c.base_defense,
                'skills': [s.name for s in c.starting_skills]
            }
            for cid, c in classes.items()
        ]
    })


@app.route('/api/player/create', methods=['POST'])
def create_player():
    data = request.json
    name = data.get('name', 'Hero')
    class_id = data.get('class', 'warrior')
    
    char_class = get_class_by_id(class_id)
    player = Player(name, character_class=char_class)
    game_state['player'] = player
    
    # Generate world for this player
    game_state['world'] = World(10, 10)
    game_state['world'].generate(seed=42)
    
    return jsonify({
        'success': True,
        'player': player.get_info()
    })


@app.route('/api/player/info', methods=['GET'])
def player_info():
    if not game_state['player']:
        return jsonify({'error': 'No player created'}), 400
    
    player = game_state['player']
    return jsonify(player.get_info())


@app.route('/api/player/action', methods=['POST'])
def player_action():
    if not game_state['player']:
        return jsonify({'error': 'No player created'}), 400
    
    data = request.json
    action = data.get('action')
    player = game_state['player']
    
    if action == 'gather':
        player.add_gold(10)
        item = Item(f"resource_{player.gold}", "Gathered Resource")
        player.add_item(item)
        return jsonify({'success': True, 'message': 'Gathered resources!', 'gold': player.gold})
    
    elif action == 'rest':
        player.hp = player.max_hp
        return jsonify({'success': True, 'message': 'Fully rested!', 'hp': player.hp})
    
    elif action == 'trigger_event':
        event = player.events.random_event()
        return jsonify({
            'success': True,
            'event': {
                'title': event.title,
                'description': event.description,
                'reward': event.reward
            }
        })
    
    return jsonify({'error': 'Unknown action'}), 400


@app.route('/api/world/info', methods=['GET'])
def world_info():
    if not game_state['world']:
        return jsonify({'error': 'No world generated'}), 400
    
    world = game_state['world']
    return jsonify({
        'width': world.width,
        'height': world.height,
        'grid': world.grid
    })


@app.route('/api/npcs', methods=['GET'])
def get_npcs_list():
    npcs = list_npcs()
    return jsonify({
        'npcs': [
            {
                'id': nid,
                'name': n.name,
                'role': n.role.value,
                'location': n.location,
                'dialogue': n.dialogue
            }
            for nid, n in npcs.items()
        ]
    })


@app.route('/api/npc/<npc_id>', methods=['GET'])
def npc_info(npc_id):
    npc = get_npc(npc_id)
    if not npc:
        return jsonify({'error': 'NPC not found'}), 404
    
    return jsonify({
        'id': npc_id,
        'name': npc.name,
        'role': npc.role.value,
        'location': npc.location,
        'dialogue': npc.dialogue
    })


@app.route('/api/quests', methods=['GET'])
def quests_list():
    return jsonify({
        'quests': [
            {'id': 'fetch_herbs', 'title': 'Gather 5 herbs', 'reward': 100},
            {'id': 'defeat_bandits', 'title': 'Defeat bandits near the road', 'reward': 250},
            {'id': 'explore_ruins', 'title': 'Explore ancient ruins', 'reward': 500}
        ]
    })


@app.route('/api/reputation', methods=['GET'])
def get_reputation():
    if not game_state['player']:
        return jsonify({'error': 'No player created'}), 400
    
    player = game_state['player']
    reps = player.reputation.get_all_reputations()
    
    return jsonify({
        'reputation': {
            faction: {
                'value': rep,
                'status': player.reputation.get_faction_status(Faction[faction.upper()])
            }
            for faction, rep in reps.items()
        }
    })


@app.route('/api/homestead', methods=['GET'])
def homestead_info():
    if not game_state['player']:
        return jsonify({'error': 'No player created'}), 400
    
    player = game_state['player']
    home = player.homesteads.get_active_homestead()
    
    if not home:
        return jsonify({'error': 'No homestead'}), 400
    
    return jsonify(home.get_info())


@app.route('/api/homesteads', methods=['GET'])
def homesteads_list():
    if not game_state['player']:
        return jsonify({'error': 'No player created'}), 400
    
    player = game_state['player']
    homes = player.homesteads.list_homesteads()
    
    return jsonify({
        'homesteads': [h.get_info() for h in homes]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
