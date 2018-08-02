from firebase import firebase
from point_system import update_points
from announcement import make_announcement
fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def add_point_task():
    """
    Every 10 minutes, check all users who have
    point incrementing items and give them that many points
    """
    players = fb.get('/players', None)
    point_announcement = []
    for key, player in players.items():
        if 'Point Machine' in player['items']:
            print(player['items']['Point Machine'])
            point_amount = player['items']['Point Machine'] * 2
            player_message = f"Giving {point_amount} points to <@{player['discord_id']}>"
            print(player_message)
            point_announcement.append(player_message)
            new_total = player['points'] + point_amount
            update_points(player, new_total)
    return '\n'.join(point_announcement)


if __name__ == '__main__':
    message = add_point_task()
    make_announcement(message, channel_name='point-machines')
