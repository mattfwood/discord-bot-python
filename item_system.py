from point_system import find_player
from firebase import firebase
fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)

items = [
    {
        'name': 'Good Boy Belt',
        'description': 'Prevents you from going under 10 points',
        'price': 50
    },
    {
        'name': 'Point Machine',
        'description': 'Generates one good boy point every 10 minutes',
        'price': 100
    },
    {
        'name': 'Nightmare Sword',
        'description': 'Get +10 damage to your rolls. Made from real nightmares.',
        'price': 1000
    },
    {
        'name': 'Skateboard',
        'description': 'Holy shit',
        'price': 5000
    }
]

items_dict = {
    'Good Boy Belt': {
        'description': 'Prevents you from going under 10 points',
        'price': 50
    },
    'Point Machine': {
        'description': 'Generates one good boy point per minute',
        'price': 100
    }
}


def validate_item(item_name):
    for item in items:
        if item['name'].lower() == item_name:
            return item

    return False


def buy_item(discord_id, item_name):
    item_name_lowercase = item_name.lower()
    # Check if item name is valid
    item = validate_item(item_name_lowercase)

    if item:
        # Check that user has enough points
        player = find_player(discord_id)
        if player['points'] >= item['price']:
            # Buy item
            print('BUY ITEM')
            # add item to inventory
            if 'items' in player:
                # if the player already has this item
                if item['name'] in player['items']:
                    # add one quantity
                    item_name = item['name']
                    player['items'][item['name']] += 1
                else:
                    # otherwise set it to 1
                    player['items'][item['name']] = 1
                # player['items'].append(item['name'])
            else:
                player['items'] = [item['name']]
            # deduct price from points
            player['points'] -= item['price']
            # update user
            fb.patch(f"/players/{player['discord_id']}", player)
            return f"You bought a {item_name}! Now you have {player['points']} point(s)."
        else:
            return f"You can't afford {item_name} ({item['price']} points)!. You only have {player['points']}"
    else:
        return f"{item_name} isn't an item!"


if __name__ == "__main__":
    print(buy_item('GreatBearShark', 'Point Machine'))
