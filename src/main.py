import sys
import threading
import re
import resources_rc
import config
import serialport
import binascii

from Ui_main import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt6.QtGui import QIcon, QPixmap
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
                    if self.parent.SerialReceiveHexCheckBox.isChecked():
                        data_hex = str(binascii.b2a_hex(data))[2:-1]
                        data_hex_spaced = ' ' + ' '.join([data_hex[i:i+2] for i in range(0, len(data_hex), 2)])
                        self.dataReceivedSignal.emit(data_hex_spaced)
                    else:
                        self.dataReceivedSignal.emit(data.decode('iso-8859-1'))
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
        
        self.hex_pattern = re.compile(r'^[0-9a-fA-F]+$')

        self.sendCountSum = 0
        self.receiveCountSum = 0

        self.port = serialport.SerialPort()
        self.warningMsgBox = QMessageBox()
        self.warningMsgBox.setIcon(QMessageBox.Icon.Warning)
        self.warningMsgBox.setWindowTitle("Warning")
        self.warningMsgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.SerialSendRepeatTimer = QTimer()
        self.SerialSendRepeatTimer.timeout.connect(self.serialSendRepeatTimerCb)

        self.CnLanguageAction.triggered.connect(self.serialLanguageSwitchCb)
        self.EnLanguageAction.triggered.connect(self.serialLanguageSwitchCb)

        self.SerialConnectComPushButton.clicked.connect(self.serialConnectComPushButtonCb)
        self.SerialSendPushButton.clicked.connect(self.serialSendComPushButtonCb)
        self.SerialSendTextEdit.document().contentsChange.connect(self.serialSendTextChangeCb)
        self.SerialSendClearPushButton.clicked.connect(self.serialSendClearPushButtonCb)
        self.SerialReceiveClearPushButton.clicked.connect(self.serialReceiveClearPushButtonCb)

        self.SerialSendRepeatCheckBox.stateChanged.connect(self.serialSendRepeatCheckCb)
        self.SerialSendRepeatDurationLineEdit.textChanged.connect(self.serialSendRepeatDurationLineEditCb)
        self.SerialReceiveHexCheckBox.stateChanged.connect(self.serialReceiveHexCheckBoxCb)
        self.SerialSendHexCheckBox.stateChanged.connect(self.serialSendHexCheckBoxCb)

        self.SerialBaudrateComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialStopBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialDataBitcomboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialChecksumBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialReceiveTimestampCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialSendLineFeedComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialSoftFlowControlCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlDSRDTRCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlRTSCTSCheckBox.stateChanged.connect(self.serialComConfigCb)
        

    def serialUiInit(self):
        self.trans.load(":Resources/translations/" + config.config_param["language"] +".qm")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

        self.connStatusLabel = QLabel()
        self.sendByteCountLabel = QLabel("S:0")
        self.receiveByteCountLabel = QLabel("R:0")
        self.tmpLabel = QLabel() # tmp 
        self.connStatusLabel.setPixmap(QPixmap(":Resources/img/unconnect.png"))
        self.SerialStatusBar.addPermanentWidget(self.connStatusLabel, stretch=0)
        self.SerialStatusBar.addPermanentWidget(self.tmpLabel, stretch=4) # tmp
        self.SerialStatusBar.addPermanentWidget(self.sendByteCountLabel, stretch=1)
        self.SerialStatusBar.addPermanentWidget(self.receiveByteCountLabel, stretch=1)


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

            res = self.port.open(port, baudrate, dataBit, checkSum[0], stopBit, xonxoff, rtscts, dsrdtr)
            if res:
                self.receiveSerialPortThread = SerialPortReceiveDataThread(self)
                self.receiveSerialPortThread.dataReceivedSignal.connect(self.readSerialPortDataSignalCb)
                self.receiveSerialPortThread.start()
        else:
            self.receiveSerialPortThread.stop()
            self.SerialSendRepeatCheckBox.setChecked(False) # disconnect need to close send timer
            res = self.port.close()
        return res


    def serialConnectComPushButtonCb(self):
        if self.port.serial is None and self.SerialComboBox.currentText() != "":
            self.connStatusLabel.setPixmap(QPixmap(":Resources/img/connect.png"))
            res = self.serialConnectPortSwitch(True)
            if res == True:
                if self.CnLanguageAction.isChecked():
                    self.SerialConnectComPushButton.setText("断开")
                else:
                    self.SerialConnectComPushButton.setText("Disconnect")
        elif self.port.serial is not None:
            self.connStatusLabel.setPixmap(QPixmap(":Resources/img/unconnect.png"))
            res = self.serialConnectPortSwitch(False)
            if res == True:
                if self.CnLanguageAction.isChecked():
                    self.SerialConnectComPushButton.setText("连接COM")
                else:
                    self.SerialConnectComPushButton.setText("Connect")

    def serialSendPortWirte(self, data):
        self.sendCountSum += len(data)
        self.sendByteCountLabel.setText("S:" + str(self.sendCountSum))
        self.port.write(data)

    def serialSendComPushButtonCb(self):
        if self.SerialSendTextEdit.toPlainText() == "":
            return
        if self.SerialSendHexCheckBox.isChecked() == True:
            hex_string = self.SerialSendTextEdit.toPlainText().replace(' ', '')

            data = ''
            for x in range(0, len(hex_string), 2):
                data += chr(int(hex_string[x:x+2], 16))
    
            self.serialSendPortWirte(bytes(data,encoding='utf-8'))
        else:
            self.serialSendPortWirte(str.encode(self.SerialSendTextEdit.toPlainText()))

    def serialSendClearPushButtonCb(self):
        self.sendCountSum = 0
        self.sendByteCountLabel.setText("S:0")
        self.SerialSendTextEdit.clear()


    def readSerialPortDataSignalCb(self, data):
        self.receiveCountSum +=  len(data)
        self.receiveByteCountLabel.setText("R:" + str(self.receiveCountSum))
        self.SerialReceiveTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.SerialReceiveTextEdit.insertPlainText(data)

    def serialReceiveClearPushButtonCb(self):
        self.receiveCountSum = 0
        self.receiveByteCountLabel.setText("R:0")
        if self.SerialReceiveTextEdit.toPlainText() != "":
            self.SerialReceiveTextEdit.clear()

    def serialSendTextChangeCb(self, position, charsRemoved, charsAdded):
        if not self.SerialSendHexCheckBox.isChecked():
            return
        
        if charsAdded > 0:
            beforeText = self.SerialSendTextEdit.toPlainText()[:position]
            text = self.SerialSendTextEdit.toPlainText()[position:position+charsAdded]
            afterText = self.SerialSendTextEdit.toPlainText()[position+charsAdded:]
            
            newText = ""
            
            for letter in text:
                if self.hex_pattern.match(letter):
                    newText += letter

            newText = beforeText+newText+afterText

            cursor = self.SerialSendTextEdit.textCursor()

            old_position = cursor.position()
            self.SerialSendTextEdit.document().blockSignals(True)
            self.SerialSendTextEdit.setPlainText(newText)
            self.SerialSendTextEdit.document().blockSignals(False)

            cursor.setPosition(old_position)
            self.SerialSendTextEdit.setTextCursor(cursor)


    def serialSendRepeatCheckCb(self, value):
        if value != 0:
            self.SerialSendRepeatDurationLineEdit.setEnabled(False)
            self.SerialSendRepeatTimer.start(int(self.SerialSendRepeatDurationLineEdit.text()))
        else:
            self.SerialSendRepeatDurationLineEdit.setEnabled(True)
            self.SerialSendRepeatTimer.stop()

    def serialSendRepeatTimerCb(self):
        if self.SerialSendTextEdit.toPlainText() == "":
            return
        if self.SerialSendHexCheckBox.isChecked() == True:
            hex_string = self.SerialSendTextEdit.toPlainText().replace(' ', '')

            data = ''
            for x in range(0, len(hex_string), 2):
                data += chr(int(hex_string[x:x+2], 16))
    
            self.serialSendPortWirte(bytes(data,encoding='utf-8'))
        else:
            self.serialSendPortWirte(str.encode(self.SerialSendTextEdit.toPlainText()))


    def serialSendRepeatDurationLineEditCb(self, value):
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
        elif curObjectName == self.SerialReceiveTimestampCheckBox.objectName():
            config.configini.setValue("timestampEn", value)
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

    def serialReceiveHexCheckBoxCb(self, value):
        if value:
            text = self.SerialReceiveTextEdit.toPlainText()
            hex_list = [hex(ord(x))[2:] for x in text]
            send_text_to_hex = ' '.join(hex_list)
            self.SerialReceiveTextEdit.setText(send_text_to_hex)
            self.SerialReceiveTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        else:
            hexText = self.SerialReceiveTextEdit.toPlainText().replace(' ', '')
            text = ' '.join([chr(int(hexText[i:i+2], 16)) for i in range(0, len(hexText), 2)]).replace(' ', '')
            self.SerialReceiveTextEdit.setText(text)
            self.SerialReceiveTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        config.configini.setValue("receiveHexEn", value)


    def serialSendHexCheckBoxCb(self, value):
        if value:
            text = self.SerialSendTextEdit.toPlainText()
            hex_list = [hex(ord(x))[2:] for x in text]
            send_text_to_hex = ' '.join(hex_list)
            self.SerialSendTextEdit.setText(send_text_to_hex)
            self.SerialSendTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        else:
            hexText = self.SerialSendTextEdit.toPlainText().replace(' ', '')
            text = ' '.join([chr(int(hexText[i:i+2], 16)) for i in range(0, len(hexText), 2)]).replace(' ', '')
            self.SerialSendTextEdit.setText(text)
            self.SerialSendTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        config.configini.setValue("sendHexEn", value)
    

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
