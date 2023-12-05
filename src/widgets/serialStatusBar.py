from enum import Enum
from PyQt6.QtWidgets import QStatusBar, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import pyqtSignal

class SerialStatusBar(QStatusBar):

    class SerialStatusBarClickEvent(Enum):
        SettingClickEvent = 0

    serialStatusBarClickEventSignal = pyqtSignal(SerialStatusBarClickEvent, object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settingPushButton = QPushButton()
        self.connStatusLabel = QLabel()
        self.sendByteCountLabel = QLabel("S:0")
        self.receiveByteCountLabel = QLabel("R:0")
        self.tmpLabel = QLabel() # tmp 
        self.settingPushButton.setIcon(QIcon(":img/img/setting.png"))
        self.settingPushButton.setStyleSheet("border:none")
        self.connStatusLabel.setPixmap(QPixmap(":img/img/unconnect.png"))
        self.addPermanentWidget(self.settingPushButton, stretch=0)
        self.addPermanentWidget(self.tmpLabel, stretch=4) # tmp
        self.addPermanentWidget(self.sendByteCountLabel, stretch=1)
        self.addPermanentWidget(self.receiveByteCountLabel, stretch=1)
        self.addPermanentWidget(self.connStatusLabel, stretch=0)

        self.settingPushButton.clicked.connect(self.SerialStatusBarClickEventCb)

        
    def SerialStatusBarClickEventCb(self):
        self.serialStatusBarClickEventSignal.emit(self.SerialStatusBarClickEvent.SettingClickEvent, '')