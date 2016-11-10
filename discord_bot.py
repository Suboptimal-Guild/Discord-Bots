#!/usr/bin/python

import discord
import asyncio
import csv

from roster import pmd

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
        await client.send_message(message.channel, 'I\'m a fuckboy.')
    elif message.content.startswith('!x'):
        await pmd(client, message)

client.accept_invite('https://discord.gg/mM5fXCe')

client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')
