import random
import requests
import json
from time import time
from point_system import add_point, flip_coin, find_player, bet_total
from item_system import items, buy_item
from combat_system import attack_enemy, attack_boss


def decide(user_input: str, message) -> str:
    """`[List of Options]` Pick a random item from a list, separated by commas"""
    winner = random.choice(user_input.split(','))
    return winner.strip()


def reddit(user_input, message):
    """`{Subreddit Name}` Get a random item from the top 20 items on a subreddit"""
    try:
        res = requests.get(
            f'https://www.reddit.com/r/{user_input}/hot.json?limit=20',
            headers={'User-agent': 'Bone-Bot-Discord'})
        json = res.json()
        random_url = random.choice(json['data']['children'])['data']['url']
        return random_url
    except IndexError:
        return 'Subreddit not found'


def inventory(user_input, message) -> str:
    """List the items in your inventory"""
    player = find_player(message.author.id)
    # player = find_player('GreatBearShark')
    player_items = player['items']
    item_list = []
    for item in player_items:
        # print(item)
        item_list.append(
            f"__{item.strip()}__: {player_items[item]}")

    output = '\n'.join(item_list)
    return f"**\n Inventory:**\n{output}"


def points(user_input, message) -> str:
    """Get your current number of points"""
    player = find_player(message.author.id)
    return f"You have **{player['points']}** points."


def goodboypoint(user_input, message) -> str:
    """`{Discord Name}` Give one point to a person of your choice"""
    for member in message.mentions:
        message = add_point(member.id)
        return message


def gbp(user_input, message):
    """Shorthand for !goodboypoint"""
    return goodboypoint(user_input, message)


def bet(user_input: str, message) -> str:
    """`{Bet Amount}` Place a 50/50 bet with a certain number of points"""
    try:
        amount = int(user_input)
        message = flip_coin(amount, message.author.id)
        return message
    except ValueError:
        print('VALUE ERROR:')
        print(user_input)
        if user_input == 'all':
            return bet_total(message.author.id)
        elif user_input == 'half':
            return bet_total(message.author.id, half=True)
        else:
            return "what the"


def store(user_input, message):
    """List all the items available in the store"""
    item_list = []
    for item in items:
        item_entry = f"**{item['name']}:** {item['price']} - *{item['description']}*"
        item_list.append(item_entry)
    return '\n'.join(item_list)


def buy(user_input, message) -> str:
    """`{Item Name}` Buy an item by name from the store. Use !store to see items"""
    message = buy_item(message.author.id, user_input)
    return message


def attack(user_input, message) -> str:
    """Attack the current enemy if an encounter is active"""
    message = attack_enemy(message.author.id)
    return message


def fight(user_input, message) -> str:
    """Attack the current boss if a boss encounter is active"""
    message = attack_boss(message.author.id)
    return message


def zalgo(user_input, message) -> str:
    """Uh oh"""
    return 'Ḫ̨̢͎̭̹̼E̷̗̞͟ ̶̧͚̼̥͙̪͝C͟҉̹̠O̧͎͍͈̺͟͜ͅM̦͡E̥̱̖͔̮̩S̷̝̙͚̼͍̜͘'


if __name__ == "__main__":
    # inventory('beep', 'boop')
    print(bet('all', 'message'))
