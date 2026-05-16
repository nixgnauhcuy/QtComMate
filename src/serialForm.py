import re
import logging
from enum import Enum
from time import time
from datetime import datetime

from ui.Ui_serial import Ui_serialForm
from serialPort import SerialPort
from config import ConfigManager
from serial_utils import (
    parse_send_payload,
    format_bytes_as_hex,
    text_to_hex_display,
    hex_display_to_text,
)

from PyQt6.QtWidgets import QFrame, QInputDialog, QLineEdit, QMessageBox, QFileDialog
from PyQt6.QtGui import QTextCursor, QIntValidator
from PyQt6.QtCore import pyqtSignal, QTimer

logger = logging.getLogger(__name__)

RECEIVE_POLL_INTERVAL_MS = 30
RECEIVE_DISPLAY_MAX_CHARS = 500_000


class SerialForm(QFrame, Ui_serialForm):

    def closeEvent(self, event):
        if self.serialHandle.isOpen():
            self.receivePollTimer.stop()
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
        self.encoding = self.configParam['encoding']

        self.UiInit()

        # receive
        self.last_recv_time = 0
        self.receiveByteCount = 0

        self.receivePollTimer = QTimer(self)
        self.receivePollTimer.timeout.connect(self._poll_serial_receive)

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

    def _current_serial_params(self):
        return (
            int(self.serialBaudrateComboBox.currentText()),
            int(self.serialDataBitcomboBox.currentText()),
            self.serialChecksumBitComboBox.currentText()[0],
            float(self.serialStopBitComboBox.currentText()),
            int(self.serialSoftFlowControlCheckBox.isChecked()),
            int(self.serialHardFlowControlRTSCTSCheckBox.isChecked()),
            int(self.serialHardFlowControlDSRDTRCheckBox.isChecked()),
        )

    def SerialOnOffSwitch(self, en) -> bool:
        self.last_recv_time = 0
        if en:
            port = self.serialComboBox.currentText().split()[0]
            baudrate, dataBit, checkSum, stopBit, xonxoff, rtscts, dsrdtr = self._current_serial_params()
            return self.serialHandle.open(port, baudrate, dataBit, checkSum, stopBit, xonxoff, rtscts, dsrdtr)
        return self.serialHandle.close()

    def _apply_serial_params_if_open(self) -> None:
        if not self.serialHandle.isOpen():
            return
        baudrate, dataBit, checkSum, stopBit, xonxoff, rtscts, dsrdtr = self._current_serial_params()
        if not self.serialHandle.reconfigure(baudrate, dataBit, checkSum, stopBit, xonxoff, rtscts, dsrdtr):
            self.SerialOnOffSwitch(False)
            self.SerialOnOffSwitch(True)

    def SerialSendDataPort(self, data):
        if self.serialHandle.serial is None:
            return
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
        data = parse_send_payload(sendData, self.serialSendHexCheckBox.isChecked(), self.encoding)
        self.SerialSendDataPort(data)

    def _poll_serial_receive(self):
        data = self.serialHandle.read_all_pending()
        if not data:
            return

        self.receiveByteCount += len(data)
        self.serialClickEventSignal.emit(
            self.SerialClickEvent.ReceiveDataClickEvent, self.receiveByteCount
        )
        self._append_receive_display(data)

    def _format_receive_chunk(self, data: bytes) -> str:
        if self.serialReceiveHexCheckBox.isChecked():
            return format_bytes_as_hex(data)
        return data.decode(self.encoding, errors='replace')

    def _append_receive_display(self, data: bytes):
        display_text = self._format_receive_chunk(data)

        timestamp = ""
        if self.serialReceiveTimestampCheckBox.isChecked() and time() - self.last_recv_time > 0.1:
            timestamp = f"\n[{datetime.now():%Y-%m-%d %H:%M:%S.%f}]".rjust(23, ' ')[:-3] + ']\n'
            self.last_recv_time = time()

        if self.saveFileFlag:
            self.saveFile.write(f"{timestamp}{display_text}")

        self.serialReceivePlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        self.serialReceivePlainTextEdit.insertPlainText(f"{timestamp}{display_text}")
        self.serialReceivePlainTextEdit.verticalScrollBar().setValue(
            self.serialReceivePlainTextEdit.verticalScrollBar().maximum()
        )
        self._trim_receive_view()

    def _trim_receive_view(self):
        doc = self.serialReceivePlainTextEdit.document()
        excess = doc.characterCount() - RECEIVE_DISPLAY_MAX_CHARS
        if excess <= 0:
            return
        cursor = QTextCursor(doc)
        cursor.setPosition(0)
        cursor.setPosition(excess, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()

    def SerialReceiveEventCb(self):
        objectName = self.sender().objectName()
        if objectName == self.serialConnectComPushButton.objectName(): # connect btn
            ret = False
            if self.serialHandle.serial is None and self.serialComboBox.currentText():
                res = self.SerialOnOffSwitch(True)
                if res:
                    self.receivePollTimer.start(RECEIVE_POLL_INTERVAL_MS)
                    self.serialConnectComPushButton.setText(self.tr("Disconnect"))
                    ret = True
                else:
                    self.warningMsgBox.setText(
                        self.tr("Could not open port, Please verify if the serial port is correct or if it is being occupied!!!")
                    )
                    self.warningMsgBox.exec()
            elif self.serialHandle.serial is not None:
                self.receivePollTimer.stop()
                self.serialConnectComPushButton.setText(self.tr("Connect"))
                self.SerialOnOffSwitch(False)
            self.serialClickEventSignal.emit(self.SerialClickEvent.ConnectClickEvent, ret)
        elif objectName == self.serialReceiveClearPushButton.objectName():  # clear receive btn
            self.serialReceivePlainTextEdit.clear()
            self.receiveByteCount = 0
            self.serialClickEventSignal.emit(self.SerialClickEvent.ReceiveClearClickEvent, None)

    def SerialReceiveParamChangedCb(self, value):
        objectName = self.sender().objectName()
        if objectName == self.serialBaudrateComboBox.objectName():
            if value == 0:
                data, ok = QInputDialog.getText(
                    self, self.tr("Baudrate Customize:"), self.tr("Baudrate"),
                    QLineEdit.EchoMode.Normal, ""
                )
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
                text = text_to_hex_display(text, self.encoding)
            else:
                text = hex_display_to_text(text, self.encoding)
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

        self._apply_serial_params_if_open()

    def SerialSendEventCb(self):
        objectName = self.sender().objectName()
        if objectName == self.serialSendPushButton.objectName(): # send data btn
            sendData = self.serialSendPlainTextEdit.toPlainText()
            if not sendData:
                return
            data = parse_send_payload(sendData, self.serialSendHexCheckBox.isChecked(), self.encoding)
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
                        self.SerialSendDataPort(file.read())
                except IOError:
                    logger.error("Can't open this file: %s", path)
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
                    self.saveFile = open(path, 'a', encoding='utf-8')
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
            self._apply_serial_params_if_open()
        elif objectName == self.serialHardFlowControlDSRDTRCheckBox.objectName():
            if value != 0 or self.serialHardFlowControlRTSCTSCheckBox.isChecked():
                self.serialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.serialSoftFlowControlGroupBox.setEnabled(True)
            self.config.configHandle.setValue("dsrdtr", value)
            self._apply_serial_params_if_open()
        elif objectName == self.serialHardFlowControlRTSCTSCheckBox.objectName():
            if value != 0 or self.serialHardFlowControlDSRDTRCheckBox.isChecked():
                self.serialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.serialSoftFlowControlGroupBox.setEnabled(True)
            self.config.configHandle.setValue("rtscts", value)
            self._apply_serial_params_if_open()
        elif objectName == self.serialSendHexCheckBox.objectName():
            self.config.configHandle.setValue("sendHexEn", value)
            text = self.serialSendPlainTextEdit.toPlainText()
            if not text:
                return
            if value:
                convertText = text_to_hex_display(text, self.encoding)
            else:
                convertText = hex_display_to_text(text, self.encoding)
            self.serialSendPlainTextEdit.setPlainText(convertText)
            self.serialSendPlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)

    def SerialSendTextChangeCb(self, position, charsRemoved, charsAdded):
        if not self.serialSendHexCheckBox.isChecked() or charsAdded <= 0:
            return

        plain_text = self.serialSendPlainTextEdit.toPlainText()
        before_text = plain_text[:position]
        text = plain_text[position:position + charsAdded]
        after_text = plain_text[position + charsAdded:]

        filtered = "".join(letter for letter in text if self.hex_pattern.match(letter))
        if filtered == text:
            return

        new_text = before_text + filtered + after_text
        cursor = self.serialSendPlainTextEdit.textCursor()
        old_position = cursor.position()

        self.serialSendPlainTextEdit.document().blockSignals(True)
        self.serialSendPlainTextEdit.setPlainText(new_text)
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
