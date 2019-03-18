import sys, lxml
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super().__init__()
        self.resize(480, 320)
        self.roomSchedule = self.getSchedule()

        self.schedulePage = ScheduleUI(self.roomSchedule)
        self.launchPage = LaunchUI()

        self.startLaunchUI()

    def getSchedule(self):
        url = 'https://studyrooms.lib.bcit.ca/day.php?year=2019&month=3&day=13&area=4'
        table = pd.read_html(url, attrs={'id': 'day_main'})[0]
        table = table.drop(['Room:.1'], axis=1)
        table = table.drop([13], axis=0)
        return table

    def startScheduleUI(self):
        self.setCentralWidget(self.schedulePage)
        self.show()

    def startLaunchUI(self):
        self.setCentralWidget(self.launchPage)
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


class LaunchUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.clock = DigitalClock()
        self.clock.move(0,0)


class DigitalClock(QtWidgets.QLCDNumber):
    def __init__(self):
        super().__init__()
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