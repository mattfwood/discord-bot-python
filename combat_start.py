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
    enemy = random_encounter()
    message = f"{enemy['name']} appears! ({enemy['health']} attack)"
    channels = client.get_all_channels()
    print(channels)
    for channel in channels:
        if channel.name == 'combat':
            await client.send_message(channel, message)
            await client.send_message(channel, 'Use `!attack` to try and roll higher than the enemy.')
            encounter = enemy
            encounter['started_at'] = start_time
            encounter['attacked'] = []
            await fb.patch(f'/encounters/{enemy["name"]}', encounter)
            # wait 10 minutes
            time.sleep(600)
            await client.send_message(channel, f"{enemy['name']} ran away!")
            await fb.delete(f'/encounters/{enemy["name"]}', encounter)
            client.close()

client.run(os.getenv('DISCORD_TOKEN'))