import sys

from PyQt5 import QtWidgets

from checkstatisticsmainwindow import CheckStatisticsMainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setOrganizationName("BMSTU")
    QtWidgets.QApplication.setOrganizationDomain("bmstu.ru")

    window = CheckStatisticsMainWindow()
    window.show()
    sys.exit(app.exec())
