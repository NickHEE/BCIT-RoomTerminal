import sys, lxml
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QStackedWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 320)
        self.roomSchedule = self.getSchedule()

        self.schedulePage = ScheduleUI(self.roomSchedule)
        self.launchPage = LaunchUI("2519", self)
        self.calendarPage = CalendarUI(self)
        self.addWidget(self.launchPage)
        self.addWidget(self.calendarPage)
        self.addWidget(self.schedulePage)

        self.startLaunchUI()

    def getSchedule(self):
        url = 'https://studyrooms.lib.bcit.ca/day.php?year=2019&month=3&day=13&area=4'
        table = pd.read_html(url, attrs={'id': 'day_main'})[0]
        table = table.drop(['Room:.1'], axis=1)
        table = table.drop([13], axis=0)
        return table

    def startScheduleUI(self):
        #self.setCentralWidget(self.schedulePage)
        self.setCurrentWidget(self.schedulePage)
        self.show()

    def startCalendarUI(self):
        #self.setCentralWidget(self.calendarPage)
        self.setCurrentWidget(self.calendarPage)
        self.show()

    def startLaunchUI(self):
        #self.setCentralWidget(self.launchPage)
        self.setCurrentWidget(self.launchPage)
        self.show()


class ScheduleUI(QtWidgets.QWidget):
    def __init__(self, roomSchedule):
        super().__init__()

        self.roomSchedule = roomSchedule
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.roomScheduleTable = QtWidgets.QTableWidget()
        self.roomScheduleTable.setRowCount(13)
        self.roomScheduleTable.setColumnCount(34)
        self.roomScheduleTable.horizontalHeader().setDefaultSectionSize(45)
        self.roomScheduleTable.setHorizontalHeaderLabels(self.roomSchedule.keys()[1:])
        self.roomScheduleTable.setVerticalHeaderLabels(self.roomSchedule['Room:'])

        self.updateTable()
        self.layout.addWidget(self.roomScheduleTable)

    def updateTable(self):
        for row in range(0, self.roomScheduleTable.rowCount()):
            for col, roomStatus in enumerate(self.roomSchedule.iloc[row][1:]):
                self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(roomStatus)))


class CalendarUI(QtWidgets.QWidget):
    def __init__(self, mainW):
        super().__init__()

        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.clicked[QtCore.QDate].connect(self.showDate)
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

        self.layout.addWidget(self.room, 1, alignment=QtCore.Qt.AlignCenter, )
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