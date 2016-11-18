from texttable import Texttable

import discord
import asyncio
import csv

#TODO: modularize code more and split into multiple files, im exhausted as fuck so just cramming it in here for now, it works though

# for some reason, there is a massive stink with this??? i think maybe python 2.7 vs 3.5 conflict... ill keep working in the google_sheets_interface file to get functionality down before linking it up
from sheets import get_main_character_name as gmcn
from sheets import get_roster

VALID_KEYWORDS = {"Death Knight": ["Blood", "Frost", "Unholy"],
               "Demon Hunter": ["Havoc", "Vengeance"],
               "Druid": ["Balance", "Feral", "Guardian", "Restoration"],
               "Hunter": ["Beast Mastery", "Marksmanship", "Survival"],
               "Mage": ["Arcane", "Fire", "Frost"],
               "Monk": ["Brewmaster", "Mistweaver", "Windwalker"],
               "Paladin": ["Holy", "Protection", "Retribution"],
               "Priest": ["Discipline", "Holy", "Shadow"],
               "Rogue": ["Assassination", "Outlaw", "Subtlety"],
               "Shaman": ["Elemental", "Enhancement", "Restoration"],
               "Warlock": ["Affliction", "Demonology", "Destruction"],
               "Warrior": ["Arms", "Fury", "Protection"]}

VALID_RANKS = ["Trial", "Raider", "Officer", "GM"]

async def showhelp(client, message):
    # prints out all commands that Harambot currently knows

    print(get_help_string())

    await client.send_message(message.channel, get_help_string())

async def print_me_daddy(client, message):
    await client.send_message(message.channel, get_roster_string())

async def add_to_roster(client, message):
    # format: !roster add <name> <role> <class> <spec> <rank>
    s = message.content.split()

    with open('roster.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
        if (len(s) == 7):
            writer.writerow([s[2], s[3], s[4], s[5], s[6]])
        elif len(s) == 8:
            writer.writerow([s[2], s[3], (s[4] + " " + s[5]), s[6], s[7]])


    await client.send_message(message.channel, ":banana: Added **" + s[2] + "** to roster! :monkey_face: :banana:")

    new_roster_string = get_roster_string()
    await client.send_message(message.channel, new_roster_string)

async def remove_from_roster(client,message):
    # format: !roster remove <name>
    s = message.content.split()

    with open('roster.csv', 'r') as in_file, open('roster_edit.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if row[0] != s[2]:
                writer.writerow(row)

    # at this point, roster_edit.csv has our correct updated roster, so we need to transfer back to roster.csv
    with open('roster_edit.csv', 'r') as in_file, open('roster.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            writer.writerow(row)

    await client.send_message(message.channel, ":banana: Removed **" + s[2] + "** from roster! :cry: :banana:")

    new_roster_string = get_roster_string()
    await client.send_message(message.channel, new_roster_string)

async def get_armory_link(client, message):
    # format: !armory <name>
    s = message.content.split()

    if len(s) == 2:
        link = "http://us.battle.net/wow/en/character/emerald-dream/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")
    elif len(s) == 3:
        link = "http://us.battle.net/wow/en/character/" + s[2].lower() + "/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")
    else:
        link = "http://us.battle.net/wow/en/character/" + s[2].lower() + "-" + s[3].lower() + "/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")

async def get_char_name(client, message):
    msg = message.content.split()

    name = msg[1]

    isNameFound = False

    nickname = ""
    roles = ""

    for member in message.server.members:
        if name == member.name:
            isNameFound = True
            if member.nick is not None:
                nickname = member.nick
            roles = member.roles
            break

    str = "Discord User name: " + name + "\nNickname on server " + message.server.name + ": " + nickname + "\nRoles: "
    for role in roles:
        str += (role.name + ", ")
    str = str[:-2]

    await client.send_message(message.channel, str)


async def get_own_name(client, message):
    str = "Discord User name: " + message.author.name + "\nNickname on server " + message.server.name + ": " + message.author.nick + "\nRoles: "
    for role in message.author.roles:
        str += (role.name + ", ")
    str = str[:-2]

    await client.send_message(message.channel, str)

async def get_character(client, message):
    msg = message.content.split()
    # usage: !char <discord_name>

    str = gmcn(msg[1])
    title = msg[1]

    # If the person's name ends with s (ex: Stannis), just add an apostrophe to
    # the end. (ex: Stannis')
    if msg[1][-1:] == 's':
        title += "' Characters"
    # Otherwise use "'s".
    else:
        title += "'s Characters"

    # Use a code block to format it.
    output = "```\n"
    # Center the title.
    output += title.center(40, '-')
    output += "\n"
    # Output all of the characters found. Space them appropriately.
    for x in str:
        output += "{:12s}   {:12s}   {:10s}\n".format(x[1], x[2], x[3])
    output += "```"

    # Output the message.
    await client.send_message(message.channel, output)

def get_help_string():
    str = ":banana: :monkey_face: OOH OOH AAH AAH :monkey_face: :banana:. Currently I know the following commands:\n\n"
    t = Texttable()

    print("Texttable created!!!!!!")

    t.add_rows([["Command", "Description"],
                ["!armory <character_name> <server> (if not from ED)", "Generates an armory link for the given character."],
                #["!chars <discord_name>", "Generates a list of the discord user's World of Warcraft characters."],
                ["!roster add <character_name>", "Add's a character to the raid roster. (officers only)"],
                ["!roster remove <character_name>", "Removes a character from the raid roster. (officers only)"],
                ["!roster status <character_name>", "Prints out a quick summary of who will be absent on what days."],
                ["!whoami", "Prints out your Discord Name, Server Nickname, and Roles."],
                ["!whois <discord_name>", "Prints out the Discord Name, Server Nickname, and Roles of a user."],
                ["mention the word \"joke\"", "I will tell you a joke."],
                ["!logslink", "Posts the link to Ian's, Peter's, and Tyhler's logs."],
                ["!logspage <character name> <server> (if not from ED)", "Generates the URL for a player's page on WarcraftLogs."]
                ])

    str += "```"
    str += t.draw()
    str += "```"

    str += "\nI'm a work in progress with more commands coming each and every day- if you have any suggestions forward them to my overlords @Mortivius and @Ian!"
    return str

def get_roster_string():
    a = get_roster()

    tanks = []
    healers = []
    melee = []
    ranged = []

    s = ":banana: Roster for Suboptimal *(" + str(len(a)) + " members total)* :banana:"

    for t in a:
        if t[1] == "T":
            tanks.append(t)
        elif t[1] == "M":
            melee.append(t)
        elif t[1] == "R":
            ranged.append(t)
        else:
            healers.append(t)

    melee.sort(key=lambda tup: (tup[4], tup[0]))
    ranged.sort(key=lambda tup: (tup[4], tup[0]))
    tanks.sort(key=lambda tup: (tup[4], tup[0]))
    healers.sort(key=lambda tup: (tup[4], tup[0]))

    t = Texttable()

    b = [["Name", "Role", "Class", "Spec", "Rank"]]

    names = roles = classes = specs = ranks = ""

    for player in tanks:
        names += player[0] + '\n'
        roles += player[1] + '\n'
        classes += player[2] + '\n'
        specs += player[3] + '\n'
        ranks += player[4] + '\n'

    names = names[:-1]
    roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, roles, classes, specs, ranks])

    names = roles = classes = specs = ranks = ""

    for player in melee:
        names += player[0] + '\n'
        roles += player[1] + '\n'
        classes += player[2] + '\n'
        specs += player[3] + '\n'
        ranks += player[4] + '\n'

    names = names[:-1]
    roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, roles, classes, specs, ranks])

    names = roles = classes = specs = ranks = ""

    for player in ranged:
        names += player[0] + '\n'
        roles += player[1] + '\n'
        classes += player[2] + '\n'
        specs += player[3] + '\n'
        ranks += player[4] + '\n'

    names = names[:-1]
    roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, roles, classes, specs, ranks])

    names = roles = classes = specs = ranks = ""

    for player in healers:
        names += player[0] + '\n'
        roles += player[1] + '\n'
        classes += player[2] + '\n'
        specs += player[3] + '\n'
        ranks += player[4] + '\n'

    names = names[:-1]
    roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, roles, classes, specs, ranks])

    t.add_rows(b)

    s += "```"
    s += t.draw()
    s += "```"

    return s;
