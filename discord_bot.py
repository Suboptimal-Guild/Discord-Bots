#!/usr/bin/python
'''
import discord
import asyncio

# Disables the SSL warning that is printed to the console.
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def example_func(author, message):
    client.send_message(message.channel, "%s, How are you doing?" % author)

#@client.event
def on_message(message):
    author = message.author

    if message.content.startwith('!test'):
        example_func(author, message)



password = 'MjQzMTIzNjEyNTMyMzQyNzg5.CwWINA.Asi_1i6v3MUvBQfiqg4tFD0tnWs'
ID = 'starter-pot#3689'

client.login(ID, password)

client.accept_invite('https://discord.gg/b9T4n')

client.run()
'''

import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'I\'m a fuckboy.\n Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.accept_invite('https://discord.gg/mM5fXCe')

client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')
