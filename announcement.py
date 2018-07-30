import os
import discord
import asyncio
import time
from combat_system import random_encounter
from firebase import firebase

client = discord.Client()


@client.event
async def on_ready():
    print('Sending Announcement')
    channels = client.get_all_channels()
    for channel in channels:
        if channel.name == 'general':
            message = '@here Weak Mortals, A New Item Has Appeared In The Shop'
            await client.send_message(channel, message)
            client.close()

client.run(os.getenv('DISCORD_TOKEN'))
