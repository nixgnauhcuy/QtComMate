import serial.tools.list_ports
from PyQt6.QtWidgets import QComboBox

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
            portList = [str(port) for port in serial.tools.list_ports.comports()]
            return portList
        except Exception as err:
            print("Error getting access to the serial device! The error message is:" + str(err))
