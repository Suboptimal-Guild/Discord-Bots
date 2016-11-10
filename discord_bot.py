#!/usr/bin/python

import discord

client = discord.Client()

# Disables the SSL warning that is printed to the console.
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

@client.event

def on_message(message):

    hashedPW = b'$2b$12$e.iRNKBzIpx7cDkzIdR8s.7Zce7bSef4dBnVDHcRj7QVBgLlXCEY2';
    realPW = 
