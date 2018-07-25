import pprint
import random
import requests
import pdb
import json
from time import time
from point_system import add_point, flip_coin

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas


def decide(message, author):
    winner = random.choice(message.split(','))
    return winner.strip()

# get a random item from the top 20 items on a subreddit
def subreddit(message, author):
    res = requests.get(
        'https://www.reddit.com/r/{}/hot.json?limit=20'.format(message),
        headers={'User-agent': 'Bone-Bot-Discord'})
    json = res.json()
    random_url = random.choice(json['data']['children'])['data']['url']
    return random_url


def goodboypoint(message, author):
    message = add_point(message)
    return message

def bet(message, author):
    amount = int(message)
    message = flip_coin(amount, author.name)
    return message


# print(bet(7, '@kiss me through the BONE'))
