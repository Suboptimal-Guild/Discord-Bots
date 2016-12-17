#!/usr/bin/python

import discord
import asyncio
import csv
from random import randint

#TODO: ensure proper controls when calling commands, i.e. only certain ranks can invoke certain commands

# Commands imports
from commands.epgp import update_EPGP
from commands.epgp import print_EPGP
from commands.epgp import print_EPGP_leaderboard
from commands.roster import print_roster as pr
from commands.commands import get_armory_link as gal
from commands.commands import get_char_name as gcn
from commands.commands import get_own_name as gon
from commands.commands import get_character as getchar
from commands.commands import showhelp
from commands.logs import get_logs_page
from commands.logs import get_logs_links
from commands.post_outs import generate_post_out
from commands.post_outs import print_attendance

# Fun imports
from fun.quote import print_quote
from fun.response import *

HARAMBOT_DEV = "MjQ5NTkwMTE3MzU2Nzk3OTUz.CxIg5A.BYYtQ1H4H3l4CuLl-YrWjI50eOk"
HARAMBOT_PRODUCTION = "MjQ2MTMxMjkyMjg5MjM2OTky.CxIzbg.ftm3bhYcnsceIm2bgLQDlx7UmOk"

# sheets interface
#from google_sheets_interface import get_main_character_name as gmcn

client = discord.Client()

'''LIST OF ALL THINGS TO ADD:
'''
#TODO: raid announcements 30 min prior to raid time starting
#TODO: drag everyone into raid channel when raid starts
#TODO: some type of alts command
#TODO: log pages for people since WL uses generated IDs unlike armory which uses character/realmname
#TODO: audit (maybe full audit for officers, individual audit of themselves for everyone?)
#TODO: bis command of some sort?
#TODO: look into EMBED object documentation in python library
#TODO: tagging by Harambot in a message??
#TODO: see todo over in commands for get_roster_string- dat shit ugly do
#TODO: add offspecs to roster status command
#TODO: addons/WA
#TODO: surveys with reactions

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message): # placeholder "bookmarks"
    # also we want to post messages in the channe lwhere the user asked, but if possible make the message only viewable to them kinda like the default bot can do
    if message.author.name == HARAMBOT or message.author.name == HARAMBOT_DEV:
        pass
    elif message.content.startswith('!test'):
        await client.send_message(message.channel, 'I\'m a fuckboy.')
    elif message.content.startswith('!roster status'):
        await pr(client, message)
    elif message.content.startswith('!armory'):
        await gal(client, message)
    elif message.content.startswith('!whois'):
        await gcn(client, message)
    elif message.content.startswith('!whoami'):
        await gon(client, message)
    elif message.content.startswith('!chars'):
        await getchar(client, message)
    elif message.content == '!help':
        await showhelp(client, message)
    elif message.content.startswith('!epgp export') and is_officer(message.author):
        await update_EPGP(client, message)
    elif message.content.startswith('!epgp leaderboard'):
        await print_EPGP_leaderboard(client, message)
    elif message.content.startswith('!epgp'):
        await print_EPGP(client, message)
    elif message.content.startswith('!bis'):
        pass # do nothing yet
    elif message.content.startswith('!audit') and is_officer(message.author): #officers only (unless maybe people wanna run the audit on themselves?)
        pass # do nothing yet
    elif message.content.startswith('!logs'):
        await get_logs_links(client, message)
    elif message.content.startswith('!logspage'):
        # DOES NOT WORK, see above TODO
        await get_logs_page(client, message)
    # Post out stuff
    elif message.content.startswith('!attendance'):
        await print_attendance(client, message)
    elif message.content.startswith('!postout') or message.content.startswith('!late') or message.content.startswith('!absent'):
        await generate_post_out(client, message)
    # fun stuff
    elif message.content.lower().startswith('!chuckquote'):
        await print_quote(client, message, "chuck")
    elif message.content.lower().startswith('!peterquote') or message.content.lower().startswith('!petequote'):
        await print_quote(client, message, "peter")
    elif "banana" in message.content.lower():
        await client.send_message(message.channel, SHOCKED_MONKEY_URL + "\n... I love bananas. + 100 EP")
    elif "joke" in message.content.lower():
        await tell_joke(client, message)
    elif "love" in message.content.lower() and "harambot" in message.content.lower():
        await client.send_message(message.channel, "\n:monkey_face: + 50 EP I love you too, " + message.author.name + ". :monkey_face:\n" + LOVE_GORILLA_URL)
    elif "fuck" in message.content.lower() and "harambot" in message.content.lower():
        await client.send_message(message.channel, MIDDLE_FINGER_GORILLA_URL + "\n:monkey: - 50 EP :monkey:")
    elif "harambot" in message.content.lower() and is_message_a_greeting(message):
        await client.send_message(message.channel, ":banana: :monkey_face: Greetings, " + message.author.name + ". :banana:")
    elif "harambot" in message.content.lower() and is_message_a_thank_you(message):
        await client.send_message(message.channel, ":banana: :monkey_face: You got it, " + message.author.name + ". :banana:\n" + NO_PROBLEM_GORILLA)
    elif did_mention_harambot(client, message):
        await client.send_message(message.channel, ":monkey: You rang, " + message.author.name + "? :monkey:")
    elif "harambot" in message.content.lower():
        await client.send_message(message.channel, "Someone called?")

def is_officer(member):
    return is_member_of_role(member, "Officers") or is_member_of_role(member, "Starlord") or is_member_of_role(member, "admin")

def is_member_of_role(member, role_name):
    for role in member.roles:
        if role_name == role.name:
            return True
    return False

def main():
    client.accept_invite('https://discord.gg/NyYKejv')

    #type = input("Please specify which Harambot you would like to run (dev/prod): ")

    #while type != "dev" and type != "prod":
    #    type = input("That was not a valid input. Please specify which Harambot you would like to run (dev/prod): ")

    #if type == "dev":
    client.run("MjQ5NTkwMTE3MzU2Nzk3OTUz.CxIg5A.BYYtQ1H4H3l4CuLl-YrWjI50eOk")
    #else:
        #client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')

if __name__ == "__main__":
    main()
