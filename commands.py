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


def subreddit(input, message):
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
    amount = int(input)
    message = flip_coin(amount, message.author.name)
    return message


def zalgo(input, message):
    return 'Ḫ̨̢͎̭̹̼E̷̗̞͟ ̶̧͚̼̥͙̪͝C͟҉̹̠O̧͎͍͈̺͟͜ͅM̦͡E̥̱̖͔̮̩S̷̝̙͚̼͍̜͘'
