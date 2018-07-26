import os
import discord
import asyncio
import commands

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # prevent bot from replying to self
    if message.author == client.user:
        return

    # only handle non-blank messages that start with the command symbol
    if message.content[0] is not '!' or len(message.content) is 0:
        return

    message_sender = message.author
    print(f'Received Message From {message_sender}:')
    print(message.content)
    # get command name
    command = message.content.split(' ')[0][1:] or ''

    # get text after command
    text = message.content.split(command)[1].strip() or ''

    try:
        # get method to be called based on command
        method = getattr(commands, command)

        # if valid method provided
        if method:
            # call command with message content
            reply = method(text, message=message)

            print('Replying with:')
            print(reply)

            # reply with command response
            await client.send_message(message.channel, reply)
    except AttributeError:
        reply = f"'{command}' isn't a command, dummy"
        await client.send_message(message.channel, reply)
        pass

client.run(os.getenv('DISCORD_TOKEN'))
