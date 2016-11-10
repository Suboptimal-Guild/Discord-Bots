#!/usr/bin/python

import discord
import asyncio
import csv


#TODO: ensure proper controls when calling commands, i.e. only certain ranks can invoke certain commands

from roster import print_me_daddy as pmd
from roster import add_to_roster as atr
from roster import remove_from_roster as rfr
from roster import get_armory_link as gal


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message): # placeholder "bookmarks"
    ### COMMANDS INVOKABLE BY EVERYONE ###

    ### COMMANDS INVOKABLE BY OFFICERS ###
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'I\'m a fuckboy.')
    elif message.content.startswith('!roster status'):
        await pmd(client, message)
    elif message.content.startswith('!roster add'):
        await atr(client, message)
    elif message.content.startswith('!roster remove'):
        await rfr(client, message)
    elif message.content.startswith('!armory'):
        await gal(client, message)

client.accept_invite('https://discord.gg/mM5fXCe')

client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')
