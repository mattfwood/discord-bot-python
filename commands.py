import pprint
import random
import requests
import pdb

pp = pprint.PrettyPrinter(indent=4, depth=2)

# pick a random item from a list, separated by commas
def decide(message):
  winner = random.choice(message.split(','))
  return winner.strip()

def wholesome():
  res = requests.get('https://www.reddit.com/r/wholesomeMemes/hot.json?limit=100')
  pdb.set_trace()
  pp.pprint(res.json()['data'])
  # print(random.choice(res.json()['children']).data.url)
  # return random.choice(res.json()['children']).data.url