import sys
import threading

import resources_rc
import config
import serialport

from Ui_main import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QThread, QTranslator, QTimer
from PyQt6 import QtGui

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

        self.setWindowIcon(QIcon(":Resources/icon/main.ico"))

        self.trans = QTranslator()

        config.init()
        self.serialUiInit()
        

        self.port = serialport.SerialPort()
        self.warningMsgBox = QMessageBox()
        self.warningMsgBox.setIcon(QMessageBox.Icon.Warning)
        self.warningMsgBox.setWindowTitle("Warning")
        self.warningMsgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.SerialSendRepeatTimer = QTimer()
        self.SerialSendRepeatTimer.timeout.connect(self.SerialSendRepeatTimerCb)

        self.CnLanguageAction.triggered.connect(self.serialLanguageSwitchCb)
        self.EnLanguageAction.triggered.connect(self.serialLanguageSwitchCb)

        self.SerialConnectComPushButton.clicked.connect(self.serialConnectComPushButtonCb)
        self.SerialSendPushButton.clicked.connect(self.serialSendComPushButtonCb)
        self.SerialReceiveClearPushButton.clicked.connect(self.serialReceiveClearPushButtonCb)

        self.SerialSendRepeatCheckBox.stateChanged.connect(self.SerialSendRepeatCheckCb)
        self.SerialSendRepeatDurationLineEdit.textChanged.connect(self.SerialSendRepeatDurationLineEditCb)

        self.SerialBaudrateComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialStopBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialDataBitcomboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialChecksumBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialReceiveHexCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialReceiveTimestampCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialSendHexCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialSendRepeatCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialSendLineFeedComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialSoftFlowControlCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlDSRDTRCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlRTSCTSCheckBox.stateChanged.connect(self.serialComConfigCb)
        

    def serialUiInit(self):
        self.trans.load(":Resources/translations/" + config.config_param["language"] +".qm")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

        self.SerialSendRepeatDurationLineEdit.setValidator(QtGui.QIntValidator(0, 100000))
        
        for action in self.MenuLanguage.actions():
            if action.text() == config.config_param["language"]:
                action.setChecked(True)
                action.setEnabled(False)
            else:
                action.setChecked(False)
                action.setEnabled(True)


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

    def serialConnectPortSwitch(self, en):
        res = False
        if en:
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
            if res:
                self.receiveSerialPortThread = SerialPortReceiveDataThread(self)
                self.receiveSerialPortThread.dataReceivedSignal.connect(self.readSerialPortDataSignalCb)
                self.receiveSerialPortThread.start()
        else:
            self.receiveSerialPortThread.stop()
            res = self.port.close()
        return res


    def serialConnectComPushButtonCb(self):
        if self.port.serial is None and self.SerialComboBox.currentText() != "":
            res = self.serialConnectPortSwitch(True)
            if res == True:
                self.SerialConnectComPushButton.setText("断开")
        elif self.port.serial is not None:
            res = self.serialConnectPortSwitch(False)
            if res == True:
                self.SerialConnectComPushButton.setText("连接COM")

    def serialBaudrateComboBoxCb(self):
        config.configini.setValue("baudrateIndex", self.SerialBaudrateComboBox.currentIndex())
        if self.port.serial is not None:
            self.serialConnectPortSwitch(False)
            self.serialConnectPortSwitch(True)

    def serialSendComPushButtonCb(self):
        if self.SerialSendTextEdit.toPlainText() == "":
            return
        self.port.write(str.encode(self.SerialSendTextEdit.toPlainText()))

    def readSerialPortDataSignalCb(self, data):
        self.SerialReceiveTextEdit.insertPlainText(data)

    def serialReceiveClearPushButtonCb(self):
        if self.SerialReceiveTextEdit.toPlainText() != "":
            self.SerialReceiveTextEdit.clear()


    def SerialSendRepeatCheckCb(self, value):
        if value != 0:
            self.SerialSendRepeatDurationLineEdit.setEnabled(False)
            self.SerialSendRepeatTimer.start(int(self.SerialSendRepeatDurationLineEdit.text()))
        else:
            self.SerialSendRepeatDurationLineEdit.setEnabled(True)
            self.SerialSendRepeatTimer.stop()

    def SerialSendRepeatTimerCb(self):
        sendData = self.SerialSendTextEdit.toPlainText()
        if sendData == "":
            return
        self.port.write(str.encode(sendData))

    def SerialSendRepeatDurationLineEditCb(self, value):
        if value == '0' or value == "":
            value = 1000
            self.SerialSendRepeatDurationLineEdit.setText("1000")
            self.warningMsgBox.setText("range:(1-100000)")
            self.warningMsgBox.exec()

        config.configini.setValue("sendRepeatentDuration", value)
        


    def serialComConfigCb(self, value):
        curObjectName = self.sender().objectName()
        if curObjectName == self.SerialBaudrateComboBox.objectName():
            config.configini.setValue("baudrateIndex", value)
        elif curObjectName == self.SerialStopBitComboBox.objectName():
            config.configini.setValue("stopBitIndex", value)
        elif curObjectName == self.SerialDataBitcomboBox.objectName():
            config.configini.setValue("dataBitIndex", value)
        elif curObjectName == self.SerialChecksumBitComboBox.objectName():
            config.configini.setValue("checkSumIndex", value)
        elif curObjectName == self.SerialReceiveHexCheckBox.objectName():
            config.configini.setValue("receiveHexEn", value)
        elif curObjectName == self.SerialReceiveTimestampCheckBox.objectName():
            config.configini.setValue("timestampEn", value)
        elif curObjectName == self.SerialSendHexCheckBox.objectName():
            config.configini.setValue("sendHexEn", value)
        elif curObjectName == self.SerialSendRepeatCheckBox.objectName():
            config.configini.setValue("sendRepeatenEn", value)
        elif curObjectName == self.SerialSendLineFeedComboBox.objectName():
            config.configini.setValue("sendLineFeedIndex", value)
        elif curObjectName == self.SerialSoftFlowControlCheckBox.objectName():
            config.configini.setValue("xonxoff", value)
        elif curObjectName == self.SerialHardFlowControlDSRDTRCheckBox.objectName():
            config.configini.setValue("dsrdtr", value)
        elif curObjectName == self.SerialHardFlowControlRTSCTSCheckBox.objectName():
            config.configini.setValue("rtscts", value)
        
        if self.port.serial is not None:
            self.serialConnectPortSwitch(False)
            self.serialConnectPortSwitch(True)

    def serialLanguageSwitchCb(self, value):
        if value == False:
            return
        curObjectName = self.sender().objectName()
        
        if curObjectName == self.CnLanguageAction.objectName():
                config.configini.setValue("language", self.CnLanguageAction.text())
                self.trans.load(":Resources/translations/zh_CN.qm")
        elif curObjectName == self.EnLanguageAction.objectName():
                config.configini.setValue("language", self.EnLanguageAction.text())
                self.trans.load(":Resources/translations/en.qm")

        for action in self.MenuLanguage.actions():
            if action.objectName() == curObjectName:
                action.setChecked(True)
                action.setEnabled(False)
            else:
                action.setChecked(False)
                action.setEnabled(True)

        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec())
