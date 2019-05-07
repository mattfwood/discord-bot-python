from random import choice, randint
from time import time
from firebase_helper import fb
from player import Player


def get_players():
    return fb.get('/players', None) or {}


def find_player(discord_id: str):
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
            'items': [],
        }
        fb.update(f'/players/{discord_id}', new_player)
        return new_player


def add_user(discord_id: str) -> str:
    """
    Initialize a new user with one point and return
    """
    current_minutes = time() / 60
    new_player = {
        'discord_id': discord_id,
        'points': 1,
        'last_updated': int(current_minutes),
        'items': [],
    }
    fb.update(f'/players/{discord_id}', new_player)
    return f'You gave <@{discord_id}> one good boy point! Now they have {1}.'


def update_points(player, value: int, cooldown: bool = False) -> None:
    # TODO: Add item check
    if 'items' in player:
        # If the user's new value is less than 10
        if 'Good Boy Belt' in player['items'] and value < 10:
            # Reset it to 10
            value = 10
    player['points'] = value
    if cooldown:
        current_minutes = time() / 60
        player['last_updated'] = current_minutes
    fb.update(f"/players/{player['discord_id']}", player)


def add_point(discord_id: str) -> str:
    all_players = get_players()
    if discord_id in all_players:
        current_minutes = time() / 60
        player = all_players[discord_id]
        # Check if points are on cooldown
        if point_available(player):
            new_total = player['points'] + 1
            # set point cooldown as well
            update_points(player, new_total, cooldown=True)

            player['last_updated'] = current_minutes
            fb.update(f'/players/{discord_id}', player)
            return f"You gave <@{player['discord_id']}> one good boy point! Now they have {new_total}."
        else:
            time_diff = int(current_minutes - player['last_updated'])
            minutes_left = 5 - time_diff
            return f"It's too soon to give another good boy point to <@{player['discord_id']}>! ({minutes_left} minutes left)"
    else:
        # Add user
        return add_user(discord_id)


def point_available(player) -> bool:
    current_minutes = time() / 60
    last_updated = player['last_updated']
    time_diff = int(current_minutes - last_updated)

    if time_diff > 5:
        return True
    else:
        return False


def flip_coin(amount: int, player_name: str) -> str:
    # player = find_player(player_name)
    player = Player(player_name)
    # If the user has enough points to bet
    if 0 <= amount <= player.points:
        if 'Loaded Dice' in player.items:
            roll = randint(1, 100)
            win = roll <= 60
        else:
            win = choice([True, False])
        if win:
            # gain amount bet
            player.update_points(amount)

            if 'Loaded Dice' in player.items:
                return f"<:poggers:471769534903353364> Hmm... Those dice don't look right, but you won {amount} points! Now you have {player.points}."
            else:
                return f'<:poggers:471769534903353364> Winner! You won {amount} points! Now you have {player.points}.'

        else:
            # lose amount
            player.update_points(-amount)
            insult = choice(
                [
                    'stinky loser',
                    'honking goose',
                    'squawking duck',
                    'unbelievable fool',
                    'little baby',
                ]
            )
            return (
                f'You {insult}. You lost {amount} points! Now you have {player.points}.'
            )
    else:
        if amount < 0:
            return "You can't bet negative points!"
        else:
            return f"You can't bet {amount} points, you only have {player.points}!"


def bet_total(discord_id, half=False):
    player = Player(discord_id)
    total_points = player.points / 2 if half else player.points
    return flip_coin(total_points, discord_id)


if __name__ == "__main__":
    print(flip_coin(1, '199772341679554561'))
