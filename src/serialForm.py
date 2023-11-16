import threading
import re
from enum import Enum
from time import sleep
from datetime import datetime
from ui.Ui_serial import Ui_serialForm
from serialPort import SerialPort
from config import ConfigManager

from PyQt6.QtWidgets import QFrame, QInputDialog, QLineEdit, QMessageBox, QFileDialog
from PyQt6.QtGui import QTextCursor, QIntValidator
from PyQt6.QtCore import pyqtSignal, QThread, QByteArray, QTimer

class SerialReceiveDataThread(QThread):
    dataReceivedSignal = pyqtSignal(bytes)

    def __init__(self, serial=None, rbuf=None):
        super(SerialReceiveDataThread, self).__init__()
        self.serial = serial
        self.rbuf = rbuf
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            try:
                data = self.serial.read()
                if data:
                    self.rbuf.append(data)
                    self.dataReceivedSignal.emit(data)
                else:
                    sleep(0.01)
            except Exception as e:
                print(e)
                continue

class SerialForm(QFrame, Ui_serialForm):

    def closeEvent(self, event):
        if self.serialHandle.isOpen():
            self.serialReceiveThread.stop()
            self.SerialSendRepeatTimer.stop()
            self.serialHandle.close()

    class SerialClickEvent(Enum):
        ConnectClickEvent = 0
        ReceiveClearClickEvent = 1
        ReceiveDataClickEvent = 2
        SendDataClickEvent = 3
        SendClearClickEvent = 4

    serialClickEventSignal = pyqtSignal(SerialClickEvent, object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.serialHandle = SerialPort()
        self.config = ConfigManager()
        self.configParam = self.config.Load()
        self.hex_pattern = re.compile(r'^[0-9a-fA-F]+$')

        self.UiInit()

        # receive
        self.receiveByteCount = 0
        self.receiveByteArray = QByteArray()

        self.serialConnectComPushButton.clicked.connect(self.SerialReceiveEventCb)
        self.serialReceiveClearPushButton.clicked.connect(self.SerialReceiveEventCb)
        self.serialReceiveHexCheckBox.stateChanged.connect(self.SerialReceiveParamChangedCb)
        self.serialBaudrateComboBox.currentIndexChanged.connect(self.SerialReceiveParamChangedCb)
        self.serialStopBitComboBox.currentIndexChanged.connect(self.SerialReceiveParamChangedCb)
        self.serialDataBitcomboBox.currentIndexChanged.connect(self.SerialReceiveParamChangedCb)
        self.serialChecksumBitComboBox.currentIndexChanged.connect(self.SerialReceiveParamChangedCb)
        self.serialReceiveTimestampCheckBox.stateChanged.connect(self.SerialReceiveParamChangedCb)

        # send
        self.sendByteCount = 0

        self.SerialSendRepeatTimer = QTimer()
        self.SerialSendRepeatTimer.timeout.connect(self.SerialSendRepeatTimerCb)

        self.serialSendPushButton.clicked.connect(self.SerialSendEventCb)
        self.serialSendClearPushButton.clicked.connect(self.SerialSendEventCb)
        self.serialSendRepeatCheckBox.stateChanged.connect(self.SerialSendEventCb)
        self.serialSendPlainTextEdit.document().contentsChange.connect(self.SerialSendTextChangeCb)
        
        self.serialSendRepeatDurationLineEdit.textChanged.connect(self.SerialSendParamChangedCb)
        self.serialSendHexCheckBox.stateChanged.connect(self.SerialSendParamChangedCb)
        self.serialSendLineFeedComboBox.currentIndexChanged.connect(self.SerialSendParamChangedCb)
        self.serialSoftFlowControlCheckBox.stateChanged.connect(self.SerialSendParamChangedCb)
        self.serialHardFlowControlDSRDTRCheckBox.stateChanged.connect(self.SerialSendParamChangedCb)
        self.serialHardFlowControlRTSCTSCheckBox.stateChanged.connect(self.SerialSendParamChangedCb)

        # File
        self.saveFileFlag = False
        self.serialFileSelectPushButton.clicked.connect(self.SerialSendEventCb)
        self.serialFileSendPushButton.clicked.connect(self.SerialSendEventCb)
        self.serialFilePathSaveSelectPushButton.clicked.connect(self.SerialSendEventCb)
        self.serialFileSavePushButton.clicked.connect(self.SerialSendEventCb)

    def SerialOnOffSwitch(self, en) -> bool:
        res = False
        if en:
            port = self.serialComboBox.currentText().split()[0]
            baudrate = int(self.serialBaudrateComboBox.currentText())
            stopBit = float(self.serialStopBitComboBox.currentText())
            dataBit = int(self.serialDataBitcomboBox.currentText())
            checkSum = self.serialChecksumBitComboBox.currentText()
            xonxoff = int(self.serialSoftFlowControlCheckBox.isChecked())
            rtscts = int(self.serialHardFlowControlRTSCTSCheckBox.isChecked())
            dsrdtr = int(self.serialHardFlowControlDSRDTRCheckBox.isChecked())
            res = self.serialHandle.open(port, baudrate, dataBit, checkSum[0], stopBit, xonxoff, rtscts, dsrdtr)
        else:
            res = self.serialHandle.close()
        return res
    
    def SerialSendDataPort(self, data):
        newline_mappings = {
            1: b'\r\n',  # 回车换行
            2: b'\r',    # 回车
            3: b'\n',    # 换行
        }
        newLine = newline_mappings.get(self.serialSendLineFeedComboBox.currentIndex(), b'')
        data += newLine

        self.sendByteCount += len(data)
        self.serialClickEventSignal.emit(self.SerialClickEvent.SendDataClickEvent, self.sendByteCount)
        self.serialHandle.write(data)

    # timer cb
    def SerialSendRepeatTimerCb(self):
        sendData = self.serialSendPlainTextEdit.toPlainText()
        if not sendData:
            return
        
        if self.serialSendHexCheckBox.isChecked():
            hex_string = sendData.replace(' ', '')
            if len(hex_string) % 2 != 0:
                padded_parts = [part.zfill(2) for part in hex_string[-1]]
                data = bytes.fromhex(hex_string[:-1] +"".join(padded_parts))
            else:
                data = bytes.fromhex(hex_string)
        else:
            data = sendData.encode('gbk')
        if self.serialHandle.serial is not None:
            self.SerialSendDataPort(data)
            
    
    def SerialPortReceiveDataSignalCb(self, data):
        self.receiveByteCount += len(data)
        self.serialClickEventSignal.emit(self.SerialClickEvent.ReceiveDataClickEvent, self.receiveByteCount)

        if self.serialReceiveHexCheckBox.isChecked():
            data = " " + " ".join([f"{b:02x}" for b in data])
        else:
            data = data.decode('gbk')  

        timestamp = ""
        if self.serialReceiveTimestampCheckBox.isChecked():
            timestamp = f"\n[{datetime.now():%Y-%m-%d %H:%M:%S.%f}]".rjust(23, ' ')[:-3] + ']\n'
        if self.saveFileFlag:
            self.saveFile.write(data)

        self.serialReceivePlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        self.serialReceivePlainTextEdit.insertPlainText(f"{timestamp}{data}")
        self.serialReceivePlainTextEdit.verticalScrollBar().setValue(
            self.serialReceivePlainTextEdit.verticalScrollBar().maximum()
        )


    def SerialReceiveEventCb(self):
        objectName = self.sender().objectName()
        if objectName == self.serialConnectComPushButton.objectName(): # connect btn
            ret = False
            if self.serialHandle.serial is None and self.serialComboBox.currentText():
                res = self.SerialOnOffSwitch(True)
                if res:
                    self.serialReceiveThread = SerialReceiveDataThread(self.serialHandle, self.receiveByteArray)
                    self.serialReceiveThread.dataReceivedSignal.connect(self.SerialPortReceiveDataSignalCb)
                    self.serialReceiveThread.start()
                    self.serialConnectComPushButton.setText(self.tr("Disconnect"))
                    ret = True
            elif self.serialHandle.serial is not None:
                self.serialConnectComPushButton.setText(self.tr("Connect"))
                self.SerialOnOffSwitch(False)
                self.serialReceiveThread.stop()
            self.serialClickEventSignal.emit(self.SerialClickEvent.ConnectClickEvent, ret)
        elif objectName == self.serialReceiveClearPushButton.objectName():  # clear receive btn
            self.serialReceivePlainTextEdit.clear()
            self.receiveByteCount = 0
            self.receiveByteArray.clear()
            self.serialClickEventSignal.emit(self.SerialClickEvent.ReceiveClearClickEvent, None)

    def SerialReceiveParamChangedCb(self, value):
        objectName = self.sender().objectName()
        if objectName == self.serialBaudrateComboBox.objectName():
            if value == 0:
                data, ok = QInputDialog.getText(self, self.tr("Baudrate Customize:"), self.tr("Baudrate"), QLineEdit.EchoMode.Normal, "")
                if ok and data != "":
                    self.serialBaudrateComboBox.setItemText(0, data)
                else:
                    self.serialBaudrateComboBox.setCurrentIndex(12)
            else:
                self.serialBaudrateComboBox.setItemText(0, "custom")

            self.config.configHandle.setValue("baudrateIndex", value)
        elif objectName == self.serialReceiveHexCheckBox.objectName():
            text = self.serialReceivePlainTextEdit.toPlainText()
            if value:
                text = text.encode('gbk')
                text = ' '.join([f"{byte:02x}" for byte in text])
            else:
                bytes_object = bytes.fromhex("".join(text.split()))
                text = bytes_object.decode('gbk')
            
            self.serialReceivePlainTextEdit.setPlainText(text)
            self.serialReceivePlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
            self.config.configHandle.setValue("receiveHexEn", value)
        elif objectName == self.serialStopBitComboBox.objectName():
            self.config.configHandle.setValue("stopBitIndex", value)
        elif objectName == self.serialDataBitcomboBox.objectName():
            self.config.configHandle.setValue("dataBitIndex", value)
        elif objectName == self.serialChecksumBitComboBox.objectName():
            self.config.configHandle.setValue("checkSumIndex", value)
        elif objectName == self.serialReceiveTimestampCheckBox.objectName():
            self.config.configHandle.setValue("timestampEn", value)
        
        if self.serialHandle.serial is not None:
            self.SerialOnOffSwitch(False)
            self.SerialOnOffSwitch(True)

    def SerialSendEventCb(self):
        objectName = self.sender().objectName()
        if objectName == self.serialSendPushButton.objectName(): # send data btn
            sendData = self.serialSendPlainTextEdit.toPlainText()
            if not sendData:
                return
            if self.serialSendHexCheckBox.isChecked():
                hex_string = sendData.replace(' ', '')
                if len(hex_string) % 2 != 0:
                    padded_parts = [part.zfill(2) for part in hex_string[-1]]
                    data = bytes.fromhex(hex_string[:-1] +"".join(padded_parts))
                else:
                    data = bytes.fromhex(hex_string)
            else:
                data = sendData.encode('gbk')
            if self.serialHandle.serial is not None:
                self.SerialSendDataPort(data)
        elif objectName == self.serialSendClearPushButton.objectName(): # send clean
            self.sendByteCount = 0
            self.serialSendPlainTextEdit.clear()
            self.serialClickEventSignal.emit(self.SerialClickEvent.SendClearClickEvent, None)
        elif objectName == self.serialSendRepeatCheckBox.objectName():
            if self.serialSendRepeatCheckBox.isChecked():
                self.serialSendRepeatDurationLineEdit.setEnabled(False)
                self.SerialSendRepeatTimer.start(int(self.serialSendRepeatDurationLineEdit.text()))
            else:
                self.serialSendRepeatDurationLineEdit.setEnabled(True)
                self.SerialSendRepeatTimer.stop()
        elif objectName == self.serialFileSelectPushButton.objectName():
            file = QFileDialog.getOpenFileName(self, "Please select the send file", "", "files(*)")
            if file[0]:
                self.serialFileSendLineEdit.setText(file[0])
        elif objectName == self.serialFileSendPushButton.objectName():
            path = self.serialFileSendLineEdit.text()
            if path:
                try:
                    with open(path, "rb") as file:
                        data = file.read()
                        self.SerialSendDataPort(data)
                except IOError:
                    print(f"Can't open this file: {file_name}")
        elif objectName == self.serialFilePathSaveSelectPushButton.objectName():
            file = QFileDialog.getSaveFileName(self, "Please select the save file", "", "files(*)")
            if file[0]:
                self.serialFilePathSaveLineEdit.setText(file[0])
        elif objectName == self.serialFileSavePushButton.objectName():
            path = self.serialFilePathSaveLineEdit.text()
            if path:
                self.saveFileFlag = not self.saveFileFlag
                button_text = self.tr("Stop") if self.saveFileFlag else self.tr("Start")
                self.serialFileSavePushButton.setText(button_text)
                if self.saveFileFlag:
                    self.saveFile = open(path, 'a')
                else:
                    self.saveFile.close()

    def SerialSendParamChangedCb(self, value):
        objectName = self.sender().objectName()
        if objectName == self.serialSendRepeatDurationLineEdit.objectName():
            if value == '0' or value == "":
                value = 1000
                self.serialSendRepeatDurationLineEdit.setText("1000")
                self.warningMsgBox.setText("range:(1-100000)")
                self.warningMsgBox.exec()
            self.config.configHandle.setValue("sendRepeatentDuration", value)
        elif objectName == self.serialSendLineFeedComboBox.objectName():
            self.config.configHandle.setValue("sendLineFeedIndex", value)
        elif objectName == self.serialSoftFlowControlCheckBox.objectName():
            if value != 0:
                self.serialHardFlowControlGroupBox.setEnabled(False)
            else:
                self.serialHardFlowControlGroupBox.setEnabled(True)
            self.config.configHandle.setValue("xonxoff", value)
        elif objectName == self.serialHardFlowControlDSRDTRCheckBox.objectName():
            if value != 0 or self.serialHardFlowControlRTSCTSCheckBox.isChecked():
                self.serialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.serialSoftFlowControlGroupBox.setEnabled(True)
            self.config.configHandle.setValue("dsrdtr", value)
        elif objectName == self.serialHardFlowControlRTSCTSCheckBox.objectName():
            if value != 0 or self.serialHardFlowControlDSRDTRCheckBox.isChecked():
                self.serialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.serialSoftFlowControlGroupBox.setEnabled(True)
            self.config.configHandle.setValue("rtscts", value)
        elif self.serialSendHexCheckBox.objectName():
            self.config.configHandle.setValue("sendHexEn", value)
            text = self.serialSendPlainTextEdit.toPlainText()
            if not text:
                return
            
            if value:
                hex_list = [f"{byte:02x}" for byte in text.encode('gbk')]
                convertText = str(hex_list)
            else:
                byte_array = bytearray.fromhex(text)
                convertText = byte_array.decode('gbk')
            
            self.serialSendPlainTextEdit.setPlainText(convertText)
            self.serialSendPlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)

    def SerialSendTextChangeCb(self, position, charsRemoved, charsAdded):
        if not self.serialSendHexCheckBox.isChecked():
            return
        
        if charsAdded > 0:
            beforeText = self.serialSendPlainTextEdit.toPlainText()[:position]
            text = self.serialSendPlainTextEdit.toPlainText()[position:position+charsAdded]
            afterText = self.serialSendPlainTextEdit.toPlainText()[position+charsAdded:]
            
            newText = ""
            for letter in text:
                if self.hex_pattern.match(letter):
                    newText += letter

            newText = beforeText+newText+afterText

            cursor = self.serialSendPlainTextEdit.textCursor()

            old_position = cursor.position()
            self.serialSendPlainTextEdit.document().blockSignals(True)
            self.serialSendPlainTextEdit.setPlainText(newText)
            self.serialSendPlainTextEdit.document().blockSignals(False)

            cursor.setPosition(old_position)
            self.serialSendPlainTextEdit.setTextCursor(cursor)



    def UiInit(self):
        # receive ui init
        self.serialBaudrateComboBox.setCurrentIndex(int(self.configParam["baudrateIndex"]))
        self.serialStopBitComboBox.setCurrentIndex(int(self.configParam["stopBitIndex"]))
        self.serialDataBitcomboBox.setCurrentIndex(int(self.configParam["dataBitIndex"]))
        self.serialChecksumBitComboBox.setCurrentIndex(int(self.configParam["checkSumIndex"]))
        self.serialReceiveHexCheckBox.setChecked(int(self.configParam["receiveHexEn"]))
        self.serialReceiveTimestampCheckBox.setChecked(int(self.configParam["timestampEn"]))

        # send ui init
        self.warningMsgBox = QMessageBox()
        self.warningMsgBox.setIcon(QMessageBox.Icon.Warning)
        self.warningMsgBox.setWindowTitle("Warning")
        self.warningMsgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.serialSendRepeatDurationLineEdit.setValidator(QIntValidator(0, 100000))

        self.serialSendHexCheckBox.setChecked(int(self.configParam["sendHexEn"]))
        self.serialSendRepeatDurationLineEdit.setText(self.configParam["sendRepeatentDuration"])
        self.serialSendLineFeedComboBox.setCurrentIndex(int(self.configParam["sendLineFeedIndex"]))
        self.serialSoftFlowControlCheckBox.setChecked(int(self.configParam["xonxoff"]))
        self.serialHardFlowControlDSRDTRCheckBox.setChecked(int(self.configParam["dsrdtr"]))
        self.serialHardFlowControlRTSCTSCheckBox.setChecked(int(self.configParam["rtscts"]))

        if self.serialSoftFlowControlCheckBox.isChecked():
            self.serialHardFlowControlGroupBox.setEnabled(False)
        if self.serialHardFlowControlDSRDTRCheckBox.isChecked() or self.serialHardFlowControlRTSCTSCheckBox.isChecked():
            self.serialSoftFlowControlGroupBox.setEnabled(False)