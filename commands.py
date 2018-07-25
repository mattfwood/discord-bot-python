import pprint
import random
import requests
import pdb
import json
from time import time
from point_system import add_point, flip_coin

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas


def decide(input, message):
    winner = random.choice(input.split(','))
    return winner.strip()

# get a random item from the top 20 items on a subreddit
def subreddit(input, message):
    res = requests.get(
        'https://www.reddit.com/r/{}/hot.json?limit=20'.format(input),
        headers={'User-agent': 'Bone-Bot-Discord'})
    json = res.json()
    random_url = random.choice(json['data']['children'])['data']['url']
    return random_url


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


# print(bet(7, '@kiss me through the BONE'))
