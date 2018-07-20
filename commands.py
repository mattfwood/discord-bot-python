import pprint
import random
import requests
import pdb
import json

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

def goodBoyPoint(name):
    json_data = open('./score.json').read()
    score = json.loads(json_data)
    if name in score:
      print('NAME FOUND')
      score[name] += 1
    else:
      print('NAME NOT FOUND')
      score[name] = 0

    pp.pprint(score)
    with open('./score.json', 'w') as output:
        json.dump(score, output)

    message = 'You gave {} one good boy point! Now they have {}.'.format(name, score[name])

    return message
