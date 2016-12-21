import discord

async def get_logs_page(client, message):
    s = message.content.split()
    pass

async def get_logs_links(client, message):
    peter_logs_url = "https://www.warcraftlogs.com/guilds/usercalendar/256766"
    ian_logs_url = "https://www.warcraftlogs.com/guilds/usercalendar/5415"
    tyhler_logs_url = "https://www.warcraftlogs.com/guilds/201686"

    s = "Peter's logs: " + peter_logs_url + "\nIan's logs: " + ian_logs_url + "\nTyhler's logs: " + tyhler_logs_url
    await client.send_message(message.channel, ":banana: " + s + " :banana:")
