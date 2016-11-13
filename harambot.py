#!/usr/bin/python

import discord
import asyncio
import csv


#TODO: ensure proper controls when calling commands, i.e. only certain ranks can invoke certain commands

from commands import print_me_daddy as pmd
from commands import add_to_roster as atr
from commands import remove_from_roster as rfr
from commands import get_armory_link as gal
from commands import get_char_name as gcn
from commands import get_own_name as gon
from commands import get_character as getchar
from commands import showhelp


# sheets interface
#from google_sheets_interface import get_main_character_name as gmcn

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

    ### check is
    ### if <desired role> in message.author.roles

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
    elif message.content.startswith('!whois'):
        await gcn(client, message)
    elif message.content.startswith('!whoami'):
        await gon(client, message)
    elif message.content.startswith('!chars'):
        await getchar(client, message)
    elif message.content.startswith('!help'):
        await showhelp(client, message)
    elif message.content.startswith('!epgp'):
        pass # do nothing yet
    elif message.content.startswith('!bis'):
        pass # do nothing yet
    elif message.content.startswith('!audit'):
        pass # do nothing yet
    elif message.content.startswith('!logs'):
        pass # do nothing yet

client.accept_invite('https://discord.gg/mM5fXCe')

client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')
