from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from enum import Enum
from time import strftime

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# Enums
#AbsenceType = Enum('AbsenceType', 'late absent eloa')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_post_out(name, starttime, endtime, type):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    typedesc = ""
    description = ""

    if type == 'late':
        typedesc = "Late"
        description = "will be late tonight."
    elif type == 'absent':
        typedesc = "Absent"
        description = "will be absent tonight."
    elif type == 'eloa':
        typedesc = "Extended Leave of Absence"
        description = "will be absent for this time period."

    print(typedesc)
    print(description)

    # body
    event = {
        'summary': '{0} '.format(name) + typedesc,
        'location': 'Raid',
        'description': '{0} '.format(name) + description,
        'start': {
            'dateTime': starttime,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': endtime,
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    eventsResult = service.events().insert(
        calendarId='9gspv11m882ke0jt24rdkpudss@group.calendar.google.com', sendNotifications=True,
        supportsAttachments=True, maxAttendees=1, body=event).execute()

def get_post_outs():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='9gspv11m882ke0jt24rdkpudss@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(datetime.datetime.strptime(start[:-6], "%Y-%m-%dT%H:%M:%S").strftime('%a, %b %d, %Y %I:%M %p'), datetime.datetime.strptime(start[:-6], "%Y-%m-%dT%H:%M:%S").strftime('%a, %b %d, %Y %I:%M %p'), event['summary'])

    return events


if __name__ == '__main__':
    #get_post_outs()
    create_post_out("Ripparian", "2016-12-28T09:00:00", "2016-12-29T00:00:00", "late")
    #list_cals()
