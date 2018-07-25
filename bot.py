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

    # only handle messages that start with the command symbol
    if message.content[0] != '!':
        return

    print('Received Message From {}:'.format(message.author))
    print(message.content)
    # get command name
    command = message.content.split(' ')[0][1:]

    # get text after command
    text = message.content.split(command)[1].strip()

    try:
        # get method to be called based on command
        method = getattr(commands, command)

        # if valid method provided
        if method:
            # call command with message content
            reply = method(text, author=message.author)

            print('Replying with:')
            print(reply)

            # reply with command response
            await client.send_message(message.channel, reply)
    except AttributeError:
        reply = "'{}' isn't a command, dummy".format(command)
        await client.send_message(message.channel, reply)
        pass

client.run(os.getenv('DISCORD_TOKEN'))


# input = "!decide one, two, three"

# # get command name
# command = input.split(' ')[0].replace('!', '')

# # get text after command
# message = input.split(command)[1].strip()
# print(commands.decide(message))
