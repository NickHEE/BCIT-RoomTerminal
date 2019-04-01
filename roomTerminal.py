import sys
import BCIT
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime, timedelta
import time


class MainWindow(QtWidgets.QStackedWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 320)

        self.booking = None
        self.schedulePage = ScheduleUI(self)
        self.launchPage = LaunchUI("2519", self)
        self.calendarPage = CalendarUI(self)
        self.loginPage = LoginUI(self)
        self.bookPage = BookUI(self)
        self.addWidget(self.launchPage)
        self.addWidget(self.calendarPage)
        self.addWidget(self.schedulePage)
        self.addWidget(self.loginPage)
        self.addWidget(self.bookPage)

        self.startLaunchUI()

    def startScheduleUI(self, date):
        self.schedulePage.updateTable(date)
        self.setCurrentWidget(self.schedulePage)
        print(date)
        self.show()

    def backToScheduleUI(self):
        self.setCurrentWidget(self.schedulePage)
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
        print(booking)

    def startBookUI(self, booking, session):
        self.setCurrentWidget(self.bookPage)
        self.bookPage.booking = booking
        self.bookPage.session = session
        self.bookPage.updateUI()

class ScheduleUI(QtWidgets.QWidget):
    def __init__(self, mainW):
        super().__init__()

        self.date = None
        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()

        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.clicked.connect(mainW.startCalendarUI)
        self.roomScheduleTable = QtWidgets.QTableWidget()
        self.roomScheduleTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.roomScheduleTable.setRowCount(13)
        self.roomScheduleTable.setColumnCount(34)
        self.roomScheduleTable.horizontalHeader().setDefaultSectionSize(45)
        self.roomScheduleTable.itemClicked.connect(lambda item: self.onClick(item, mainW))

        self.layout.addWidget(self.roomScheduleTable)
        h_box.addWidget(self.backBtn)
        h_box.addStretch()
        self.layout.addLayout(h_box)
        self.setLayout(self.layout)

    def onClick(self, item, mainW):
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
        self.date = date
        dNow = QtCore.QDate.currentDate()
        tNow = datetime.now()
        print(date, dNow)
        self.roomSchedule = BCIT.QtGetSchedule(date)
        self.roomScheduleTable.setHorizontalHeaderLabels(self.roomSchedule.keys())
        self.roomScheduleTable.setVerticalHeaderLabels(self.roomSchedule.index.values)

        for row in range(0, self.roomScheduleTable.rowCount()):
            for col, roomStatus in enumerate(self.roomSchedule.iloc[row]):
                tCell = datetime.strptime(self.roomSchedule.keys()[col], '%H:%M')
                if (date < dNow) or \
                (((tCell.hour < tNow.hour) or
                (tCell.hour == tNow.hour and tCell.minute < tNow.minute)) and not (date > dNow)):
                    self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(''))
                    self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(160, 160, 160))

                    flags = self.roomScheduleTable.item(row, col).flags()
                    flags &= ~QtCore.Qt.ItemIsSelectable
                    flags &= ~QtCore.Qt.ItemIsEnabled
                    self.roomScheduleTable.item(row, col).setFlags(flags)
                else:
                    if str(roomStatus) == 'nan':
                        self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(''))
                        self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(130, 213, 130))
                    else:
                        self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(roomStatus)))
                        self.roomScheduleTable.item(row, col).setBackground(QtGui.QColor(255, 204, 153))

                        flags = self.roomScheduleTable.item(row, col).flags()
                        flags &= ~QtCore.Qt.ItemIsSelectable
                        flags &= ~QtCore.Qt.ItemIsEnabled
                        self.roomScheduleTable.item(row, col).setFlags(flags)

class CalendarUI(QtWidgets.QWidget):
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
    def __init__(self, mainW):
        super().__init__()

        self.booking = None
        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()
        v_boxInner = QtWidgets.QVBoxLayout()

        self.studentNumTxt = QtWidgets.QLabel('Student Number')
        self.studentNumBox = QtWidgets.QLineEdit()
        self.passwordTxt = QtWidgets.QLabel('Password')
        self.passwordBox = QtWidgets.QLineEdit()
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginBtn = QtWidgets.QPushButton('Login')
        self.loginBtn.clicked.connect(lambda _: self.login(mainW))
        v_boxInner.addWidget(self.studentNumTxt, 1 ,alignment=QtCore.Qt.AlignCenter)
        v_boxInner.addWidget(self.studentNumBox, 3)
        v_boxInner.addWidget(self.passwordTxt, 1, alignment=QtCore.Qt.AlignCenter)
        v_boxInner.addWidget(self.passwordBox, 3)
        v_boxInner.addWidget(self.loginBtn)
        h_box.addLayout(v_boxInner, 1)

        self.tapImg = QtGui.QPixmap('tap.png')
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
        try:
            session = BCIT.BCITStudySession(login=self.studentNumBox.text(), password=self.passwordBox.text())
        except:
            msg = QtWidgets.QMessageBox.information(self, 'Room Terminal', 'Login Failed')
            return
        mainW.startBookUI(self.booking, session)


class BookUI(QtWidgets.QWidget):
    def __init__(self, mainW):
        super().__init__()


        self.booking = None
        self.session = None

        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        v_boxL = QtWidgets.QVBoxLayout()
        v_boxR = QtWidgets.QVBoxLayout()

        self.bookingLbl = QtWidgets.QLabel()
        self.nameLbl = QtWidgets.QLabel('Optional Name:')
        self.nameBox = QtWidgets.QLineEdit('roomTerminal')
        self.bookLengthLbl = QtWidgets.QLabel("Book For:")

        self.bookLengthDropDown = QtWidgets.QComboBox()
        self.bookLengthTimes = ['0:30', '1:00', '1:30', '2:00']
        self.bookBtn = QtWidgets.QPushButton('Book')
        self.bookBtn.clicked.connect(self.book)

        self.layout.addWidget(self.bookingLbl)
        self.layout.addLayout(h_box)
        h_box.addLayout(v_boxL,1)
        v_boxL.addWidget(self.nameLbl)
        v_boxL.addWidget(self.nameBox)
        h_box.addLayout(v_boxR,1)
        v_boxR.addWidget(self.bookLengthLbl)
        v_boxR.addWidget(self.bookLengthDropDown)
        self.layout.addWidget(self.bookBtn, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

    def updateUI(self):
        self.bookLengthDropDown.clear()
        self.bookingLbl.setText('SW1-{} - {}'.format(self.booking[0], self.booking[1]))
        for t in range (0, self.booking[3]):
            self.bookLengthDropDown.addItem(self.bookLengthTimes[t])
        print(self.bookLengthDropDown.currentIndex())

    def book(self):
        room = 'SW1-' + self.booking[0]
        t = self.booking[1]
        d = self.booking[2]
        l = (self.bookLengthDropDown.currentIndex()+1) * 30

        tBooking = datetime(year=d.year(),
                            month=d.month(),
                            day=d.day(),
                            hour=int(t[0:2]), minute=int(t[3:4]))

        booking = BCIT.Booking(date=tBooking, length=l, room=room, user=self.session.loginData["NewUserName"])
        print(booking)
        self.session.book(booking)


class LaunchUI(QtWidgets.QWidget):
    def __init__(self, room, mainW):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.room = QtWidgets.QLabel("SW1-" + room,)
        self.room.setFont(QtGui.QFont('Times', 24))
        self.clock = DigitalClock(5, self)

        self.bookNowBtn = QtWidgets.QPushButton("Book this room")
        self.viewBookingsBtn = QtWidgets.QPushButton("View room bookings")
        self.viewBookingsBtn.clicked.connect(mainW.startCalendarUI)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.bookNowBtn)
        h_box.addWidget(self.viewBookingsBtn)

        self.layout.addWidget(self.room, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.clock, 4)
        self.layout.addLayout(h_box)

        #self.clock = QtWidgets.QLCDNumber(7, self)
        #self.clock.display('1000')
        self.setLayout(self.layout)


class DigitalClock(QtWidgets.QLCDNumber):
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
    main = MainWindow()
    sys.exit(app.exec_())