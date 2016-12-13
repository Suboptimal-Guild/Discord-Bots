from texttable import Texttable

import discord
import asyncio

# imported functions
from google.sheets import get_EPGP

async def update_EPGP(client, message):
    s = message.content.split()
    print("".join(s[2:]))
    dict = json.loads("".join(s[2:]))
    roster = dict['roster']

    write_EPGP(roster)
    await client.send_message(message.channel, "EPGP is now updated!")

async def print_EPGP(client, message):
    s = message.content.title().split()
    s = s[1:]

    print(len(s))

    output = ""

    if len(s) > 1:
        a = get_EPGP()
        b = [["Name", "EP", "GP", "Ratio"]]
        t = Texttable()

        for row in a:
            if row[0] in s:
                b.append([row[0], row[3], row[4], row[5]])
        if len(b) != len(s) + 1:
            await client.send_message(message.channel, ":banana: One of the names given was invalid. Please try again. :banana:")
        t.add_rows(b)
        output += "EPGP information for **" + " ".join(s) + "**:\n"
        output += "```"
        output += t.draw()
        output += "```"
    elif len(s) == 1:
        a = get_EPGP()

        for row in a:
            if row[0] == s[0]:
                # Player found.
                t = Texttable()
                b = [["Name", "EP", "GP", "Ratio"], [row[0], row[3], row[4], row[5]]]
                t.add_rows(b)
                output += "EPGP information for **" + row[0] + "**:\n"
                output += "```"
                output += t.draw()
                output += "```"
                break
        if output == "":
            # Player wasn't found.
            await client.send_message(message.channel, ":banana: Sorry, but I couln't find EPGP information for " + s[1] + ".\n\nPlease chack the name and try again. :banana:")
    else:
        a = get_EPGP()
        t = Texttable()
        b = [["Name", "EP", "GP", "Ratio"]]
        for row in a[:len(a) // 2]:
            b.append([row[0], row[3], row[4], row[5]])

        c = [["Name", "EP", "GP", "Ratio"]]
        for row in a[len(a) // 2:]:
            c.append([row[0], row[3], row[4], row[5]])

        t.add_rows(b)
        output += "Full EPGP Leaderboard for **Suboptimal**"
        output += "```"
        output += t.draw()
        output += "```"

        await client.send_message(message.channel, output)

        t = Texttable()
        t.add_rows(c)
        output = "```"
        output += t.draw()
        output += "```"

        await client.send_message(message.channel, output)

async def print_EPGP_leaderboard(client, message):
    s = message.content.lower()
    s = message.content.split(' ', 1)[1]
    s = message.content.split(' ', 1)[1]
    s = message.content.split(' ', 1)[1]

    a = get_EPGP()

    armor_types = ["cloth", "leather", "mail", "plate"]
    roles = ["tank", "melee", "ranged", "healer"]
    stats = ["strength", "agility", "intellect"]
    dict = {}

    with open('classifications.json') as f:
        dict = json.load(f)

    player_class = spec = armor = role = stat = ""

    # Look to see if a class was specified.
    for key in sorted(dict.keys()):
        print(str(key).lower() + ", " + s)
        index = s.find(str(key).lower())
        if index > -1:
            player_class = str(key)
            s.replace(key, '')
            break

    # If a class was specified, look for a spec.
    if player_class != "":
        for key, value in dict[player_class].items():
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
            stat = key
            s.replace(key, '')
            break

    # Filter results.
    c = []
    for row in a[:]:
        if player_class != "" and row[1] != player_class:
            a.remove(row)
        elif spec != "" and row[2] != spec:
            a.remove(row)
        elif armor != "" and dict[row[1]][row[2]]["Armor Type"][0].lower() != armor[0]:
            a.remove(row)
        elif role != "" and dict[row[1]][row[2]]["Role"][0].lower() != role[0]:
            a.remove(row)
        elif stat != "" and dict[row[1]][row[2]]["Main Stat"][0].lower() != stat[0]:
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
    output += "```"
    output += t.draw()
    output += "```"

    await client.send_message(message.channel, output)
