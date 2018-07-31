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
            raid['players'].append({ discord_id: 30 })
            pass
        else:
            raid['players'] = [{ discord_id: 30 }]
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
    raid['boss']['health'] = 300
    fb.patch(f'/raid/', raid)
    return 'Raid has started! Take turns attacking to try and defeat the boss.'
