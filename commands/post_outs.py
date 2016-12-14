from texttable import Texttable
import datetime
from time import strftime
import asyncio

from google.googcal import create_post_out
from google.googcal import get_post_outs

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

    def generate_single_raid_dates(date):
        if len(date[2]) == 2:
            date[2] = "20" + date[2]
        startdate = datetime.datetime.combine(datetime.date(int(date[2]), int(date[0]), int(date[1])), datetime.time(21, 0))
        enddate = startdate + datetime.timedelta(hours=3)
        startdate = startdate.isoformat()
        enddate = enddate.isoformat()

        return startdate, enddate

    # Generate start and end datetime
    if s[0] == "!postout":
        try:
            startdate = generate_date_time(s[1], s[2])
            enddate = generate_date_time(s[3], s[4])
        except ValueError:
            await client.send_message(message.channel, ":banana: Sorry, I could not create a post out with the given information :banana:")
            return
        type = "eloa"
    elif s[0] == "!absent":
        date = s[1].split('/')
        try:
            startdate, enddate = generate_single_raid_dates(date)
        except ValueError:
            await client.send_message(message.channel, ":banana: Sorry, I could not create a post out with the given information :banana:")
            return
        type = "absent"
    elif s[0] == "!late":
        date = s[1].split('/')
        try:
            startdate, enddate = generate_single_raid_dates(date)
        except ValueError:
            await client.send_message(message.channel, ":banana: Sorry, I could not create a post out with the given information :banana:")
            return
        type = "late"

    if message.author.nick == None:
        try:
            await client.send_message(message.channel, ":banana: Post out has been added to the calendar! :banana:")
            await client.send_message(message.channel, create_post_out(message.author.name, str(startdate), str(enddate), type))
        except ValueError:
            await client.send_message(message.channel, ":banana: Sorry, I could not create a post out with the given information :banana:")
    else:
        try:
            await client.send_message(message.channel, ":banana: Post out has been added to the calendar! :banana:")
            await client.send_message(message.channel, create_post_out(message.author.name, str(startdate), str(enddate), type))
        except ValueError:
            await client.send_message(message.channel, ":banana: Sorry, I could not create a post out with the given information :banana:")
