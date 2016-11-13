from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


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
                                   'sheets.googleapis.com-python-quickstart.json')

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

def get_main_character_name(discord_name):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1K0V19lxMsIC7TzLTJ8AY8s7vjlIljpmK_5MuO2LopSI' # Harambot Test spreadsheet
    rangeName = 'Discord!A2:D'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        #print('Discord Name, Main Character Name:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if row[0] == discord_name:
                print('Name is ' + row[1] + '!')
                return row[1], row[2], row[3]
            #print('%s, %s' % (row[0], row[1]))
        print('Discord name not found!')
        return -1

def add_character(name, classname, role):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1K0V19lxMsIC7TzLTJ8AY8s7vjlIljpmK_5MuO2LopSI' # Harambot Test spreadsheet
    rangeName = 'A1:A'
    values = {'values':[['Hello Saturn',],]}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName,
        valueInputOption='RAW',
        body=values).execute()
    #values = result.get('values', [])

    #if not values:
    #    print('Data failed to add.')


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # google sample v
    #spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    spreadsheetId = '1K0V19lxMsIC7TzLTJ8AY8s7vjlIljpmK_5MuO2LopSI' # Harambot Test spreadsheet
    #rangeName = 'Class Data!A2:E'
    rangeName = 'Discord!A2:C'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Discord Name, Main Character Name:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))


if __name__ == '__main__':
    #main()
    #get_main_character_name('Mortivius (Peter)')
    add_character('Valorok', 'Warrior', 'Tank')
