import pprint
import random
import requests
import pdb
import json
from time import time
from point_system import add_point, flip_coin, find_player
from item_system import items, buy_item

pp = pprint.PrettyPrinter(indent=4, depth=2)


def decide(input: str, message) -> str:
    # Pick a random item from a list, separated by commas
    winner = random.choice(input.split(','))
    return winner.strip()


def reddit(input, message):
    try:
        # Get a random item from the top 20 items on a subreddit
        res = requests.get(
            f'https://www.reddit.com/r/{input}/hot.json?limit=20',
            headers={'User-agent': 'Bone-Bot-Discord'})
        json = res.json()
        random_url = random.choice(json['data']['children'])['data']['url']
        return random_url
    except IndexError:
        return 'Subreddit not found'


def inventory(input, message):
    player = find_player(message.author.name)
    items = ', '.join(player['items'])
    return f"Inventory: {items}"


def points(input, message):
    player = find_player(message.author.name)
    return f"You have {player['points']} points, pal."


def goodboypoint(input, message):
    for member in message.mentions:
        message = add_point(member.name)
        return message


def gbp(input, message):
    return goodboypoint(input, message)


def bet(input, message):
    try:
        amount = int(input)
        message = flip_coin(amount, message.author.name)
        return message
    except ValueError:
        return "what the"


def store(input, message):
    item_list = []
    for item in items:
        item_entry = f"{item['price']} - {item['name']}: {item['description']}"
        item_list.append(item_entry)
    return '\n'.join(item_list)


def buy(input, message):
    message = buy_item(message.author.name, input)
    return message


def zalgo(input, message):
    return 'Ḫ̨̢͎̭̹̼E̷̗̞͟ ̶̧͚̼̥͙̪͝C͟҉̹̠O̧͎͍͈̺͟͜ͅM̦͡E̥̱̖͔̮̩S̷̝̙͚̼͍̜͘'
