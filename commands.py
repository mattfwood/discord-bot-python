import pprint
import random
import requests
import pdb
import json
from time import time
from point_system import add_point

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas


def decide(message, author):
    winner = random.choice(message.split(','))
    return winner.strip()

# get a random item from the top 20 items on a subreddit
def subreddit(name, author):
    res = requests.get(
        'https://www.reddit.com/r/{}/hot.json?limit=20'.format(name),
        headers={'User-agent': 'Bone-Bot-Discord'})
    json = res.json()
    random_url = random.choice(json['data']['children'])['data']['url']
    return random_url


def goodboypoint(name, author):
    message = add_point(name)
    return message