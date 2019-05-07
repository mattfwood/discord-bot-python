import os
import discord
import commands
from raven import Client
from show_commands import show_commands

raven_client = Client(
    'https://3a4591b085414cf4853854b0dd92348a:21dead98a66e405494a4cb328f530c00@sentry.io/1250949'
)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    try:
        # prevent bot from replying to self
        if message.author == client.user:
            return

        # only handle non-blank messages that start with the command symbol
        if len(message.content) == 0 or message.content[0] !== '!':
            return

        message_sender = message.author
        print(f'Received Message From {message_sender}:')
        print(message.content)
        # get command name
        command = message.content.split(' ')[0][1:] or ''

        if len(command) is 1 or len(command.strip('!')) is 0:
            return

        # get text after command
        text = message.content.split(command)[1].strip() or ''

        # Check if user is asking for command list
        # (to avoid cyclical dependencies)
        print(f'COMMAND: {command}')
        if command == 'commands':
            print('SHOWING COMMANDS')
            reply = show_commands()
            await client.send_message(message.channel, reply)

        # get method to be called based on command
        method = getattr(commands, command)

        # if valid method provided
        if method:
            # call command with message content
            reply = f'<@{message.author.id}> ' + method(text, message=message)

            print('Replying with:')
            print(reply)

            # reply with command response
            await client.send_message(message.channel, reply)
    except Exception as e:
        print('EXCEPTION:')
        print(repr(e))
        # Catch errors that are invalid commands
        if command not in commands.__dict__ and command is not 'commands':
            reply = f"<@{message.author.id}> '{command}' isn't a command, dummy"
            await client.send_message(message.channel, reply)
        else:
            # Otherwise report real errors
            raven_client.captureException()


client.run(os.getenv('DISCORD_TOKEN'))
