import os
import discord
import asyncio
import time
from combat_system import random_encounter

client = discord.Client()


def make_announcement(message, channel_name='general'):
    try:

        @client.event
        async def on_ready():
            print('Sending Announcement')
            channels = client.get_all_channels()
            for channel in channels:
                if channel.name == channel_name:
                    await client.send_message(channel, message)
                    client.close()
                    print('Closing Client...')
                    return

        client.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    make_announcement(
        '@everyone New items have appeared in the shop...', channel_name='general'
    )
