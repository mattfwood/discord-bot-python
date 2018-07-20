import pprint
import random
import requests
import pdb
import json
from time import time

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas


def decide(message):
    winner = random.choice(message.split(','))
    return winner.strip()

# get a random item from the top 20 items on a subreddit


def subreddit(name):
    res = requests.get(
        'https://www.reddit.com/r/{}/hot.json?limit=20'.format(name),
        headers={'User-agent': 'Bone-Bot-Discord'})
    json = res.json()
    random_url = random.choice(json['data']['children'])['data']['url']
    return random_url


def goodboypoint(name):
    player = name.lower()
    json_data = open('./score.json').read()
    score = json.loads(json_data)
    current_minutes = (time() / 60)

    if player in score:
        # check that user has a last_updated field
        last_updated = score[player]['last_updated']
        time_diff = int(current_minutes - last_updated)
        # if it's been 60 minutes since last good boy point
        if time_diff > 60:
            # give them a point
            score[player]['points'] += 1
            score[player]['last_updated'] = current_minutes
        else:
            print("It's too soon to give another good boy point to {}! ({} minutes left)".format(
                player, (60 - time_diff)))
            return "It's too soon to give another good boy point to {}! ({} minutes left)".format(player, (60 - time_diff))
    else:
        score[player] = {"points": 1, "last_updated": current_minutes}

    with open('./score.json', 'w') as output:
        json.dump(score, output)

    message = 'You gave {} one good boy point! Now they have {}.'.format(
        player, score[player]['points'])

    return message
