from texttable import Texttable

import discord
import asyncio
import csv
import json
import datetime
from time import strftime

#TODO: modularize code more and split into multiple files, im exhausted as fuck so just cramming it in here for now, it works though

# for some reason, there is a massive stink with this??? i think maybe python 2.7 vs 3.5 conflict... ill keep working in the google_sheets_interface file to get functionality down before linking it up
from sheets import get_main_character_name as gmcn
from sheets import get_roster
from sheets import get_EPGP
from sheets import write_EPGP
from googcal import create_post_out
from googcal import get_post_outs

async def showhelp(client, message):
    # prints out all commands that Harambot currently knows
    header, str1, str2, footer = get_help_strings()

    await client.send_message(message.channel, header)
    await client.send_message(message.channel, str1)
    await client.send_message(message.channel, str2)
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
                ["!whois <discord_name>", "Prints out the Discord info of a user."]
                ])

    str1 = "```"
    str1 += t.draw()
    str1 += "```"

    t = Texttable()
    t.add_rows([["Command", "Description"],
                ["!epgp", "Prints the entire EPGP leaderboard."],
                ["!epgp leaderboard <params>", "Prints EPGP leaderboard for the parameters specified."],
                ["!epgp export <export string>", "Update the EPGP spreadsheet!."],
                ["!postout <startdate> <starttime> <enddate> <endtime>", "Create a calendar event to post out for a given time period.\n" +
                                                                         "Date Format: (mm/dd/yy)\n" +
                                                                         "Time Format: (hh:mm{AM/PM}) OR use (hh:mm) in military time"],
                #["!bis",""],
                #["!audit",""],
                ["mention the word \"joke\"", "I will tell you a joke."],
                ["!logs", "Posts the WarcraftLogs links."],
                #["!logspage <character name> <server> (if not from ED)", "Generates the URL for a player's page on WarcraftLogs."]
                ])

    str2 = "```"
    str2 += t.draw()
    str2 += "```"

    footer_text = "\n:monkey_face: I'm a work in progress with more commands coming each and every day- if you have any suggestions forward them to my overlords Mortivius and Ian! :monkey_face:"
    return header_text, str1, str2, footer_text

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

async def update_EPGP(client, message):
    s = message.content.split()
    print("".join(s[2:]))
    dict = json.loads("".join(s[2:]))
    roster = dict['roster']

    write_EPGP(roster)
    await client.send_message(message.channel, "EPGP is now updated!")

async def print_attendance(client, message):
    events = get_post_outs()

    if events == []:
        await client.send_message(message.channel, ":banana: There are no post outs currently! :banana:")
        return

    t = Texttable()

    b = [["Event Name", "Start", "End"]]

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.strptime(start[:-6], "%Y-%m-%dT%H:%M:%S").strftime('%a %b %d, %Y %I:%M %p')
        end = event['end'].get('dateTime', event['end'].get('date'))
        end = datetime.datetime.strptime(end[:-6], "%Y-%m-%dT%H:%M:%S").strftime('%a %b %d, %Y %I:%M %p')
        b.append([event['summary'], str(start), str(end)])

    t.add_rows(b)

    output = "Post outs for Suboptimal\n```"
    output += t.draw()
    output += "```"

    await client.send_message(message.channel, output)

async def generate_post_out(client, message):
    s = message.content.split()
    startdate = None
    enddate = None
    type = ""

    def generate_date_time(date, time):
        # Generate start datetime
        date = date.split('/') # Split the date into month, day, and year
        time = time.split(':') # Split the time into hour and minutes

        # Add the leading numbers to the year if they put in two numbers for the year.
        if len(date[2]) == 2:
            date[2] = "20" + date[2]

        if int(time[0]) > 12 or int(time[0]) == 0: # If they put in military time.
            time[0] = int(time[0])
        elif time[0] == '12' and time[1][-2:] == "PM": # Midnight in military time is 0:00
            time[0] = 0
        elif time[1][-2:] == "PM": # Convert a PM time to military time.
            time[0] = int(time[0]) + 12
        else: # Otherwise just use the given hour.
            time[0] = int(time[0])

        # Generate the datetime date and time.
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        time = datetime.time(time[0], int(time[1][:2]))

        # Combine the date and time and format it into a proper string.
        return datetime.datetime.combine(date, time).isoformat()

    # Generate start and end datetime
    if s[0] == "!postout":
        startdate = generate_date_time(s[1], s[2])
        enddate = generate_date_time(s[3], s[4])
        type = "eloa"
    elif s[0] == "!absent":
        date = s[1].split('/')
        startdate = datetime.datetime.combine(datetime.date(int(date[2]), int(date[0]), int(date[1])), datetime.time(21, 0))
        enddate = startdate + datetime.timedelta(hours=3)
        startdate = startdate.isoformat()
        enddate = enddate.isoformat()
        type = "absent"
    elif s[0] == "!late":
        date = s[1].split('/')
        startdate = datetime.datetime.combine(datetime.date(int(date[2]), int(date[0]), int(date[1])), datetime.time(21, 0))
        enddate = startdate + datetime.timedelta(hours=3)
        startdate = startdate.isoformat()
        enddate = enddate.isoformat()
        type = "late"

    if message.author.nick == None:
        create_post_out(message.author.name, str(startdate), str(enddate), type)
    else:
        create_post_out(message.author.nick, str(startdate), str(enddate), type)

    await client.send_message(message.channel, ":banana: Post out has been added to the calendar! :banana:")

def get_roster_strings():
    roster = get_roster()

    header_string = ":banana: Roster for Suboptimal *(" + str(len(roster)) + " members total)* :banana:"

    table_dict = {}

    table_dict['T'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['M'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['R'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['H'] = [["Name", "Class", "Spec", "Rank"]]

    for player in roster:
        table_dict[player[1]].append([player[0], player[2], player[3], player[4]])

    # Helper function so we repeat ourselves less.
    def get_roster_print(header, rows):
        t = Texttable()
        t.add_rows(rows)
        return str(header + '\n```' + t.draw() + "```")

    tank_string = get_roster_print('**TANKS**', table_dict['T']) # Add tanks to our output.
    melee_string = get_roster_print('**MELEE**', table_dict['M']) # Add melee to our output.
    ranged_string = get_roster_print('**RANGED**', table_dict['R']) # Add ranged to our output.
    healer_string = get_roster_print('**HEALERS**', table_dict['H']) # Add healers to our output.

    return header_string, tank_string, melee_string, ranged_string, healer_string
