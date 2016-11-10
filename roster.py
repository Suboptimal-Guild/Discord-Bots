import discord
import asyncio
import csv

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
        writer.writerow([s[2], s[3], s[4], s[5], s[6]])

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
        await client.send_message(message.channel, ":banana: I was unable to find **" + str(s[1]) + "** on the guild roster. :banana:")


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
            #print "%s" % player['Name']
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])
            #await client.send_message(message.channel, "%s %s %s %s" % (player['Name'], player['Class'], player['Spec'], player['Rank']))

        m += "\n"

        m += "# # # # # # # # # # # # RANGE # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in ranged:
            #print "%s" % player['Name']
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])
            #await client.send_message(message.channel, "%s %s %s %s" % (player['Name'], player['Class'], player['Spec'], player['Rank']))

        m += "\n"

        m += "# # # # # # # # # # # # HEALS # # # # # # # # # # # #\n"
        m += "-----------------------------------------------------\n"

        for player in healers:
            #print "%s" % player['Name']
            m += "{:12s}   {:12s}   {:13s}   {:7s}\n".format(player['Name'], player['Class'], player['Spec'], player['Rank'])
            #await client.send_message(message.channel, "%s %s %s %s" % (player['Name'], player['Class'], player['Spec'], player['Rank']))

        m += "```"

        return m
