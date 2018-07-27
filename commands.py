import pprint
import random
import requests
import pdb
import json
from time import time
from point_system import add_point, flip_coin

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
    items = [{
        'name': 'Big Boy Belt',
        'description': 'Prevents you from going under 10 points',
        'cost': 50
    },
        'name': 'Good Boy Point Machine',
        'description': 'Generates one good boy point per minute',
        'cost': 100
    }]
    item_list = []
    for item in items:
        item_entry = f'{item[' cost ']} - {item[' name ']}: {item[' description ']}'
        item_list.append(item_entry)
    return '\n'.join(item_list)


def zalgo(input, message):
    return 'Ḫ̨̢͎̭̹̼E̷̗̞͟ ̶̧͚̼̥͙̪͝C͟҉̹̠O̧͎͍͈̺͟͜ͅM̦͡E̥̱̖͔̮̩S̷̝̙͚̼͍̜͘'
