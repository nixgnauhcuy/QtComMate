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
            return [str(port) for port in comports()]
        except Exception:
            logger.exception("Error getting access to serial devices")
            return []

    @staticmethod
    def resolve_port_display(port_device: str, port_hint: str = "") -> str:
        if not port_device:
            return ""

        try:
            available = list(comports())
        except Exception:
            logger.exception("Error resolving serial port")
            return ""

        for port in available:
            if port.device == port_device:
                return str(port)

        if port_hint:
            for port in available:
                if port_hint == str(port):
                    return str(port)

            hint_tail = port_hint.split(" - ", 1)[-1] if " - " in port_hint else port_hint
            for port in available:
                if hint_tail and hint_tail in str(port):
                    return str(port)

        return ""

    def select_port_display(self, display: str) -> bool:
        if not display:
            return False

        for index in range(self.count()):
            if self.itemText(index) == display:
                self.setCurrentIndex(index)
                return True

        self.insertItem(1, display)
        self.setCurrentIndex(1)
        return True
