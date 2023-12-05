from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(820, 550)
        mainWindow.setMinimumSize(QtCore.QSize(820, 550))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/main.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        mainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName("mainLayout")
        mainWindow.setCentralWidget(self.centralWidget)
        self.mainStatusBar = SerialStatusBar(mainWindow)
        self.mainStatusBar.setObjectName("mainStatusBar")
        mainWindow.setStatusBar(self.mainStatusBar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "QtComMate"))
from widgets.serialStatusBar import SerialStatusBar
