import serial
import serial.tools.list_ports

from PyQt6.QtWidgets import QComboBox


class SerialPort_ComBoBox(QComboBox):

    def __init__(self, parent=None):
        super(SerialPort_ComBoBox, self).__init__(parent)

    def showPopup(self):
        self.clear()
        ports = self.get_port_list(self)
        if ports is not None:
            index = 1
            for port in ports:
                self.insertItem(index, port)
                index += 1
        QComboBox.showPopup(self)

    @staticmethod
    def get_port_list(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            for port in port_list:
                yield str(port)
        except Exception as err:
            print(
                "Error getting access to the serial device! The error message is:" + str(err))
