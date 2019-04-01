import requests
import json
import re

#from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import lxml


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
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116"
}


class BCITStudySession:
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
        self.session.headers.update(headers)
        res = self.session.post(urls['loginUrl'], data=self.loginData, **kwargs)

        # Test login
        if res.text.lower().find(self.loginData["NewUserName"].lower()) < 0:
            raise Exception("could not log onto BCIT '{}'"
                            " (did not find successful login string)".format(urls['loginUrl']))
        else:
            print(f"\n***Login as {self.loginData['NewUserName']} successful!***\n")

    def book(self, booking):
         response = self.session.post('https://studyrooms.lib.bcit.ca/edit_entry_handler.php', data=booking.bookData)


def QtGetSchedule(date):

    url = 'https://studyrooms.lib.bcit.ca/day.php?year={}&month={}&day={}&area=4'.format(date.year(),
                                                                                         date.month(),
                                                                                         date.day())
    table = pd.read_html(url, attrs={'id': 'day_main'}, skiprows=[14], index_col=0)[0]
    table = table.drop(['Room:.1'], axis=1)
    return table

class Booking:
    def __init__(self, date, length, room, user):
        self.length = length
        self.user = user
        self.startDate = date
        self.endDate = self.startDate + timedelta(minutes=int(length))
        self.startSeconds = int(self.startDate.hour) * 3600 + int(self.startDate.minute) * 60
        self.endSeconds = int(self.endDate.hour) * 3600 + int(self.endDate.minute) * 60
        self.room = rooms[room]
        self.bookData = bookTemplate
        self.BookingToJson()

    def __repr__(self):
        return(f'Date: {str(self.startDate.date())}\n'
               f'Time: {str(self.startDate.hour)}:{str(self.startDate.minute)} to '
               f'{str(self.endDate.hour)}:{str(self.endDate.minute)} \n'
               f'Room: {self.room}\n')

    def BookingToJson(self):
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


"""
class BCITStudySession:
    def __init__(self,
                 urls,
                 loginData,
                 bookings,
                 headers,
                 **kwargs):
        self.urls = urls
        self.loginData = loginData
        self.bookings = bookings
        self.headers = headers
        self.session = requests.Session()
        self.login(**kwargs)

    def login(self, **kwargs):
        self.session.headers.update(self.headers)
        res = self.session.post(self.urls['loginUrl'], data=self.loginData, **kwargs)

        # Test login
        if res.text.lower().find(self.loginData["NewUserName"].lower()) < 0:
            raise Exception(f"could not log onto BCIT '{self.urls['loginUrl']}'"
                            " (did not find successful login string)")
        else:
            print(f"\n***Login as {self.loginData['NewUserName']} successful!***\n")

    def book(self):
        page = self.session.get(self.urls['baseUrl']+f'day.php?year={self.bookings["start_year"]}&'
                                                            f'month={self.bookings["start_month"]}&'
                                                              f'day={self.bookings["start_day"]}&'
                                                             f'area=4') # **Add multiple areas later
        # **Change to use booking obj
        s_hr = int(self.bookings["start_seconds"]) // 3600
        s_m = int(self.bookings["start_seconds"]) % 3600 // 60
        e_hr = int(self.bookings["end_seconds"]) // 3600
        e_m = int(self.bookings["end_seconds"]) % 3600 // 60
        length = abs((e_hr - s_hr) + ((e_m - s_m) / 60))

        soup = BeautifulSoup(page.text, features='html.parser')
        emptyEntries = soup.find_all('td', {'class': 'new'})
        emptyStarts = [entry for entry in emptyEntries if f'hour={s_hr}&minute={s_m}' in entry.find('a')['href']]
        availableRooms = []

        for t in emptyStarts:
            seq = t.find_next_siblings('td', {'class': 'new'}, limit=(length * 2) - 1)
            if len(seq) == (length * 2 - 1):
                room = re.search(r'room=(\d+)', t.find('a')['href']).group(1)
                availableRooms.append(room)
                # print(f"Room {rooms[int(room)]} is available!\n")

        # **add room preference, check if room was booked?
        if availableRooms:
            availableRooms.sort(reverse=True)
            print("Room Found!")
            self.bookings['rooms[]'] = availableRooms[0]
            self.bookings['create_by'] = self.loginData['NewUserName']
            b = self.session.post('https://studyrooms.lib.bcit.ca/edit_entry_handler.php', data=self.bookings)
            print(b.text)
            self.session.close()
            return rooms[int(availableRooms[0])]
        else:
            self.session.close()
            return False


"""











