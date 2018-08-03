import string
from point_system import find_player
from player import Player

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
        'name': 'Loaded Dice',
        'description': "Gives you a +10% chance to win bets",
        'price': 500,
    },
    {
        'name': 'Tortellini Armor',
        'description': 'Made from tender tortellini children',
        'price': 5000,
    },
    {
        'name': 'Nightmare Sword',
        'description': 'Get +10 damage to your rolls. Made from real nightmares.',
        'price': 1000
    },
    {
        'name': 'Second Sword',
        'description': 'Get two attempts when attacking a boss.',
        'price': 2500
    },
    {
        'name': 'Skateboard',
        'description': 'Holy shit',
        'price': 5000
    },
    {
        'name': 'Plate of Spaghetti',
        'description': "Your One Weakness.",
        'price': 10000
    }
]


def validate_item(item_name: str):
    for item in items:
        if item['name'].lower() == item_name:
            return item

    return False


def has_digit(input: str) -> bool:
    return any(char.isdigit() for char in input)


def get_quantity(input: str) -> int:
    return int(input.strip(string.ascii_letters + ' '))


def get_name(input: str) -> str:
    return input.strip(string.digits + ' ')


def buy_item(discord_id: str, item_name: str) -> str:
    quantity = 1
    # If the item name has a digit, they want more than one
    if has_digit(item_name):
        quantity = get_quantity(item_name)
        item_name = get_name(item_name)

    item_name_lowercase = item_name.lower()
    # Check if item name is valid
    item = validate_item(item_name_lowercase)
    item_name = item['name']

    if item:
        # Check that user has enough points
        # player = find_player(discord_id)
        player = Player(discord_id)
        if player.points >= (item['price'] * quantity):
            # add item to inventory
            if 'items' in vars(player):
                # if the player already has this item
                if item['name'] in player.items:
                    # add one quantity
                    item_name = item_name
                    player.items[item_name] += quantity
                else:
                    # otherwise set it to 1
                    player.items[item_name] = quantity
            else:
                player.items = {item_name: quantity}
            # deduct price from points for each one bought
            player.points -= item['price'] * quantity
            # update user
            player.update_player()
            return f"You bought {quantity} {item_name}(s)! Now you have {player.points} point(s)."
        else:
            return f"You can't afford {item_name} ({item['price']} points)!. You only have {player.points}"
    else:
        return f"{item_name} isn't an item!"


if __name__ == "__main__":
    print(buy_item('200702104568987649', 'Point Machine 2'))
