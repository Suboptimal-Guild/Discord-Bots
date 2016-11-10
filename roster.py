import discord
import asyncio
import csv

async def pmd(client, message):
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

        await client.send_message(message.channel, m)
