import sys
import BCIT
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QStackedWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 320)

        self.schedulePage = ScheduleUI(self)
        self.launchPage = LaunchUI("2519", self)
        self.calendarPage = CalendarUI(self)
        self.addWidget(self.launchPage)
        self.addWidget(self.calendarPage)
        self.addWidget(self.schedulePage)

        self.startLaunchUI()

    def startScheduleUI(self, date):
        self.schedulePage.updateTable(date)
        self.setCurrentWidget(self.schedulePage)
        self.show()

    def startCalendarUI(self):
        self.setCurrentWidget(self.calendarPage)
        self.show()

    def startLaunchUI(self):
        self.setCurrentWidget(self.launchPage)
        self.show()


class ScheduleUI(QtWidgets.QWidget):
    def __init__(self, mainW):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()


        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.clicked.connect(mainW.startCalendarUI)
        self.roomScheduleTable = QtWidgets.QTableWidget()
        self.roomScheduleTable.setRowCount(13)
        self.roomScheduleTable.setColumnCount(34)
        self.roomScheduleTable.horizontalHeader().setDefaultSectionSize(45)

        self.layout.addWidget(self.roomScheduleTable)
        h_box.addWidget(self.backBtn)
        h_box.addStretch()
        self.layout.addLayout(h_box)
        self.setLayout(self.layout)

    def updateTable(self, date):
        self.roomSchedule = BCIT.QtGetSchedule(date)
        self.roomScheduleTable.setHorizontalHeaderLabels(self.roomSchedule.keys()[1:])
        self.roomScheduleTable.setVerticalHeaderLabels(self.roomSchedule['Room:'])

        for row in range(0, self.roomScheduleTable.rowCount()):
            for col, roomStatus in enumerate(self.roomSchedule.iloc[row][1:]):
                self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(roomStatus)))


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