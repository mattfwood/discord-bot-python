from time import time
from firebase import firebase
import pprint
pp = pprint.PrettyPrinter(indent=4)

firebase = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)
all_players = firebase.get('/players', None) or {}
players_list = []
id_list = []

for key, value in all_players.items():
    players_list.append(value)
    id_list.append(value['discord_id'])

def get_score():
    pass


def add_user(discord_id):
    new_player = {
        'discord_id': discord_id,
        'points': 1,
        'last_updated': int(time())
    }
    firebase.post('/players/', new_player)
    return 'You gave {} one good boy point! Now they have {}.'.format(
        discord_id, 1)


def add_point(discord_id):
    if discord_id in id_list:
        player_index = id_list.index(discord_id)
        player = players_list[player_index]
        # Check if points are on cooldown
        if point_available(player):
            player['points'] += 1
            player['last_updated'] = (time() / 60)
            firebase.patch('/players/{}'.format(key), player)
            return 'You gave {} one good boy point! Now they have {}.'.format(
                player, player['points'])
        else:
            current_minutes = (time() / 60)
            time_diff = int(current_minutes - player['last_updated'])
            return "It's too soon to give another good boy point to {}! ({} minutes left)".format(player, (60 - time_diff))
    else:
        # Add user
        print('USER NOT FOUND')
        add_user(discord_id)


def point_available(player):
    last_updated = player['last_updated']
    current_minutes = (time() / 60)
    time_diff = int(current_minutes - last_updated)

    if time_diff > 60:
        return True
    else:
        return False


# add_user('GreatBearShark#8830')
add_point('GreatBearShark#8830')
