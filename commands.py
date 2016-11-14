from texttable import Texttable

import discord
import asyncio
import csv

#TODO: modularize code more and split into multiple files, im exhausted as fuck so just cramming it in here for now, it works though

# for some reason, there is a massive stink with this??? i think maybe python 2.7 vs 3.5 conflict... ill keep working in the google_sheets_interface file to get functionality down before linking it up
from sheets import get_main_character_name as gmcn

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
    str = ":banana: :monkey_face: OOH OOH AAH AAH :monkey_face: :banana:. Currently I know the following commands:\n\n"

    t = Texttable()

    t.add_rows([["Command", "Description"],
                ["!armory <character_name>", "Generates an armory link for the given character."],
                ["!chars <discord_name>", "Generates a list of the discord user's World of Warcraft characters."],
                ["!roster add <character_name>", "Add's a character to the raid roster."],
                ["!roster remove <character_name>", "Removes a character from the raid roster."],
                ["!roster status <character_name>", "Prints out a quick summary of who will be absent on what days."],
                ["!whoami", "Prints out your Discord Name, Server Nickname, and Roles."],
                ["!whois <discord_name>", "Prints out the Discord Name, Server Nickname, and Roles of a user."]
                ])

    str += "```"
    str += t.draw()
    str += "```"

    await client.send_message(message.channel, str)


async def print_me_daddy(client, message):
    roster_string = get_roster_string()
    roster_size = get_roster_size()

    await client.send_message(message.channel, ":banana: Roster for Suboptimal *(" + str(roster_size) + " members total)* :banana:")
    await client.send_message(message.channel, roster_string)

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
    person_is_on_roster = False
    link = "http://us.battle.net/wow/en/character/emerald-dream/" + s[1] + "/advanced"

    with open('roster.csv', 'r') as in_file:
        for row in csv.reader(in_file):
            if row[0] == s[1]:
                person_is_on_roster = True
                break

    # first, verify that the requested person is actually on the roster
    if person_is_on_roster:
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")
    else:
        await client.send_message(message.channel, ":banana: I was unable to find **" + str(s[1]) + "** on the guild roster. Would you like me to add them? :banana:")

        #TODO: need to figure out multiple checks, since currently even if i say no it has to wait until the timeout to keep checking for yes. Hmm...
        def add_check(msg):
            return msg.content == "yes"

        #msg = await client.wait_for_message(author=message.author, content='no')
        msg = await client.wait_for_message(timeout=10, author=message.author, check=add_check)

        if msg is None:
            await client.send_message(message.channel, ":banana: Ok, **" + str(s[1]) + "** was not added. :banana:")
        elif msg.content == "yes":
            await client.send_message(message.channel, ":banana: Ok, please type the letter for their role followed by their class, spec, and rank, all separated by spaces. :banana:")

            def check(msg):
                valid_roles = ["T", "M", "R", "H"]
                a = msg.content.split()

                bool_one = (len(a) == 4 and a[0] in valid_roles and a[1] in VALID_KEYWORDS and a[2] in VALID_KEYWORDS[a[1]] and a[3] in VALID_RANKS)
                bool_two = (len(a) == 5 and a[0] in valid_roles and (a[1] + " " + a[2]) in VALID_KEYWORDS and a[3] in VALID_KEYWORDS[(a[1] + " " + a[2])] and a[4] in VALID_RANKS)
                return bool_one or bool_two

            msg2 = await client.wait_for_message(timeout=15, author=message.author, check=check)

            if msg2 is None:
                 await client.send_message(message.channel, ":banana: Sorry, I was unable to add **" + s[1] +"** to the roster. :banana:")
            else:
                msg2.content = "!roster add " + str(s[1]) + " " + msg2.content
                await add_to_roster(client, msg2)
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


def get_roster_size():
    with open('roster.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        count = sum(1 for row in reader)
        return count

def get_roster_string():
    with open('roster.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        tanks = []
        healers = []
        melee = []
        ranged = []

        for row in reader:
            if row['Role'] == 'T':
                tanks.append(row)
            elif row['Role'] == 'M':
                melee.append(row)
            elif row['Role'] == 'R':
                ranged.append(row)
            elif row['Role'] == 'H':
                healers.append(row)
            else:
                print("Help")

        m =  "```"
        m += "# # # # # # # # # # # # TANKS # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in tanks:
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])

        m += "\n"
        m += "# # # # # # # # # # # # MELEE # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in melee:
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])

        m += "\n"
        m += "# # # # # # # # # # # # RANGE # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in ranged:
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])

        m += "\n"
        m += "# # # # # # # # # # # # HEALS # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in healers:
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])

        m += "```"

        return m
