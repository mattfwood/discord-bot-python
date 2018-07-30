import os
import discord
import asyncio
import time
from combat_system import random_encounter, get_reward
from firebase import firebase
from raven import Client

fb = firebase.FirebaseApplication(
    'https://discord-bot-db.firebaseio.com', None)

client = discord.Client()
start_time = time.time()


@client.event
async def on_ready():
    print('Starting Combat Event')
    # Reset all previous counters to be safe
    enemy = random_encounter()
    fb.delete(f'/boss', None)
    message = f"{enemy['name']} appears!"
    channels = client.get_all_channels()
    print(channels)
    for channel in channels:
        if channel.name == 'combat':
            await client.send_message(channel, message)
            await client.send_message(channel, 'Use `!fight` to try and roll the highest attack against the enemy for the next 5 minutes.')
            encounter = enemy
            encounter['started_at'] = start_time
            encounter['attacked'] = []
            fb.patch(f'/boss', encounter)
            # wait 5 minutes
            await asyncio.sleep(300)

            boss = fb.get('/boss', None)

            highest_attack = max(boss['attacked'].values())
            for player, attack in boss['attacked'].items():
                if attack is highest_attack:
                    winner = player
                    reward = get_reward(boss['health']) * 2
                    await client.send_message(channel, f"{winner} wins the boss fight with a score of {attack}! {winner} wins **{reward}** points!")
                    client.close()
                    return

client.run(os.getenv('DISCORD_TOKEN'))
