from firebase import firebase
from point_system import update_points
fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def add_point_task():
    """
    Every 10 minutes, check all users who have
    point incrementing items and give them that many points
    """
    players = fb.get('/players', None)
    for key, player in players.items():
        if 'Point Machine' in player['items']:
            print(player['items']['Point Machine'])
            point_amount = player['items']['Point Machine'] * 2
            print(f"Giving {point_amount} points to {player['discord_id']}")
            new_total = player['points'] + point_amount
            update_points(player, new_total)

    pass


if __name__ == '__main__':
    add_point_task()
