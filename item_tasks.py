from firebase_helper import fb
from point_system import update_points
from announcement import make_announcement


def add_point_task():
    """
    Every 10 minutes, check all users who have
    point incrementing items and give them that many points
    """
    players = fb.get('/players', None)
    print(players)
    point_announcement = []
    for key, player in players.items():
        if 'items' in player and 'Point Machine' in player['items']:
            point_amount = player['items']['Point Machine'] * 2
            player_message = (
                f"Giving {point_amount} points to <@{player['discord_id']}>"
            )
            point_announcement.append(player_message)
            new_total = player['points'] + point_amount
            update_points(player, new_total)
    return '\n'.join(point_announcement)


if __name__ == '__main__':
    message = add_point_task()
    make_announcement(message, channel_name='point-machines')
