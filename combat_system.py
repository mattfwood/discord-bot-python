from random import choice
from firebase import firebase
from point_system import update_points, find_player

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)

enemies = [
    {
        'name': 'Giant Gabagool',
        'health': 93,
    },
    {
        'name': 'Johnny Two Times',
        'health': 22,
    },
    {
        'name': 'Pineapple Bee Monster',
        'health': 71,
    },
    {
        'name': 'Big Clown',
        'health': 48,
    },
    {
        'name': 'Peanut Pete',
        'health': 81
    },
    {
        'name': 'Emotionally Unavailable Eddy',
        'health': 99
    },
    {
        'name': 'Big Bad Boy',
        'health': 55
    },
    {
        'name': 'Ultra Edison',
        'health': 89
    },
    {
        'name': 'Meatball Marinara',
        'health': 64
    }
]


def random_encounter() -> dict:
    encounter = choice(enemies)
    return encounter


def add_to_attacked(discord_id: str, boss=False, amount=None):
    if boss:
        boss = fb.get('/boss', None)
        if 'attacked' in boss:
            boss['attacked'][discord_id] = amount
        else:
            boss['attacked'] = {discord_id: amount}

        fb.patch(f'/boss/', boss)
    else:
        encounters = fb.get('/encounters', None)
        encounters_list = list(encounters.keys())
        encounter_key = encounters_list[0]
        encounter = encounters[encounter_key]
        if 'attacked' in encounter:
            print(type(encounter['attacked']))
            encounter['attacked'][discord_id]
        else:
            encounter['attacked'] = {discord_id: amount or 0}
        fb.patch(f'/encounters/{encounter_key}', encounter)


def attack_enemy(discord_id: str) -> str:
    encounters = fb.get('/encounters', None)
    encounters_list = list(encounters.keys())
    # Check if there's an encounter
    if len(encounters_list) != 0:
        encounter = encounters[encounters_list[0]]

        # Check if this person has already attacked or if no one has attacked
        if 'attacked' not in encounter or discord_id not in encounter['attacked']:
            attack = choice(range(1, 100))
            player = find_player(discord_id)
            # If player has sword
            if 'Nightmare Sword' in player['items']:
                # Add 10 to attack
                attack += 10
            if attack > encounter['health']:
                # Calculate reward based on enemy health
                reward = get_reward(encounter['health'])
                # Find player and update points
                new_total = player['points'] + reward
                update_points(player, new_total)
                weapon_text = ''
                # Conditionally add text if player has weapon
                if 'Nightmare Sword' in player['items']:
                    weapon_text = ' (+10 from Nightmare Sword) '
                message = f"You rolled **{attack}**{weapon_text}and defeated **{encounter['name']}**! You get **{reward}** points."
                add_to_attacked(discord_id)
                return message
            else:
                # Try again if they have second sword
                if 'Second Sword' in player['items']:
                    second_attack = choice(range(1, 100))
                    if 'Nightmare Sword' in player['items']:
                        # Add 10 to attack
                        second_attack += 10
                        if second_attack > encounter['health']:
                            reward = get_reward(encounter['health'])
                            new_total = player['points'] + reward
                            update_points(player, new_total)
                            weapon_text = ''
                            # Conditionally add text if player has weapon
                            if 'Nightmare Sword' in player['items']:
                                weapon_text = ' (+10 from Nightmare Sword) '
                            message = f"Your first attack of **{attack}** failed, but on your second attack you rolled **{second_attack}**{weapon_text}and defeated **{encounter['name']}**! You get **{reward}** points."
                            add_to_attacked(discord_id)
                            return message

                # Otherwise resolve fight as a loss
                weapon_text = ''
                if 'Nightmare Sword' in player['items']:
                    weapon_text = ' (+10 from Nightmare Sword) '
                message = f"You rolled **{attack}**{weapon_text}and lost to **{encounter['name']}**. You get *nothing*."
                add_to_attacked(discord_id)
                return message
        else:
            return f"You've already attacked {encounters_list[0]}"
    else:
        return "There's no encounter right now!"


def attack_boss(discord_id: str) -> str:
    boss = fb.get('/boss', None)
    # Check if there's a boss
    if boss:
        # Make sure user hasn't attacked
        if 'attacked' not in boss or discord_id not in boss['attacked']:
            player = find_player(discord_id)
            # Generate normal attack
            attack = choice(range(1, 100))

            # Add modifiers
            if 'Nightmare Sword' in player['items']:
                # Add 10 to attack
                attack += 10

            add_to_attacked(discord_id, boss=True, amount=attack)
            return f'{discord_id} attacked for {attack}'
        else:
            return "You've already attacked this boss!"


def get_reward(health: int) -> int:
    base = health * 2
    modifier = choice(range(-20, 20))
    return base + modifier


if __name__ == '__main__':
    # random_encounter()
    # attack('nothing')
    # print(attack_enemy('GreatBearShark'))
    # add_to_attacked('GreatBearShark', 50)
    # print(attack_boss('GreatBearShark'))
    boss = fb.get('/boss', None)
    for player, attack in boss['attacked'].items():
        print((player, attack))
