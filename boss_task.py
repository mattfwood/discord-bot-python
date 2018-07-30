import os
import discord
import asyncio
import time
from combat_system import random_encounter
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
            await client.send_message(channel, 'Use `!fight` to try and roll the highest attack against the enemy.')
            encounter = enemy
            encounter['started_at'] = start_time
            encounter['attacked'] = []
            fb.patch(f'/boss', encounter)
            # wait 5 minutes
            await asyncio.sleep(300)

            # Alert that the enemy ran away
            await client.send_message(channel, f"{enemy['name']} ran away!")
            # Reset Encounters
            fb.delete(f'/boss', None)
            client.close()

client.run(os.getenv('DISCORD_TOKEN'))
