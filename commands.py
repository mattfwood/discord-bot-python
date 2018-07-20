import pprint
import random
import requests
import pdb

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas
def decide(message):
    winner = random.choice(message.split(','))
    return winner.strip()

# get a random item from the top 20 items on a subreddit
def subreddit(name):
    res = requests.get(
        'https://www.reddit.com/r/{}/hot.json?limit=20'.format(name))
    pp.pprint(res.json())


def wholesome():
    res = requests.get(
        'https://www.reddit.com/r/wholesomeMemes/hot.json?limit=20')
    pp.pprint(res.json())
    # print(random.choice(res.json()['children']).data.url)
    # return random.choice(res.json()['children']).data.url
