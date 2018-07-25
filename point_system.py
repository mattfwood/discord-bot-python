from time import time
from firebase import firebase
import pprint
pp = pprint.PrettyPrinter(indent=4)

firebase = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)
all_players = firebase.get('/players', None) or {}
# pp.pprint(all_players)

# player = firebase.post('/players', new_player)
# print(player)

def get_score():
    pass

def add_user(discord_id):
    new_player = {
        'player_id': discord_id,
        'points': 0,
        'last_updated': int(time())
    }
    print(new_player)
    player = firebase.patch('/players/{}'.format(discord_id), new_player)
    return new_player

def add_point(discord_id):
    for key, value in all_players.items():
        player = all_players[key]
        pp.pprint((value))
        if discord_id != value['discord_id']:
            # Add user
            print('USER NOT FOUND')
            add_user(discord_id)

        else:
            print('USER EXISTS')
            firebase.post('/players')


# add_user('GreatBearShark#8830')
