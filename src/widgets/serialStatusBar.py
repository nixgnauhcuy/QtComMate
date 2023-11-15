from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtGui import QPixmap

class SerialStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.connStatusLabel = QLabel()
        self.sendByteCountLabel = QLabel("S:0")
        self.receiveByteCountLabel = QLabel("R:0")
        self.tmpLabel = QLabel() # tmp 
        self.connStatusLabel.setPixmap(QPixmap(":img/img/unconnect.png"))
        self.addPermanentWidget(self.connStatusLabel, stretch=0)
        self.addPermanentWidget(self.tmpLabel, stretch=4) # tmp
        self.addPermanentWidget(self.sendByteCountLabel, stretch=1)
        self.addPermanentWidget(self.receiveByteCountLabel, stretch=1)