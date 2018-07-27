import random
import pprint
from time import time
from firebase import firebase
pp = pprint.PrettyPrinter(indent=4)

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def get_players():
    return fb.get('/players', None) or {}


def get_score():
    pass


def find_player(discord_id):
    all_players = get_players()
    # Find or create player from discord_id
    if discord_id in all_players:
        return all_players[discord_id]
    else:
        current_minutes = time() / 60
        new_player = {
            'discord_id': discord_id,
            'points': 1,
            'last_updated': int(current_minutes),
            'items': []
        }
        fb.patch(f'/players/{discord_id}', new_player)
        return new_player


def add_user(discord_id):
    """
    Initialize a new user with one point and return
    """
    current_minutes = time() / 60
    new_player = {
        'discord_id': discord_id,
        'points': 1,
        'last_updated': int(current_minutes),
        'items': []
    }
    fb.patch(f'/players/{discord_id}', new_player)
    return f'You gave {discord_id} one good boy point! Now they have {1}.'


def update_points(player, value, cooldown=False):
    # TODO: Add item check
    if 'items' in player:
        # If the user's new value is less than 10
        if 'Good Boy Belt' in player['items'] and value < 10:
            # Reset it to 10
            value = 10
    player['points'] = value
    if cooldown:
        current_minutes = time() / 60
        player['last_updated'] = (current_minutes)
    fb.patch(f"/players/{player['discord_id']}", player)


def add_point(discord_id):
    all_players = get_players()
    if discord_id in all_players:
        current_minutes = time() / 60
        player = all_players[discord_id]
        # Check if points are on cooldown
        if point_available(player):
            new_total = player['points'] + 1
            # set point cooldown as well
            update_points(player, new_total, cooldown=True)

            player['last_updated'] = (current_minutes)
            fb.patch(f'/players/{discord_id}', player)
            return f"You gave {player['discord_id']} one good boy point! Now they have {new_total}."
        else:
            time_diff = int(current_minutes - player['last_updated'])
            player_name = player['discord_id']
            minutes_left = 5 - time_diff
            return f"It's too soon to give another good boy point to {player_name}! ({minutes_left} minutes left)"
    else:
        # Add user
        return add_user(discord_id)


def point_available(player):
    current_minutes = time() / 60
    last_updated = player['last_updated']
    time_diff = int(current_minutes - last_updated)

    if time_diff > 5:
        return True
    else:
        return False


def flip_coin(amount, player_name):
    pp.pprint(player_name)
    player = find_player(player_name)
    # If the user has enough points to bet
    if 0 <= amount <= player['points']:
        win = random.choice([True, False])
        if win:
            # gain amount bet
            new_total = player['points'] + amount
            update_points(player, new_total)
            return f'<:poggers:471769534903353364> Winner! You won {amount} points! Now you have {new_total}.'

        else:
            # lose amount
            new_total = player['points'] - amount
            update_points(player, new_total)
            insult = random.choice(
                ['stinky loser',
                 'honking goose',
                 'squawking duck',
                 'unbelievable fool',
                 'little baby'])
            return f'You {insult}. You lost {amount} points! Now you have {new_total}.'
    else:
        if amount < 0:
            return "You can't bet negative points!"
        else:
            return f"You can't bet {amount} points, you only have {player['points']}!"
