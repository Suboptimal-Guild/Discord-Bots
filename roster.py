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

        for row in spamreader:
            if row['Role'] == 'R':
                ranged.append(row)
            elif row['Role'] == 'H':
                healers.append(row) 
