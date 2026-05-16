import logging
from serial.tools.list_ports import comports
from PyQt6.QtWidgets import QComboBox

logger = logging.getLogger(__name__)

class SerialPortComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.refreshPorts()

    def showPopup(self):
        self.clear()
        ports = self.getPortList()
        for index, port in enumerate(ports, start=1):
            self.insertItem(index, port)
        super().showPopup()

    def refreshPorts(self):
        self.clear()
        ports = self.getPortList()
        for index, port in enumerate(ports, start=1):
            self.insertItem(index, port)

    def getPortList(self):
        try:
            portList = [str(port) for port in comports()]
            return portList
        except Exception:
            logger.exception("Error getting access to serial devices")
            return []
