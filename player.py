from time import time
from firebase import firebase

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)

def find_player(discord_id: str):
    all_players = fb.get('/players', None) or {}
    # Find or create player from discord_id
    if discord_id in all_players:
        return all_players[discord_id]
    else:
        current_minutes = time() / 60
        new_player = {
            'discord_id': discord_id,
            'points': 1,
            'last_updated': int(current_minutes),
            'items': {}
        }
        fb.patch(f'/players/{discord_id}', new_player)
        return new_player

class Player:
    def __init__(self, discord_id):
        player = find_player(discord_id)
        items = player['items'] if 'items' in player else {}
        self.items = items
        self.points = player['points']
        self.discord_id = player['discord_id']
        self.last_updated = player['last_updated']

    def check_points(self, value):
        return self.points > value

    def update_player(self):
        player = vars(self)
        fb.patch(f'/players/{self.discord_id}', player)

    def update_points(self, amount):
        self.points += amount
        self.update_player()

    def has_item(self, item_name):
        return item_name in self.items

    def delete_player(self):
        """Mostly used for test teardown"""
        fb.delete(f'/players/{self.discord_id}', None)