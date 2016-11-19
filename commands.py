from texttable import Texttable

import discord
import asyncio
import csv
import json

#TODO: modularize code more and split into multiple files, im exhausted as fuck so just cramming it in here for now, it works though

# for some reason, there is a massive stink with this??? i think maybe python 2.7 vs 3.5 conflict... ill keep working in the google_sheets_interface file to get functionality down before linking it up
from sheets import get_main_character_name as gmcn
from sheets import get_roster
from sheets import write_EPGP

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

async def showhelp(client, message):
    # prints out all commands that Harambot currently knows
    header, mainstring, footer = get_help_strings()

    await client.send_message(message.channel, header)
    await client.send_message(message.channel, mainstring)
    await client.send_message(message.channel, footer)

async def print_roster(client, message):
    header, tanks, melee, ranged, healers = get_roster_strings()

    await client.send_message(message.channel, header)
    await client.send_message(message.channel, tanks)
    await client.send_message(message.channel, melee)
    await client.send_message(message.channel, ranged)
    await client.send_message(message.channel, healers)

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
    # format: !armory <name> <optional server>
    s = message.content.split()

    if len(s) == 2:
        link = "http://us.battle.net/wow/en/character/emerald-dream/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")
    elif len(s) == 3:
        link = "http://us.battle.net/wow/en/character/" + s[2].lower() + "/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")
    #TODO: we sure there are no realms that are 3 words???
    else:
        link = "http://us.battle.net/wow/en/character/" + s[2].lower() + "-" + s[3].lower() + "/" + s[1].title() + "/advanced"
        await client.send_message(message.channel, ":banana: Armory link for **" + str(s[1]) + "**: " + link + " :banana:")

async def get_logs_page(client, message):
    s = message.content.split()
    pass

async def get_logs_links(client, message):
    peter_logs_url = "https://www.warcraftlogs.com/guilds/usercalendar/256766"
    ian_logs_url = "https://www.warcraftlogs.com/guilds/usercalendar/5415"
    tyhler_logs_url = "https://www.warcraftlogs.com/guilds/201686"

    s = "Peter's logs: " + peter_logs_url + "\nIan's logs: " + ian_logs_url + "\nTyhler's logs: " + tyhler_logs_url
    await client.send_message(message.channel, ":banana: " + s + " :banana:")

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

def get_help_strings():
    header_text = ":banana: Currently I know the following commands: :banana:"
    t = Texttable()

    t.add_rows([["Command", "Description"],
                ["!armory <character_name> <server> (if not from ED)", "Generates an armory link for the given character."],
                #["!chars <discord_name>", "Generates a list of the discord user's World of Warcraft characters."],
                ["!roster add <name>", "Adds to the raid roster."],
                ["!roster remove <name>", "Removes from the raid roster."],
                ["!roster status <name>", "Prints out current raid roster."],
                ["!whoami", "Prints out your Discord info."],
                ["!whois <discord_name>", "Prints out the Discord info of a user."],
                #["!epgp",""],
                #["!bis",""],
                #["!audit",""],
                ["mention the word \"joke\"", "I will tell you a joke."],
                ["!logs", "Posts the WarcraftLogs links."],
                #["!logspage <character name> <server> (if not from ED)", "Generates the URL for a player's page on WarcraftLogs."]
                ])

    str = "```"
    str += t.draw()
    str += "```"

    footer_text = "\n:monkey_face: I'm a work in progress with more commands coming each and every day- if you have any suggestions forward them to my overlords Mortivius and Ian! :monkey_face:"
    return header_text, str, footer_text

async def print_EPGP(client, message):
    s = message.content.split()

    output = ""

    if len(s) > 2:
        await client.send_message(message.channel, ":banana: Sorry, but that is invalid input. Please try again. :banana:")
        return
    elif len(s) == 2:
        a = get_EPGP()

        for row in a:
            if row[0] == s[1]:
                # Player found.
                t = Texttable()
                b = [["Name", "EP", "GP", "Ratio"], [row[0], row[3], row[4], row[5]]]
                t.add_rows(b)
                output += "EPGP information for **" + row[0] + "**:\n"
                output += "'''"
                output += t.draw()
                output += "'''"
                break
        if output == "":
            # Player wasn't found.
            await client.send_message(message.channel, ":banana: Sorry, but I couln't find EPGP information for " + s[1] + ".\n\nPlease chack the name and try again.". :banana:")

    else:
        a = get_EPGP()
        t = Texttable()
        b = [["Name", "EP", "GP", "Ratio"]]
        for row in a:
            b.append([row[0], row[3], row[4], row[5]])
            t.add_rows(b)
            output += "Full EPGP Leaderboard for **Suboptimal**"
            output += "'''"
            output += t.draw()
            output += "'''""

    await client.send_message(message.channel, output)

async def print_EPGP_leaderboard(client, message):
    s = message.content.lower()
    s = message.content.split(' ', 1)[1]
    s = message.content.split(' ', 1)[1]

    a = get_EPGP()

    armor_types = ["cloth", "leather", "mail", "plate"]
    roles = ["tank", "melee", "ranged", "healer"]
    stats = ["strength", "agility", "intellect"]
    dict = {}

    with open('dclassifications.json') as f:
        dict = json.load(f)

    player_class = spec = armor = role = stat = ""

    # Look to see if a class was specified.
    for key in VALID_KEYWORDS.items():
        index = s.find(key)
        if index > -1:
            player_class = key
            s.replace(key, '')
            break

    # If a class was specified, look for a spec.
    if player_class != "":
        for key in dict[player_class].items():
            index = s.find(key)
            if index > -1:
                spec = key
                s.replace(key, '')
                break

    # Look to see if an armor type was specified.
    for key in armor_types:
        index = s.find(key)
        if index > -1:
            armor = key
            s.replace(key, '')
            break

    # Look to see if a role was specified.
    for key in roles:
        index = s.find(key)
        if index > -1:
            role = key
            s.replace(key, '')
            break

    # Look to see if a stat was specified.
    for key in stats:
        index = s.find(key)
        if index > -1:
            role = key
            s.replace(key, '')
            break

    # Filter results.
    for row in a:
        if player_class != "" and row[1] != player_class:
            a.remove(row)
        elif spec != "" and row[2] != spec:
            a.remove(row)
        elif armor != "" and dict[row[1]][row[2]]["Armor Type"][0] != armor[0]:
            a.remove(row)
        elif role != "" and dict[row[1]][row[2]]["Role"][0] != role[0]:
            a.remove(row)
        elif stat != "" and dict[row[1]][row[2]]["Stat"][0] != stat[0]:
            a.remove(row)

    # Make the string look pretty.
    output = "Here is the EPGP leaderboard for the following parameters:\n"
    if player_class != "":
        output += "Class: " + player_class.title() + '\n'
    if spec != "":
        output += "Spec: " + spec.title() + '\n'
    if armor != "":
        output += "Armor Type: " + armor.title() + '\n'
    if role != "":
        output += "Role: " + role.title() + '\n'
    if stat != "":
        output += "Stat: " + stat.title() + '\n'

    t = Texttable()
    b = [["Name", "EP", "GP", "Ratio"]]
    for row in a:
        b.append([row[0], row[3], row[4], row[5]])
    t.add_rows(b)
    output += "'''"
    output += t.draw()
    output += "'''"

    await client.send_message(message.channel, output)

async def update_EPGP(client, message):
    s = message.content.split()
    dict = json.loads(s)
    roster = dict['roster']

    write_EPGP(roster)
    await client.send_message(message.channel, "EPGP is now updated!")


#TODO: my god we need to make this method more elegant
def get_roster_strings():
    roster = get_roster()

    tanks = []
    healers = []
    melee = []
    ranged = []

    header_string = ":banana: Roster for Suboptimal *(" + str(len(roster)) + " members total)* :banana:"
    tank_string = ranged_string = melee_string = healer_string = ""

    # we know based on the method defined in sheets.py that player[1] is the letter that indicates role
    for player in roster:
        newplayer = [player[0],player[2],player[3],player[4]]
        if player[1] == "T":
            tanks.append(newplayer)
        elif player[1] == "M":
            melee.append(newplayer)
        elif player[1] == "R":
            ranged.append(newplayer)
        else:
            healers.append(newplayer)

    melee.sort(key=lambda tup: (tup[3], tup[0]))
    ranged.sort(key=lambda tup: (tup[3], tup[0]))
    tanks.sort(key=lambda tup: (tup[3], tup[0]))
    healers.sort(key=lambda tup: (tup[3], tup[0]))

    t = Texttable()
    b = [["Name", "Class", "Spec", "Rank"]]
    names = roles = classes = specs = ranks = ""

    for player in tanks:
        names += player[0] + '\n'
        #roles += player[1] + '\n'
        classes += player[1] + '\n'
        specs += player[2] + '\n'
        ranks += player[3] + '\n'

    names = names[:-1]
    #roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, classes, specs, ranks])
    t.add_rows(b)
    tank_string += "**TANKS**\n```"
    tank_string += t.draw()
    tank_string += "```"

    t = Texttable()
    b = [["Name", "Class", "Spec", "Rank"]]
    names = roles = classes = specs = ranks = ""

    for player in melee:
        names += player[0] + '\n'
        #roles += player[1] + '\n'
        classes += player[1] + '\n'
        specs += player[2] + '\n'
        ranks += player[3] + '\n'

    names = names[:-1]
    #roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, classes, specs, ranks])
    t.add_rows(b)
    melee_string += "**MELEE DPS**\n```"
    melee_string += t.draw()
    melee_string += "```"

    t = Texttable()
    b = [["Name", "Class", "Spec", "Rank"]]
    names = roles = classes = specs = ranks = ""

    for player in ranged:
        names += player[0] + '\n'
        #roles += player[1] + '\n'
        classes += player[1] + '\n'
        specs += player[2] + '\n'
        ranks += player[3] + '\n'

    names = names[:-1]
    #roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, classes, specs, ranks])
    t.add_rows(b)
    ranged_string += "**RANGED DPS**\n```"
    ranged_string += t.draw()
    ranged_string += "```"

    t = Texttable()
    b = [["Name", "Class", "Spec", "Rank"]]
    names = roles = classes = specs = ranks = ""

    for player in healers:
        names += player[0] + '\n'
        #roles += player[1] + '\n'
        classes += player[1] + '\n'
        specs += player[2] + '\n'
        ranks += player[3] + '\n'

    names = names[:-1]
    #roles = roles[:-1]
    classes = classes[:-1]
    specs = specs[:-1]
    ranks = ranks[:-1]

    b.append([names, classes, specs, ranks])
    t.add_rows(b)
    healer_string += "**HEALERS**\n```"
    healer_string += t.draw()
    healer_string += "```"

    return header_string, tank_string, melee_string, ranged_string, healer_string
