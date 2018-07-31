from random import randint
from firebase import firebase
from point_system import update_points, find_player
from combat_system import random_encounter

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def raid_fund(amount, discord_id):
    raid = fb.get('/raid', None)
    if raid['active'] is True:
        return 'A raid has already started!'

    if raid and raid['active'] is False:
        # Add raid fund amount
        raid['fund'] += amount
        if 'players' in raid:
            if discord_id not in raid['players']:
                raid['players'][discord_id] = 30
        else:
            raid['players'] = { discord_id: 30 }
        fb.patch(f'/raid/', raid)
        if raid['fund'] < 1000:
            return f"You added {amount} points to the raid fund, bringing the total to {raid['fund']} ({1000 - raid['fund']} remaining to start)"
        else:
            return start_raid()
    else:
        # Create raid
        new_raid = {
            'fund': amount,
            'players': [discord_id],
            'active': False,
        }
        fb.patch(f'/raid/', new_raid)
        return f'You started a new raid fund with {amount} points ({1000 - amount} remaining to start)'


def start_raid():
    raid = fb.get('/raid', None)
    # Mark raid as active
    raid['active'] = True
    raid['boss'] = random_encounter()
    raid['boss']['health'] = 100
    fb.patch(f'/raid/', raid)
    return 'Raid has started! Take turns attacking to try and defeat the boss.'

def raid_attack(discord_id):
    raid = fb.get('/raid', None)
    player = find_player(discord_id)
    combat_text = []
    if raid['active'] is True:
        # Check that player is alive
        player_in_raid = discord_id in raid['players']
        if player_in_raid is False:
            return 'Sorry, you did not fund this raid and cannot participate'

        # Calculate damage
        damage = randint(1, 10)

        # Apply damage to boss
        raid['boss']['health'] -= damage

        combat_text.append(f"You dealt {damage} to {raid['boss']['name']}! ({raid['boss']['health']} HP left)")

        # Check if boss is dead
        boss_dead = raid['boss']['health'] <= 0

        if boss_dead:
            return raid_win(combat_text)

        # Deal damage to player
        boss_damage = randint(1, 10)
        raid['players'][discord_id] -= boss_damage

        player_dead = raid['players'][discord_id] <= 0

        # Check that player is still alive
        if player_dead:
            combat_text.append(f"{raid['boss']['name']} dealt **{boss_damage}** and killed you! Hopefully one of your raid members will avenge your death.")

        # Check that any players are still alive
        no_remaining_players = max(raid['players']) < 1

        if no_remaining_players:
            return raid_loss(combat_text)

        return '\n'.join(combat_text)
    else:
        return "There isn't an active raid."

def raid_win(combat_text):
    combat_text.append("You've defeated the raid boss! Make sure Matt actually adds the points here at some point.")
    return '\n'.join(combat_text)

def raid_loss(combat_text):
    combat_text.append('All raid members have died! The raid has ended.')
    return '\n'.join(combat_text)

def raid_reset():
    pass