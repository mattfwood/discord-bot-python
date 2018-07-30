import os
import discord
import asyncio
import time
from combat_system import random_encounter
from firebase import firebase

client = discord.Client()


def make_announcement(message, channel='general'):
    @client.event
    async def on_ready():
        print('Sending Announcement')
        channels = client.get_all_channels()
        for channel in channels:
            if channel.name == 'general':
                await client.send_message(channel, message)
                client.close()

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    make_announcement('test')
