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

def random_encounter():
    enemy = choice(enemies)
    # print(enemy_name)
    encounter = enemy
    print(encounter.keys())
    return encounter

def add_to_attacked(discord_id):
    encounters = fb.get('/encounters', None)
    encounters_list = list(encounters.keys())
    encounter_key = encounters_list[0]
    encounter = encounters[encounter_key]
    if 'attacked' in encounter:
        print(type(encounter['attacked']))
        encounter['attacked'].append(discord_id)
    else:
        encounter['attacked'] = [discord_id]
    fb.patch(f'/encounters/{encounter_key}', encounter)

def attack_enemy(discord_id):
    encounters = fb.get('/encounters', None)
    print(encounters)
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
                weapon_text = '(+10 from Nightmare Sword)'
            message = f"You rolled {attack} {weapon_text} and defeated {encounter['name']}! You get {reward} points."
            add_to_attacked(discord_id)
            return message
        else:
            message = f"You rolled {attack} and lost to {encounter['name']}. You get nothing."
            add_to_attacked(discord_id)
            return message
      else:
        return f"You've already attacked {encounters_list[0]}"
    else:
        return "There's no encounter right now!"

# def attack_success(discord_id):

def end_encounter(client):
    client.close()

def get_reward(health):
    base = health * 2
    modifier = choice(range(-20, 20))
    return base + modifier

if __name__ == '__main__':
    # random_encounter()
    # attack('nothing')
    # print(attack_enemy('GreatBearShark'))
    add_to_attacked('GreatBearShark')