"""
BCIT.py - Module used for interacting with the BCIT online study room booking system
Nicholas Huttemann, 2019-04-08
"""

import requests
from datetime import timedelta
import pandas as pd


class BCITStudySession:
    """ Start a BCIT study room session using the python requests library """

    def __init__(self,
                 login,
                 password,
                 **kwargs):

        self.loginData = loginTemplate
        loginTemplate["NewUserName"] = login
        loginTemplate["NewUserPassword"] = password

        self.session = requests.Session()
        self.login(**kwargs)

    def login(self, **kwargs):
        # Set the headers so we appear to be a human
        self.session.headers.update(headers)

        # Post login data
        response = self.session.post(urls['loginUrl'], data=self.loginData, **kwargs)

        # Test for successful login
        if response.text.lower().find(self.loginData["NewUserName"].lower()) < 0:
            raise Exception("could not log onto BCIT '{}'"
                            " (did not find successful login string)".format(urls['loginUrl']))
        else:
            print("\n***Login as {} successful!***\n".format(self.loginData['NewUserName']))

    def book(self, booking):
        """ Post booking data and test for successful booking """

        response = self.session.post('https://studyrooms.lib.bcit.ca/edit_entry_handler.php', data=booking.bookData)
        if response.text.lower().find('scheduling conflict') != -1:
            return False
        else:
            return True


def QtGetSchedule(date):
    """ Fetch a room schedule for a particular day from the BCIT website.
        Uses a QtDate and returns a pandas dataframe containing the schedule """
    url = 'https://studyrooms.lib.bcit.ca/day.php?year={}&month={}&day={}&area=4'.format(date.year(),
                                                                                         date.month(),
                                                                                         date.day())
    table = pd.read_html(url, attrs={'id': 'day_main'}, skiprows=[14], index_col=0)[0]
    table = table.drop(['Room:.1'], axis=1)
    return table

class Booking:
    """ Create a study room booking with the required parameters"""

    def __init__(self, date, length, room, user, name):
        self.name = name
        self.length = length
        self.user = user
        self.startDate = date
        self.endDate = self.startDate + timedelta(minutes=int(length))
        self.startSeconds = int(self.startDate.hour) * 3600 + int(self.startDate.minute) * 60
        self.endSeconds = int(self.endDate.hour) * 3600 + int(self.endDate.minute) * 60
        self.room = rooms[room]
        self.bookData = bookTemplate
        self.BookingToJson()


    def BookingToJson(self):
        """ Convert booking data into a JSON format so it can easily be POST'd """

        self.bookData['start_day'] = self.startDate.day
        self.bookData['start_month'] = self.startDate.month
        self.bookData['start_year'] = self.startDate.year
        self.bookData['start_seconds'] = self.startSeconds
        self.bookData['end_day'] = self.endDate.day
        self.bookData['end_month'] = self.endDate.month
        self.bookData['end_year'] = self.endDate.year
        self.bookData['end_seconds'] = self.endSeconds
        self.bookData['rooms[]'] = self.room
        self.bookData['create_by'] = self.user
        self.bookData['name'] = self.name

# Mapping between online study room service number and actual room number
_rooms = {
    26: 'SW1-1104',
    27: 'SW1-1105',
    28: 'SW1-1106',
    29: 'SW1-2110',
    30: 'SW1-2111',
    31: 'SW1-2112',
    32: 'SW1-2113',
    33: 'SW1-2186',
    34: 'SW1-2187',
    35: 'SW1-2513',
    36: 'SW1-2515',
    37: 'SW1-2517',
    38: 'SW1-2519'
}
rooms = {v: k for k, v in _rooms.items()}

""" Data and templates used to interact with BCIT online services """

loginTemplate = {
  "NewUserName": "",
  "NewUserPassword": "",
  "returl": "https://studyrooms.lib.bcit.ca/",
  "TargetURL": "https://studyrooms.lib.bcit.ca/",
  "Action": "SetName"
}
bookTemplate = {
  "name": "Memes",
  "description": "",
  "start_day": "",
  "start_month": "",
  "start_year": "",
  "start_seconds": "",
  "end_day": "",
  "end_month": "",
  "end_year": "",
  "end_seconds": "",
  "area": "4",
  "rooms[]": "",
  "type":"I",
  "confirmed": "1",
  "returl": "https://studyrooms.lib.bcit.ca/",
  "create_by": "",
  "rep_id": "0",
  "edit_type": "series"
}

urls = {
    'baseUrl': 'https://studyrooms.lib.bcit.ca/',
    'loginUrl': 'https://studyrooms.lib.bcit.ca/admin.php',
    'bookUrl': 'https://studyrooms.lib.bcit.ca/edit_entry_handler.php'
}

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "en-US,en;q=0.9",
  "Cache-Control": "max-age=0",
  "Connection": "keep-alive",
  "Content-Type": "application/x-www-form-urlencoded",
  "Host": "studyrooms.lib.bcit.ca",
  "Origin": "https://studyrooms.lib.bcit.ca",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116"
}
