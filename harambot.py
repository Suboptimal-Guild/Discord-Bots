#!/usr/bin/python

import discord
import asyncio
import csv
from random import randint


#TODO: ensure proper controls when calling commands, i.e. only certain ranks can invoke certain commands

from commands import print_me_daddy as pmd
from commands import add_to_roster as atr
from commands import remove_from_roster as rfr
from commands import get_armory_link as gal
from commands import get_char_name as gcn
from commands import get_own_name as gon
from commands import get_character as getchar
from commands import showhelp
from commands import get_help_string

# constants
MIDDLE_FINGER_GORILLA_URL = "http://3.bp.blogspot.com/-s3eobLzuVm0/Twxkz6yOe_I/AAAAAAAACHg/wxDw-nWa_eU/s1600/Funny+Gorilla5.jpg"
SHOCKED_MONKEY_URL = "https://s-media-cache-ak0.pinimg.com/736x/86/53/41/8653410a1ee96e3ac9bb22b4ed08c556.jpg"
LAUGHING_GORILLA_URL = "https://tigerlilytoph.files.wordpress.com/2012/01/laughing-gorilla.jpg"
LAUGHING_GORILLA_URL2 = "http://www.onlygod365.com/wp-content/uploads/2013/02/LaughingGorilla1.jpg"
LAUGHING_GORILLA_URL3 = "http://static.squarespace.com/static/51806e5ae4b0809658b411ef/t/51bd2aa9e4b0cc528082c718/1371351722080/HAHA-Gorilla.jpg?format=500w"
LAUGHING_GORILLA_URL4 = "http://myfunnypics.org/main.php?g2_view=core.DownloadItem&g2_itemId=736&g2_serialNumber=2"
LAUGHING_GORILLA_URL5 = "http://www.zooborns.com/.a/6a010535647bf3970b01310f6b78be970c-600wi"
LAUGHING_GORILLA_URL6 = "https://pbs.twimg.com/media/CIWeyDEUwAAs_AO.jpg"
LOVE_GORILLA_URL = "https://arigorillatrekking.files.wordpress.com/2014/02/gorilal-love.jpg"
THUMBS_UP_GORILLA = "http://gorillaloveproject.org/files/files/gorilla.jpg"

HARAMBOT = "Harambot 🍌"

LAUGHING_GORILLAS = [LAUGHING_GORILLA_URL, LAUGHING_GORILLA_URL2, LAUGHING_GORILLA_URL3, LAUGHING_GORILLA_URL4, LAUGHING_GORILLA_URL5, LAUGHING_GORILLA_URL6]

# sheets interface
#from google_sheets_interface import get_main_character_name as gmcn

client = discord.Client()

'''LIST OF ALL THINGS TO ADD:
'''
#TODO: raid announcements 30 min prior to raid time starting
#TODO: drag everyone into raid channel when raid starts

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message): # placeholder "bookmarks"
    # also we want to post messages in the channe lwhere the user asked, but if possible make the message only viewable to them kinda like the default bot can do
    if message.author.name == HARAMBOT:
        pass
    elif message.content.startswith('!test'):
        await client.send_message(message.channel, 'I\'m a fuckboy.')
    elif message.content.startswith('!roster status'):
        await pmd(client, message)
    elif message.content.startswith('!roster add') and is_officer(message.author): # officers only
        await atr(client, message)
    elif message.content.startswith('!roster remove') and is_officer(message.author): # officers only
        await rfr(client, message)
    elif message.content.startswith('!armory'):
        await gal(client, message)
    elif message.content.startswith('!whois'):
        await gcn(client, message)
    elif message.content.startswith('!whoami'):
        await gon(client, message)
    elif message.content.startswith('!chars'):
        await getchar(client, message)
    elif message.content == '!help':
        #await client.send_message(message.channel, get_help_string())
        await showhelp(client, message) #TODO: fix this shit? getting error code 400
    elif message.content.startswith('!epgp'):
        pass # do nothing yet
    elif message.content.startswith('!bis'):
        pass # do nothing yet
    elif message.content.startswith('!audit') and is_officer(message.author): #officers only (unless maybe people wanna run the audit on themselves?)
        pass # do nothing yet
    elif message.content.startswith('!logslink'):
        pass # do nothing yet
    elif message.content.startswith('!logspage'):
        pass # do nothing yet
    elif "banana" in message.content.lower():
        await client.send_message(message.channel, SHOCKED_MONKEY_URL + "\n... I love bananas. + 100 EP")
    elif "joke" in message.content.lower():
        await tell_joke(client, message)
    elif "love" in message.content.lower() and "harambot" in message.content.lower():
        await client.send_message(message.channel, "\n:monkey_face: + 50 EP I love you too, " + message.author.name + ". :monkey_face:\n" + LOVE_GORILLA_URL)
    elif "fuck" in message.content.lower() and "harambot" in message.content.lower():
        await client.send_message(message.channel, MIDDLE_FINGER_GORILLA_URL + "\n:monkey: - 50 EP :monkey:")
    #TODO: doesnt reconize tagging him, weird
    elif "harambot" in message.content.lower():
        await client.send_message(message.channel, ":banana: :monkey_face: Greetings, " + message.author.name + ". :banana:")

def is_officer(member):
    return is_member_of_role(member, "Officers") or is_member_of_role(member, "Starlord")

def is_member_of_role(member, role_name):
    for role in member.roles:
        if role_name == role.name:
            return True
    return False

async def tell_joke(client, message):
    rand = randint(0,len(JOKE_QUESTIONS)-1)
    await client.send_message(message.channel, ":monkey: " + JOKE_QUESTIONS[rand] + " :monkey:") # need random number

    def add_check(msg):
        return msg.content == JOKE_ANSWERS[rand]

    msg = await client.wait_for_message(timeout=5, author=message.author, check=add_check)

    if msg is None:
        await client.send_message(message.channel, ":monkey_face: " + JOKE_ANSWERS[rand] + " :monkey_face:\n\n" + LAUGHING_GORILLAS[randint(0,len(LAUGHING_GORILLAS)-1)])
    elif msg.content == JOKE_ANSWERS[rand]:
        await client.send_message(message.channel, ":banana: Correct! + 50 EP, " + message.author.name + " :banana:\n\n" + THUMBS_UP_GORILLA)

JOKE_QUESTIONS = ["What do you call an angry monkey?",
"What do you call a monkey that sells potato chips?",
"Where do monkeys go to drink?",
"Why do monkeys like bananas?",
"Where should a monkey go when he loses his tail?",
"Why should you never fight with a monkey?",
"Where do chimps get their gossip?",
"What do you call a baby monkey?"]

JOKE_ANSWERS = ["Furious George.",
"A chipmunk.",
"The monkey bars.",
"Because they have appeal.",
"To a retailer!",
"There use gorilla warfare.",
"Through the ape vine.",
"A chimp off the old block."]

client.accept_invite('https://discord.gg/NyYKejv')

client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')
