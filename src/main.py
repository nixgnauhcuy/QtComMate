import sys
import threading

import main_qrc
import config
import serialport

from Ui_main import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QThread


class SerialPortReceiveDataThread(QThread):
    dataReceivedSignal = pyqtSignal(str)

    def __init__(self, parent):
        super(SerialPortReceiveDataThread, self).__init__()
        self.parent = parent
        self.thread = threading.Event()

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while True:
            if self.stopped():
                break
            try:
                data = self.parent.port.read()
                if data:
                    self.dataReceivedSignal.emit(data)
            except Exception as e:
                print(e)
                continue


class MyPyQT_Form(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(":/icon/main.ico"))

        config.init()
        self.serialUiInit()

        self.port = serialport.SerialPort()

        self.SerialConnectComPushButton.clicked.connect(self.serialConnectComPushButtonCb)
        self.SerialSendPushButton.clicked.connect(self.serialSendComPushButtonCb)

    def serialUiInit(self):
        self.SerialBaudrateComboBox.setCurrentIndex(int(config.config_param["baudrateIndex"]))
        self.SerialStopBitComboBox.setCurrentIndex(int(config.config_param["stopBitIndex"]))
        self.SerialDataBitcomboBox.setCurrentIndex(int(config.config_param["dataBitIndex"]))
        self.SerialChecksumBitComboBox.setCurrentIndex(int(config.config_param["checkSumIndex"]))
        self.SerialReceiveHexCheckBox.setChecked(int(config.config_param["receiveHexEn"]))
        self.SerialReceiveTimestampCheckBox.setChecked(int(config.config_param["timestampEn"]))
        self.SerialSendHexCheckBox.setChecked(int(config.config_param["sendHexEn"]))
        self.SerialSendRepeatCheckBox.setChecked(int(config.config_param["sendRepeatenEn"]))
        self.SerialSendRepeatDurationLineEdit.setText(config.config_param["sendRepeatentDuration"])
        self.SerialSendLineFeedComboBox.setCurrentIndex(int(config.config_param["sendLineFeedIndex"]))
        self.SerialSoftFlowControlCheckBox.setChecked(int(config.config_param["xonxoff"]))
        self.SerialHardFlowControlDSRDTRCheckBox.setChecked(int(config.config_param["dsrdtr"]))
        self.SerialHardFlowControlRTSCTSCheckBox.setChecked(int(config.config_param["rtscts"]))

    def serialConnectComPushButtonCb(self):
        if self.port.serial is None and self.SerialComboBox.currentText() != "":
            port = self.SerialComboBox.currentText().split()[0]
            baudrate = int(self.SerialBaudrateComboBox.currentText())
            stopBit = float(self.SerialStopBitComboBox.currentText())
            dataBit = int(self.SerialDataBitcomboBox.currentText())
            checkSum = self.SerialChecksumBitComboBox.currentText()
            xonxoff = int(self.SerialSoftFlowControlCheckBox.isChecked())
            rtscts = int(self.SerialHardFlowControlRTSCTSCheckBox.isChecked())
            dsrdtr = int(self.SerialHardFlowControlDSRDTRCheckBox.isChecked())

            res = self.port.open(port, baudrate, dataBit,
                                 checkSum[0], stopBit, xonxoff, rtscts, dsrdtr)
            self.receiveSerialPortThread = SerialPortReceiveDataThread(self)
            self.receiveSerialPortThread.dataReceivedSignal.connect(self.readSerialPortDataSignalCb)
            self.receiveSerialPortThread.start()
            if res == True:
                self.SerialConnectComPushButton.setText("断开")
        elif self.port.serial is not None:
            self.SerialConnectComPushButton.setText("连接COM")
            self.receiveSerialPortThread.stop()
            self.port.close()

    def serialSendComPushButtonCb(self):
        if self.SerialSendTextEdit.toPlainText() == "":
            return
        self.port.write(str.encode(self.SerialSendTextEdit.toPlainText()))

    def readSerialPortDataSignalCb(self, data):
        self.SerialReceiveTextEdit.insertPlainText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec())
