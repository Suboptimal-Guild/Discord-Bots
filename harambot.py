#!/usr/bin/python

import discord
import asyncio
import csv
from random import randint

#TODO: ensure proper controls when calling commands, i.e. only certain ranks can invoke certain commands

from commands import print_roster as pr
from commands import add_to_roster as atr
from commands import remove_from_roster as rfr
from commands import get_armory_link as gal
from commands import get_char_name as gcn
from commands import get_own_name as gon
from commands import get_character as getchar
from commands import showhelp
from commands import get_logs_page
from commands import get_logs_links
from commands import update_EPGP
from commands import print_EPGP
from commands import print_EPGP_leaderboard
from commands import generate_post_out
from commands import print_attendance

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
NO_PROBLEM_GORILLA = "http://www.animalsbase.com/wp-content/uploads/2015/10/Powerful-Gorilla-Lifts-Fist-Looks-At-Photographer.jpg"

HARAMBOT_DEV = "MjQ5NTkwMTE3MzU2Nzk3OTUz.CxIg5A.BYYtQ1H4H3l4CuLl-YrWjI50eOk"
HARAMBOT_PRODUCTION = "MjQ2MTMxMjkyMjg5MjM2OTky.CxIzbg.ftm3bhYcnsceIm2bgLQDlx7UmOk"

HARAMBOT = "Harambot 🍌"
HARAMBOT_DEV = "Harambot-Dev"

LAUGHING_GORILLAS = [LAUGHING_GORILLA_URL, LAUGHING_GORILLA_URL2, LAUGHING_GORILLA_URL3, LAUGHING_GORILLA_URL4, LAUGHING_GORILLA_URL5, LAUGHING_GORILLA_URL6]

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
        await print_chuck_quote(client, message)
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

def is_message_a_greeting(message):
    msg = message.content.lower()
    if "hi" in msg or "hello" in msg or "hey" in msg or "sup " in msg or "whats up" in msg or "yo " in msg or "what's up" in msg:
        return True
    else:
        return False

def is_message_a_thank_you(message):
    msg = message.content.lower()
    if "thanks" in msg or "thank you" in msg or "thank ya" in msg or "ty" == msg or "ty " in msg or "thx" in msg:
        return True
    else:
        return False

def is_officer(member):
    return is_member_of_role(member, "Officers") or is_member_of_role(member, "Starlord") or is_member_of_role(member, "admin")

def is_member_of_role(member, role_name):
    for role in member.roles:
        if role_name == role.name:
            return True
    return False

def did_mention_harambot(client, message):
    s = ""
    for m in message.mentions:
        if m.name == HARAMBOT:
            return True
    return False


async def tell_joke(client, message):
    rand = randint(0,len(JOKE_QUESTIONS)-1)
    await client.send_message(message.channel, ":monkey: " + JOKE_QUESTIONS[rand] + " :monkey:") # need random number

    def add_check(msg):
        return msg.content in JOKE_ANSWERS[rand].lower() and len(msg.content) > 0.5 * len(JOKE_ANSWERS[rand])

    msg = await client.wait_for_message(timeout=8, author=message.author, check=add_check)

    if msg is None:
        await client.send_message(message.channel, ":monkey_face: " + JOKE_ANSWERS[rand] + " :monkey_face:\n\n" + LAUGHING_GORILLAS[randint(0,len(LAUGHING_GORILLAS)-1)])
    else:
        await client.send_message(message.channel, ":banana: Correct! + 50 EP, " + message.author.name + " :banana:\n\n" + THUMBS_UP_GORILLA)

async def print_chuck_quote(client, message):
    rand = randint(0, len(CHUCK_QUOTES) - 1)
    await client.send_message(message.channel, CHUCK_QUOTES[rand]) # Print a random chuck quote.

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
                "They use gorilla warfare.",
                "Through the ape vine.",
                "A chimp off the old block."]

CHUCK_QUOTES = ["\"How fun is it to get sloppy blackout drunk and chase after ratchets!\" -Chuck 2016",
                "\"Do you ever drink milk before you go to sleep man? That shit gives you crazy ass dreams.\" -Chuck 2016",
                "\"Dude, Ian, you just need to get over it.\" -Chuck 2016, after Ian tells him he doesn't like to get blackout drunk anymore.",
                "\"HEAL ME!\" -Chuck every single raid",
                "\"Can you link the logs?\" -Chuck every 5 seconds",
                "\"Can you wait two minutes? I popped a potion.\" -Chuck 2016",
                "\"Dude wtf?\" -Chuck 2016",
                "\"Is this fight longer than 8 minutes?\" -Chuck 2016",
                "\"Transmog mount?\" -Chuck 2016",
                "\"Dude, that's gnar!\" -Chuck 2016"]

def main():
    client.accept_invite('https://discord.gg/NyYKejv')

    type = input("Please specify which Harambot you would like to run (dev/prod): ")

    while type != "dev" and type != "prod":
        type = input("That was not a valid input. Please specify which Harambot you would like to run (dev/prod): ")

    if type == "dev":
        client.run("MjQ5NTkwMTE3MzU2Nzk3OTUz.CxIg5A.BYYtQ1H4H3l4CuLl-YrWjI50eOk")
    else:
        client.run('MjQ2MTMxMjkyMjg5MjM2OTky.CwWLNA.Un3vOVd-WKZxpQpTHswfd1ozJUk')

if __name__ == "__main__":
    main()
