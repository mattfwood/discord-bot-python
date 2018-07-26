import random
import pprint
from time import time
from firebase import firebase
pp = pprint.PrettyPrinter(indent=4)

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)
all_players = fb.get('/players', None) or {}
players_list = []
id_list = []

for key, value in all_players.items():
    players_list.append(value)
    id_list.append(value['discord_id'])


def get_score():
    pass


def find_player(discord_id):
    # Find or create player from discord_id
    if discord_id in all_players:
        return all_players[discord_id]
    else:
        new_player = {
            'discord_id': discord_id,
            'points': 1,
            'last_updated': int(time() / 60)
        }
        fb.patch('/players/{}'.format(discord_id), new_player)
        return new_player


def add_user(discord_id):
    """
    Initialize a new user with one point and return
    """
    new_player = {
        'discord_id': discord_id,
        'points': 1,
        'last_updated': int(time() / 60)
    }
    fb.patch('/players/{}'.format(discord_id), new_player)
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
            fb.patch('/players/{}'.format(key), player)
            return 'You gave {} one good boy point! Now they have {}.'.format(
                player, player['points'])
        else:
            current_minutes = (time() / 60)
            time_diff = int(current_minutes - player['last_updated'])
            return "It's too soon to give another good boy point to {}! ({} minutes left)".format(player['discord_id'], (60 - time_diff))
    else:
        # Add user
        return add_user(discord_id)


def point_available(player):
    last_updated = player['last_updated']
    current_minutes = (time() / 60)
    time_diff = int(current_minutes - last_updated)

    if time_diff > 60:
        return True
    else:
        return False


def flip_coin(amount, player_name):
    pp.pprint(player_name)
    player = find_player(player_name)
    points = player['points']
    print(player)
    # If the user has enough points to bet
    if 0 <= amount <= player['points']:
        win = random.choice([True, False])
        if win:
            # gain amount bet
            player['points'] += amount
            fb.patch('/players/{}'.format(player_name), player)
            return 'Winner! You won {} points! Now you have {}.'.format(amount, player['points'])

        else:
            # lose amount
            player['points'] -= amount
            fb.patch('/players/{}'.format(player_name), player)
            return 'You stinky loser. You lost {} points! Now you have {}.'.format(amount, player['points'])
    else:
        print('NOT ENOUGH POINTS')
        if amount < 0:
            return "You can't bet negative points!"
        else:
            return (f"You can't bet {amount} points, you only have {player['points']}!")
