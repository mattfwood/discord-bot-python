from firebase import firebase
fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)


def add_point_task(discord_id):
    """
    Every 5 minutes, check all users who have
    point incrementing items and give them that many points
    """
    players = fb.get('/players', None)
    # for player in players:

    pass
