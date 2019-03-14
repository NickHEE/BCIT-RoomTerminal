import sys, lxml
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()
        self.resize(480, 320)
        self.roomSchedule = self.getSchedule()
        self.setupUi()

    def setupUi(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.roomScheduleTable = QtWidgets.QTableWidget()
        self.roomScheduleTable.setRowCount(13)
        self.roomScheduleTable.setColumnCount(34)
        self.roomScheduleTable.horizontalHeader().setDefaultSectionSize(45)
        self.roomScheduleTable.setHorizontalHeaderLabels(self.roomSchedule.keys()[1:])
        self.roomScheduleTable.setVerticalHeaderLabels(self.roomSchedule['Room:'])

        for row in range(0, self.roomScheduleTable.rowCount()):
            for col, roomStatus in enumerate(self.roomSchedule.iloc[row][1:]):
                self.roomScheduleTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(roomStatus)))

        self.layout.addWidget(self.roomScheduleTable)
        self.show()

    def getSchedule(self):
        url = 'https://studyrooms.lib.bcit.ca/day.php?year=2019&month=3&day=13&area=4'
        table = pd.read_html(url, attrs={'id': 'day_main'})[0]
        table = table.drop(['Room:.1'], axis=1)
        table = table.drop([13], axis=0)
        return table


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())



