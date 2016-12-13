import discord
from random import randint

# CONSTANTS
CHUCK_QUOTES = [
                "\"How fun is it to get sloppy blackout drunk and chase after ratchets!\" -Chuck 2016",
                "\"Do you ever drink milk before you go to sleep man? That shit gives you crazy ass dreams.\" -Chuck 2016",
                "\"Dude, Ian, you just need to get over it.\" -Chuck 2016, after Ian tells him he doesn't like to get blackout drunk anymore.",
                "\"Big heals on Chuck.\" -Chuck every single raid",
                "\"Can you link the logs?\" -Chuck every 5 seconds",
                "\"Can you wait two minutes? I popped a potion.\" -Chuck 2016",
                "\"Dude wtf?\" -Chuck 2016",
                "\"Is this fight longer than 8 minutes?\" -Chuck 2016",
                "\"Transmog mount?\" -Chuck 2016",
                "\"Dude, that's gnar!\" -Chuck 2016"
]

PETER_QUOTES = [
                "\"I wonder how big that kid's dick is...\" -Peter 2016"
]

async def print_quote(client, message, name):
    if name == "chuck":
        rand = randint(0, len(CHUCK_QUOTES) - 1)
        await client.send_message(message.channel, CHUCK_QUOTES[rand]) # Print a random Chuck quote.
    elif name == "peter":
        rand = randint(0, len(PETER_QUOTES) - 1)
        await client.send_message(message.channel, PETER_QUOTES[rand]) # Print a random Peter quote.
