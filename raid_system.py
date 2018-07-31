from firebase import firebase
from point_system import update_points, find_player

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def raid_fund(amount, discord_id):
    raid = fb.get('/raid', None)
    if raid:
        # Add raid fund amount
        raid['fund'] += amount
        if 'players' in raid:
            raid['players'].append(discord_id)
            pass
        else:
            raid['players'] = [discord_id]
        fb.patch(f'/raid/', raid)
        if raid['fund'] < 1000:
            return f"You added {amount} points to the raid fund, bringing the total to {raid['fund']} ({1000 - raid['fund']} remaining to start)"
        else:
            raise Exception('Raid Not Implemented')

    else:
        # Create raid
        new_raid = {
            'fund': amount,
            'players': [discord_id]
        }
        fb.patch(f'/raid/', new_raid)
        return f'You started a new raid fund with {amount} points ({1000 - amount} remaining to start)'


def start_raid():
    raid = fb.get('/raid', None)
