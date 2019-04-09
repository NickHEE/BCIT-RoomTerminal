"""
roomTerminal.py - Main GUI application used to display room status and book rooms
Nicholas Huttemann, 2019-04-08
"""

import sys, os, time
import BCIT
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import serial

# if using Pi, setup LED and signals
if os.name == 'posix':
    from gpiozero import LED, RGBLED
    led = RGBLED(red=16, green=20, blue=21, active_high=False, initial_value=(0,0,1))
    roomAvailableSignal = LED(5)
    roomUnavailableSignal = LED(6)


class MainWindow(QtWidgets.QStackedWidget):
    """Main Window that contains the currently displayed UI"""

    def __init__(self, room='1104', led=None, roomAvailableSignal=None, roomUnavailableSignal=None):
        """
        Setup all the various UI's
        room: BCIT SW1 room to be monitored (attached room)
        led: Pi Signal - Room status LED
        roomAvailableSignal: Pi -> DE0-nano signal - Indicates room is currently empty
        roomUnavailableSignal: Pi -> DE0-nanp signal - Indicates room is currently booked
        """
        super().__init__()
        self.resize(480, 320)

        self.booking = None
        self.attachedRoom = room
        self.led = led
        self.roomAvailableSignal = roomAvailableSignal
        self.roomUnavailableSignal = roomUnavailableSignal

        # Initialize UI's
        self.schedulePage = ScheduleUI(self)
        self.launchPage = LaunchUI(self.attachedRoom, self)
        self.calendarPage = CalendarUI(self)
        self.loginPage = LoginUI(self)
        self.bookPage = BookUI(self)
        self.addWidget(self.launchPage)
        self.addWidget(self.calendarPage)
        self.addWidget(self.schedulePage)
        self.addWidget(self.loginPage)
        self.addWidget(self.bookPage)

        # Get the status of the attached room. Set a timer to update every minute
        table = BCIT.QtGetSchedule(QtCore.QDate.currentDate())
        self.attachedRoomSchedule = table.loc[self.attachedRoom+'(6)']
        self.updateAttachedRoomStatus()
        self.statusTimer = QtCore.QTimer(self)
        self.statusTimer.timeout.connect(self.updateAttachedRoomStatus)
        self.statusTimer.start(60000)
        self.startLaunchUI()

    def updateAttachedRoomStatus(self):
        """ Determine if the currently attached room is booked or not """

        tNow = datetime.now()
        hr = str(tNow.hour)
        m = str(tNow.minute)
        if int(hr) < 10:
            hr = '0' + hr
        if int(m) < 30:
            m = '00'
        else:
            m = '30'

        # Change the clock background colour according to the room status. If on the Pi, change LED colour as well
        status = self.attachedRoomSchedule[hr+':'+m]
        if str(status) == 'nan':
            self.launchPage.clock.setStyleSheet("background-color : rgb(174, 232, 155)")
            if os.name == 'posix':
                self.led.color = (0, 1, 0)
                self.roomAvailableSignal.blink(on_time=0.001, off_time=0.001, n=1)
        else:
            self.launchPage.clock.setStyleSheet("background-color : rgb(229, 170, 112)")
            if os.name == 'posix':
                self.led.color = (1, 0, 0)
                self.roomUnavailableSignal.blink(on_time=0.001, off_time=0.001, n=1)

    """ Methods to transition between the different UIs """
    def startScheduleUI(self, date=None, update=True):
        if update:
            self.schedulePage.updateTable(date)
            time.sleep(0.25)
        self.setCurrentWidget(self.schedulePage)
        self.show()

    def backToScheduleUI(self):
        self.setCurrentWidget(self.schedulePage)
        if os.name == 'posix':
            self.loginPage.UART.close()
        self.show()

    def startCalendarUI(self):
        self.setCurrentWidget(self.calendarPage)
        self.show()

    def startLaunchUI(self):
        self.setCurrentWidget(self.launchPage)
        self.show()

    def startLoginUI(self, booking):
        self.setCurrentWidget(self.loginPage)
        self.loginPage.booking = booking
        if os.name == 'posix':
            self.loginPage.UART.open()
        print(booking)

    def startBookUI(self, booking, session):
        self.setCurrentWidget(self.bookPage)
        self.bookPage.booking = booking
        self.bookPage.session = session
        self.bookPage.updateUI()


class ScheduleUI(QtWidgets.QWidget):
    """ UI Responsible for displaying the room schedule Data Frame fetched from BCIT """

    def __init__(self, mainW):
        super().__init__()

        self.date = None
        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()

        # Setup Widgets
        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.clicked.connect(mainW.startCalendarUI)
        self.roomScheduleTable = QtWidgets.QTableWidget()
        self.roomScheduleTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.roomScheduleTable.setRowCount(13)
        self.roomScheduleTable.setColumnCount(34)
        self.roomScheduleTable.horizontalHeader().setDefaultSectionSize(52)
        self.roomScheduleTable.verticalHeader().setDefaultSectionSize(35)
        self.roomScheduleTable.itemClicked.connect(lambda item: self.onClick(item, mainW))

        # Add Widgets to layouts
        self.layout.addWidget(self.roomScheduleTable)
        h_box.addWidget(self.backBtn)
        h_box.addStretch()
        self.layout.addLayout(h_box)
        self.setLayout(self.layout)

    def onClick(self, item, mainW):
        """ Triggers when the user selects a timeslot from the schedule. Asks for confirmation and calculates
        the maximum length of a booking for the timeslot. """

        roomNum = self.roomSchedule.iloc[item.row()].name[0:4]
        time = self.roomSchedule.iloc[item.row()].index[item.column()]
        maxLen = sum(1 for t in self.roomSchedule.iloc[item.row()][item.column():item.column() + 4] if type(t) is not str)
        assert(maxLen >= 1)

        prompt = QtWidgets.QMessageBox.question(self, 'Room Terminal',
                                                'Do you want to book {} at {}?'.format(roomNum, time),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)

        if prompt == QtWidgets.QMessageBox.Yes and item.flags() & QtCore.Qt.ItemIsEnabled:
            mainW.startLoginUI( (roomNum, time, self.date, maxLen) )
        else:
            pass

    def updateTable(self, date):
        """ Fetch room availability data for a specific date from BCIT and update the room schedule table """

        # Get current date and selected date
        self.date = date
        dNow = QtCore.QDate.currentDate()
        tNow = datetime.now()
        print(date, dNow)

        # Set Room Numbers and Times as headers in the table
        self.roomSchedule = BCIT.QtGetSchedule(date)
        self.roomScheduleTable.setHorizontalHeaderLabels(self.roomSchedule.keys())
        self.roomScheduleTable.setVerticalHeaderLabels(self.roomSchedule.index.values)

        # Iterate through every time slot in the fetched schedule and updated associated cell in the table
        for row in range(0, self.roomScheduleTable.rowCount()):
            for col, roomStatus in enumerate(self.roomSchedule.iloc[row]):
                tCell = datetime.strptime(self.roomSchedule.keys()[col], '%H:%M')

                # Test for Illegal booking dates
                if (date < dNow) or \
                (((tCell.hour < tNow.hour) or
                (tCell.hour == tNow.hour and tCell.minute < tNow.minute)) and not (date > dNow)):
                    # Set cell colour to grey
                    self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(''))
                    self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(160, 160, 160))

                    # Disable illegal cells
                    flags = self.roomScheduleTable.item(row, col).flags()
                    flags &= ~QtCore.Qt.ItemIsSelectable
                    flags &= ~QtCore.Qt.ItemIsEnabled
                    self.roomScheduleTable.item(row, col).setFlags(flags)

                # Time is legal, determine if booked or not booked
                else:
                    # Not Booked
                    if str(roomStatus) == 'nan':
                        # Set cell colour to green
                        self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(''))
                        self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(130, 213, 130))
                    # Booked
                    else:
                        # Set cell colour to orange
                        self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(roomStatus)))
                        self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(255, 204, 153))

                        # Disable booked cells
                        flags = self.roomScheduleTable.item(row, col).flags()
                        flags &= ~QtCore.Qt.ItemIsSelectable
                        flags &= ~QtCore.Qt.ItemIsEnabled
                        self.roomScheduleTable.item(row, col).setFlags(flags)


class CalendarUI(QtWidgets.QWidget):
    """ Qt5 Calendar widget used to select the date to view bookings for """

    def __init__(self, mainW):
        super().__init__()

        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.clicked[QtCore.QDate].connect(mainW.startScheduleUI)
        self.backBtn = QtWidgets.QPushButton('Back')
        self.backBtn.clicked.connect(mainW.startLaunchUI)

        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.backBtn)
        h_box.addStretch()
        self.layout.addWidget(self.calendar, 4)
        self.layout.addLayout(h_box)
        self.setLayout(self.layout)

    def showDate(self, date):
        print(date)


class LoginUI(QtWidgets.QWidget):
    """ UI that allows a BCIT student to login to the booking system. If using the Pi, allows user to enter
    ID / PW from keypad """

    def __init__(self, mainW):
        super().__init__()

        self.booking = None

        # If on the Pi, setup a serial connection to read incoming ascii characters. Gets a char every .2 sec
        if os.name == 'posix':
            self.UART = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=0.1)
            self.UART.close()
            charFetcher = QtCore.QTimer(self)
            charFetcher.timeout.connect(self.getChar)
            charFetcher.start(200)

        # Setup Widgets and layout
        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()
        v_boxInner = QtWidgets.QVBoxLayout()

        self.studentNumTxt = QtWidgets.QLabel('Student Number')
        self.studentNumBox = QtWidgets.QLineEdit()
        self.studentNumBox.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                         QtWidgets.QSizePolicy.Expanding)
        f = self.studentNumBox.font()
        f.setPointSize(16)
        self.studentNumBox.setFont(f)
        self.studentNumTxt.setFont(f)

        self.passwordTxt = QtWidgets.QLabel('Password')
        self.passwordBox = QtWidgets.QLineEdit()
        self.passwordBox.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                       QtWidgets.QSizePolicy.Expanding)
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordBox.setFont(f)
        self.passwordTxt.setFont(f)

        self.loginBtn = QtWidgets.QPushButton('Login')
        self.loginBtn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                    QtWidgets.QSizePolicy.Expanding)
        self.loginBtn.clicked.connect(lambda _: self.login(mainW))
        f.setPointSize(14)
        self.loginBtn.setFont(f)

        v_boxInner.addWidget(self.studentNumTxt, 2 ,alignment=QtCore.Qt.AlignCenter)
        v_boxInner.addWidget(self.studentNumBox, 3)
        v_boxInner.addWidget(self.passwordTxt, 2, alignment=QtCore.Qt.AlignCenter)
        v_boxInner.addWidget(self.passwordBox, 3)
        v_boxInner.addWidget(self.loginBtn, 2)
        h_box.addLayout(v_boxInner, 1)

        self.tapImg = QtGui.QPixmap('BCIT.png')
        self.tapImgLbl = QtWidgets.QLabel()
        self.tapImgLbl.setPixmap(self.tapImg)
        h_box.addWidget(self.tapImgLbl, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addLayout(h_box, 5)
        self.layout.addStretch(1)

        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.clicked.connect(mainW.backToScheduleUI)
        h_box2.addWidget(self.backBtn)
        h_box2.addStretch()
        self.layout.addLayout(h_box2)
        self.setLayout(self.layout)

    def login(self, mainW):
        """ Attempt to login to the BCIT Booking system. If successful, continue to the booking UI """
        try:
            session = BCIT.BCITStudySession(login=self.studentNumBox.text(), password=self.passwordBox.text())
        except:
            msg = QtWidgets.QMessageBox.information(self, 'Room Terminal', 'Login Failed')
            return
        if os.name == 'posix':
            self.UART.close()
        self.studentNumBox.clear()
        self.passwordBox.clear()
        mainW.startBookUI(self.booking, session)

    def getChar(self):
        """ Get an ascii char and determine which box (ID or Password) to put the char into """
        if self.UART.is_open:
            if self.studentNumBox.hasFocus():
                c = self.UART.read(1)
                if c:
                    self.studentNumBox.setText(self.studentNumBox.text() + c.decode('ascii'))
            elif self.passwordBox.hasFocus():
                c = self.UART.read(1)
                if c:
                    self.passwordBox.setText(self.passwordBox.text() + c.decode('ascii'))


class BookUI(QtWidgets.QWidget):
    """ Final UI displayed before booking a room. Allows user to choose booking length and optional name """

    def __init__(self, mainW):
        super().__init__()

        self.booking = None
        self.session = None

        # Setup widgets and layout
        self.layout = QtWidgets.QVBoxLayout()
        h_boxB = QtWidgets.QHBoxLayout()

        self.bookingLbl = QtWidgets.QLabel()
        self.bookingLbl.setFont(QtGui.QFont('Times', 22))
        self.nameLbl = QtWidgets.QLabel('Optional Name:')
        self.nameLbl.setFont(QtGui.QFont('Times', 15))
        self.nameBox = QtWidgets.QLineEdit('roomTerminal')
        self.nameBox.setFixedWidth(150)
        self.nameBox.setFixedHeight(40)
        self.nameBox.setFont(QtGui.QFont('Times', 14))
        self.bookLengthLbl = QtWidgets.QLabel("Book For:")
        self.bookLengthLbl.setFont(QtGui.QFont('Times', 15))

        self.bookLengthDropDown = QtWidgets.QComboBox()
        self.bookLengthDropDown.setFixedWidth(150)
        self.bookLengthDropDown.setFixedHeight(40)
        self.bookLengthDropDown.setFont(QtGui.QFont('Times', 14))
        self.bookLengthTimes = ['0:30', '1:00', '1:30', '2:00']
        self.backBtn = QtWidgets.QPushButton('Back')
        self.bookBtn = QtWidgets.QPushButton('Book')
        self.bookBtn.clicked.connect(lambda _: self.book(mainW))
        self.backBtn.clicked.connect(lambda _: mainW.startScheduleUI(update=False))
        self.bookBtn.setFixedWidth(150)
        self.bookBtn.setFixedHeight(40)
        self.bookBtn.setFont(QtGui.QFont('Times', 16))

        self.layout.addWidget(self.bookingLbl, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.nameLbl, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.nameBox, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.bookLengthLbl, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.bookLengthDropDown, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.bookBtn, 3, alignment=QtCore.Qt.AlignCenter)
        h_boxB.addWidget(self.backBtn)
        h_boxB.addStretch()
        self.layout.addLayout(h_boxB, 3)
        self.setLayout(self.layout)

    def updateUI(self):
        """ Update book length selection widget"""
        self.bookLengthDropDown.clear()
        self.bookingLbl.setText('SW1-{} - {}'.format(self.booking[0], self.booking[1]))
        for t in range (0, self.booking[3]):
            self.bookLengthDropDown.addItem(self.bookLengthTimes[t])

    def book(self, mainW):
        """ Book specified timeslot in the BCIT booking system """

        # Prepare required booking data (Room, time, date, length)
        room = 'SW1-' + self.booking[0]
        t = self.booking[1]
        d = self.booking[2]
        l = (self.bookLengthDropDown.currentIndex()+1) * 30
        tBooking = datetime(year=d.year(),
                            month=d.month(),
                            day=d.day(),
                            hour=int(t[0:2]), minute=int(t[3:5]))

        # Put the booking information into a format that will be accepted by BCIT.
        booking = BCIT.Booking(date=tBooking, length=l, room=room,
                               user=self.session.loginData["NewUserName"],
                               name=self.nameBox.text())
        # Attempt to book the room
        if self.session.book(booking):
            msg = QtWidgets.QMessageBox.information(self, 'Room Terminal',
                                                    'Booking Successful!')
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Room Terminal',
                                                    'Booking failed, please try again')
        mainW.startLaunchUI()


class LaunchUI(QtWidgets.QWidget):
    """ Initial screen that displays when the program is launched.
    Shows the current time and attached room status """

    def __init__(self, room, mainW):
        super().__init__()

        #Setup widgets and layout
        self.layout = QtWidgets.QVBoxLayout()
        self.room = QtWidgets.QLabel("SW1-" + room,)
        self.room.setFont(QtGui.QFont('Times', 24))
        self.clock = DigitalClock(5, self)

        self.viewBookingsBtn = QtWidgets.QPushButton("View Room Bookings")
        self.viewBookingsBtn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        self.viewBookingsBtn.clicked.connect(mainW.startCalendarUI)
        f = self.viewBookingsBtn.font()
        f.setPointSize(14)
        self.viewBookingsBtn.setFont(f)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.viewBookingsBtn)

        self.layout.addWidget(self.room, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.clock, 6)
        self.layout.addLayout(h_box, 2)
        self.setLayout(self.layout)


class DigitalClock(QtWidgets.QLCDNumber):
    """ LCD Widget used to display the current time"""

    def __init__(self, numDigits, parent=None):
        super().__init__(numDigits, parent)
        self.showTime()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.resize(150,60)
        self.showTime()

    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        self.display(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Start a splash screen while the program loads
    img = QtGui.QPixmap('BCITsplash.png')
    splash = QtWidgets.QSplashScreen(img, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(img.mask())
    splash.show()

    # Parse attached room
    try:
        room = sys.argv[1]
    except:
        room = '1104'

    # Start in Pi mode, or windows mode
    if os.name == 'posix':
        main = MainWindow(room=room,
                          led=led,
                          roomAvailableSignal=roomAvailableSignal,
                          roomUnavailableSignal=roomUnavailableSignal)
    else:
        main = MainWindow(room=room)
    main.show()
    splash.finish(main)
    sys.exit(app.exec_())
