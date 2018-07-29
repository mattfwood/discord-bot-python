import random
import requests
import json
from time import time
from point_system import add_point, flip_coin, find_player
from item_system import items, buy_item
from combat_system import attack_enemy



def decide(input: str, message) -> str:
    """`[List of Options]` Pick a random item from a list, separated by commas"""
    winner = random.choice(input.split(','))
    return winner.strip()


def reddit(input, message):
    """`{Subreddit Name}` Get a random item from the top 20 items on a subreddit"""
    try:
        res = requests.get(
            f'https://www.reddit.com/r/{input}/hot.json?limit=20',
            headers={'User-agent': 'Bone-Bot-Discord'})
        json = res.json()
        random_url = random.choice(json['data']['children'])['data']['url']
        return random_url
    except IndexError:
        return 'Subreddit not found'


def inventory(input, message):
    """List the items in your inventory"""
    print('Getting inventory...')
    player = find_player(message.author.name)
    # player = find_player('GreatBearShark')
    player_items = player['items']
    item_list = []
    for item in player_items:
        item_list.append(f"__{item['name'].strip()}__: {player_items[item['name']]}")

    # player_items = ', '.join(player['items'])
    # print(player_items)
    output = '\n'.join(item_list)
    return f"**Inventory:**\n{output}"


def points(input, message):
    """Get your current number of points"""
    player = find_player(message.author.name)
    return f"You have **{player['points']}** points, pal."


def goodboypoint(input, message):
    """`{Discord Name}` Give one point to a person of your choice"""
    for member in message.mentions:
        message = add_point(member.name)
        return message


def gbp(input, message):
    """Shorthand for !goodboypoint"""
    return goodboypoint(input, message)


def bet(input, message):
    """`{Bet Amount}` Place a 50/50 bet with a certain number of points"""
    try:
        amount = int(input)
        message = flip_coin(amount, message.author.name)
        return message
    except ValueError:
        return "what the"


def store(input, message):
    """List all the items available in the store"""
    item_list = []
    for item in items:
        item_entry = f"**{item['name']}:** {item['price']} - *{item['description']}*"
        item_list.append(item_entry)
    return '\n'.join(item_list)


def buy(input, message):
    """`{Item Name}` Buy an item by name from the store. Use !store to see items"""
    message = buy_item(message.author.name, input)
    return message

def attack(input, message):
    """Attack the current enemy if an encounter is active"""
    message = attack_enemy(message.author.name)
    return message

def zalgo(input, message):
    """Uh oh"""
    return 'Ḫ̨̢͎̭̹̼E̷̗̞͟ ̶̧͚̼̥͙̪͝C͟҉̹̠O̧͎͍͈̺͟͜ͅM̦͡E̥̱̖͔̮̩S̷̝̙͚̼͍̜͘'


if __name__ == "__main__":
    # inventory('beep', 'boop')
