import sys
import threading
import re
import resources_rc
import config
import serialport
import binascii
import datetime
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFontDialog, QInputDialog, QLineEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QFont, QTextCursor, QIntValidator
from PyQt6.QtCore import pyqtSignal, QThread, QTranslator, QTimer, QFile, QIODeviceBase, QTextStream, QByteArray

from ui.Ui_main import Ui_MainWindow
from about import AboutForm

class SerialPortReceiveDataThread(QThread):
    dataReceivedSignal = pyqtSignal(str, int)

    def __init__(self, parent):
        super(SerialPortReceiveDataThread, self).__init__()
        self.parent = parent
        self.thread = threading.Event()

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while not self.stopped():
            try:
                data = self.parent.port.read()
                if data:
                    self.parent.receiveArray.append(data)
                    dataLen = len(data)
                    if self.parent.SerialReceiveHexCheckBox.isChecked():
                        data_hex_spaced = " " + " ".join([f"{b:02x}" for b in data])
                        self.dataReceivedSignal.emit(data_hex_spaced, dataLen)
                    else:
                        self.dataReceivedSignal.emit(data.decode('iso-8859-1'), dataLen)
                else:
                    time.sleep(0.01)
            except Exception as e:
                print(e)
                continue


class MyPyQT_Form(QMainWindow, Ui_MainWindow):

    def closeEvent(self, event):
        if self.port.isOpen():
            self.receiveSerialPortThread.stop()
            self.SerialSendRepeatCheckBox.setChecked(False)
            self.port.close()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.aboutForm = AboutForm()

        self.app = QApplication.instance()
        self.trans = QTranslator()

        self.serialUiInit()
        
        self.hex_pattern = re.compile(r'^[0-9a-fA-F]+$')

        self.sendCountSum = 0
        self.receiveCountSum = 0
        self.receiveArray = QByteArray()
        self.saveFileFlag = False
        self.saveFile = ""

        self.port = serialport.SerialPort()
        self.warningMsgBox = QMessageBox()
        self.warningMsgBox.setIcon(QMessageBox.Icon.Warning)
        self.warningMsgBox.setWindowTitle("Warning")
        self.warningMsgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.SerialSendRepeatTimer = QTimer()
        self.SerialSendRepeatTimer.timeout.connect(self.serialSendRepeatTimerCb)

        # Menu Settings
        # Language
        self.EnglishLanguageAction.triggered.connect(self.serialLanguageSwitchCb)
        self.SimplifiedChineseLanguageAction.triggered.connect(self.serialLanguageSwitchCb)
        self.TraditionalChineseLanguageAction.triggered.connect(self.serialLanguageSwitchCb)
        # Font
        self.FontSetAction.triggered.connect(self.serialFontSetCb)
        # Theme
        self.LightThemeAction.triggered.connect(self.serialThemeSwitchCb)
        self.DarkThemeAction.triggered.connect(self.serialThemeSwitchCb)

        # Menu Help
        # About
        self.AboutAction.triggered.connect(self.serialHelpAboutCb)
        
        # Receive Area
        self.SerialConnectComPushButton.clicked.connect(self.serialConnectComPushButtonCb)
        self.SerialReceiveClearPushButton.clicked.connect(self.serialReceiveClearPushButtonCb)
        self.SerialReceiveHexCheckBox.stateChanged.connect(self.serialReceiveHexCheckBoxCb)
        self.SerialBaudrateComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialStopBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialDataBitcomboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialChecksumBitComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialReceiveTimestampCheckBox.stateChanged.connect(self.serialComConfigCb)

        # Send Area
        self.SerialSendPushButton.clicked.connect(self.serialSendComPushButtonCb)
        self.SerialSendPlainTextEdit.document().contentsChange.connect(self.serialSendTextChangeCb)
        self.SerialSendClearPushButton.clicked.connect(self.serialSendClearPushButtonCb)
        self.SerialSendRepeatCheckBox.stateChanged.connect(self.serialSendRepeatCheckCb)
        self.SerialSendRepeatDurationLineEdit.textChanged.connect(self.serialSendRepeatDurationLineEditCb)
        self.SerialSendHexCheckBox.stateChanged.connect(self.serialSendHexCheckBoxCb)
        self.SerialSendLineFeedComboBox.currentIndexChanged.connect(self.serialComConfigCb)
        self.SerialSoftFlowControlCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlDSRDTRCheckBox.stateChanged.connect(self.serialComConfigCb)
        self.SerialHardFlowControlRTSCTSCheckBox.stateChanged.connect(self.serialComConfigCb)

        # File
        self.SerialFileSelectPushButton.clicked.connect(self.SerialFileSelectPushButtonCb)
        self.SerialFileSendPushButton.clicked.connect(self.SerialFileSendPushButtonCb)
        self.SerialFilePathSaveSelectPushButton.clicked.connect(self.SerialFilePathSaveSelectPushButtonCb)
        self.SerialFileSavePushButton.clicked.connect(self.SerialFileSavedPushButtonCb)

        

    def serialUiInit(self):
        
        self.connStatusLabel = QLabel()
        self.sendByteCountLabel = QLabel("S:0")
        self.receiveByteCountLabel = QLabel("R:0")
        self.tmpLabel = QLabel() # tmp 
        self.connStatusLabel.setPixmap(QPixmap(":img/img/unconnect.png"))
        self.SerialStatusBar.addPermanentWidget(self.connStatusLabel, stretch=0)
        self.SerialStatusBar.addPermanentWidget(self.tmpLabel, stretch=4) # tmp
        self.SerialStatusBar.addPermanentWidget(self.sendByteCountLabel, stretch=1)
        self.SerialStatusBar.addPermanentWidget(self.receiveByteCountLabel, stretch=1)


        self.SerialSendRepeatDurationLineEdit.setValidator(QIntValidator(0, 100000))
        
        for action in self.MenuLanguage.actions():
            if action.text() == config.config_param["language"]:
                action.setChecked(True)
                action.setEnabled(False)
            else:
                action.setChecked(False)
                action.setEnabled(True)

        for action in self.MenuTheme.actions():
            if action.text() == config.config_param["theme"]:
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

        if self.SerialSoftFlowControlCheckBox.isChecked():
            self.SerialHardFlowControlGroupBox.setEnabled(False)
        if self.SerialHardFlowControlDSRDTRCheckBox.isChecked() or self.SerialHardFlowControlRTSCTSCheckBox.isChecked():
            self.SerialSoftFlowControlGroupBox.setEnabled(False)

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

    # File
    # File Select File
    def SerialFileSelectPushButtonCb(self):
        file = QFileDialog.getOpenFileName(self, "Please select the send file", "", "files(*)")
        if file[0] != "":
            self.SerialFileSendLineEdit.setText(file[0])

    # File Send Select File
    def SerialFileSendPushButtonCb(self):
        if self.SerialFileSendLineEdit.text() != "":
            try:
                with open(self.SerialFileSendLineEdit.text(), "rb") as file:
                    data = file.read()
                    self.serialSendPortWirte(data)
            except IOError:
                print(f"Can't open this file: {file_name}")

    # Select File Save Path
    def SerialFilePathSaveSelectPushButtonCb(self):
        file = QFileDialog.getSaveFileName(self, "Please select the save file", "", "files(*)")
        if file[0] != "":
            self.SerialFilePathSaveLineEdit.setText(file[0])

    # File Save Select Path
    def SerialFileSavedPushButtonCb(self):
        if self.SerialFilePathSaveLineEdit.text() != "":
            if not self.saveFileFlag:
                self.saveFileFlag = True
                self.SerialFileSavePushButton.setText(self.tr("Stop"))
                self.saveFile = open(self.SerialFilePathSaveLineEdit.text(), 'a')
            else:
                self.saveFileFlag = False
                self.SerialFileSavePushButton.setText(self.tr("Start"))
                self.saveFile.close()


    def serialConnectComPushButtonCb(self):
        if self.port.serial is None and self.SerialComboBox.currentText() != "":
            self.connStatusLabel.setPixmap(QPixmap(":img/img/connect.png"))
            res = self.serialConnectPortSwitch(True)
            if res == True:
                self.SerialConnectComPushButton.setText(self.tr("Disconnect"))

        elif self.port.serial is not None:
            self.connStatusLabel.setPixmap(QPixmap(":img/img/unconnect.png"))
            res = self.serialConnectPortSwitch(False)
            if res == True:
                self.SerialConnectComPushButton.setText(self.tr("Connect"))


    def serialSendPortWirte(self, data):
        newLine = b''
        if self.SerialSendLineFeedComboBox.currentIndex() == 1:
            newLine = b'\r\n'
        elif self.SerialSendLineFeedComboBox.currentIndex() == 2:
            newLine = b'\r'
        elif self.SerialSendLineFeedComboBox.currentIndex() == 3:
            newLine = b'\n'
            
        data += newLine

        self.sendCountSum += len(data)
        self.sendByteCountLabel.setText("S:" + str(self.sendCountSum))
        self.port.write(data)

    def serialSendComPushButtonCb(self):
        if self.port.serial is None or self.SerialSendPlainTextEdit.toPlainText() == "":
            return
        if self.SerialSendHexCheckBox.isChecked() == True:
            hex_string = self.SerialSendPlainTextEdit.toPlainText().replace(' ', '')
            if len(hex_string) % 2 != 0:
                padded_parts = [part.zfill(2) for part in hex_string[-1]]
                data = bytes.fromhex(hex_string[:-1] +"".join(padded_parts))
            else:
                data = bytes.fromhex(hex_string)
    
            self.serialSendPortWirte(data)
        else:
            self.serialSendPortWirte(str.encode(self.SerialSendPlainTextEdit.toPlainText()))

    def serialSendClearPushButtonCb(self):
        self.sendCountSum = 0
        self.sendByteCountLabel.setText("S:0")
        self.SerialSendPlainTextEdit.clear()


    def readSerialPortDataSignalCb(self, data, dataLen):
        self.receiveCountSum += dataLen
        self.receiveByteCountLabel.setText("R:" + str(self.receiveCountSum))
        
        timestamp = ""
        if self.SerialReceiveTimestampCheckBox.isChecked():
            timestamp = '\n' + datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f')[:-3] + ']\n'
        if self.saveFileFlag:
            self.saveFile.write(data)

        self.SerialReceivePlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        self.SerialReceivePlainTextEdit.insertPlainText(timestamp+data)
        self.SerialReceivePlainTextEdit.verticalScrollBar().setValue(self.SerialReceivePlainTextEdit.verticalScrollBar().maximum())

    def serialReceiveClearPushButtonCb(self):
        self.receiveCountSum = 0
        self.receiveByteCountLabel.setText("R:0")
        self.receiveArray.clear()
        if self.SerialReceivePlainTextEdit.toPlainText() != "":
            self.SerialReceivePlainTextEdit.clear()

    def serialSendTextChangeCb(self, position, charsRemoved, charsAdded):
        if not self.SerialSendHexCheckBox.isChecked():
            return
        
        if charsAdded > 0:
            beforeText = self.SerialSendPlainTextEdit.toPlainText()[:position]
            text = self.SerialSendPlainTextEdit.toPlainText()[position:position+charsAdded]
            afterText = self.SerialSendPlainTextEdit.toPlainText()[position+charsAdded:]
            
            newText = ""
            
            for letter in text:
                if self.hex_pattern.match(letter):
                    newText += letter

            newText = beforeText+newText+afterText

            cursor = self.SerialSendPlainTextEdit.textCursor()

            old_position = cursor.position()
            self.SerialSendPlainTextEdit.document().blockSignals(True)
            self.SerialSendPlainTextEdit.setPlainText(newText)
            self.SerialSendPlainTextEdit.document().blockSignals(False)

            cursor.setPosition(old_position)
            self.SerialSendPlainTextEdit.setTextCursor(cursor)


    def serialSendRepeatCheckCb(self, value):
        if value != 0:
            self.SerialSendRepeatDurationLineEdit.setEnabled(False)
            self.SerialSendRepeatTimer.start(int(self.SerialSendRepeatDurationLineEdit.text()))
        else:
            self.SerialSendRepeatDurationLineEdit.setEnabled(True)
            self.SerialSendRepeatTimer.stop()

    def serialSendRepeatTimerCb(self):
        if self.port.serial is None or self.SerialSendPlainTextEdit.toPlainText() == "":
            return
        if self.SerialSendHexCheckBox.isChecked() == True:
            hex_string = self.SerialSendPlainTextEdit.toPlainText().replace(' ', '')
            if len(hex_string) % 2 != 0:
                padded_parts = [part.zfill(2) for part in hex_string[-1]]
                data = bytes.fromhex(hex_string[:-1] +"".join(padded_parts))
            else:
                data = bytes.fromhex(hex_string)
    
            self.serialSendPortWirte(data)
        else:
            self.serialSendPortWirte(str.encode(self.SerialSendPlainTextEdit.toPlainText()))


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
            if value == 0:
                data, ok = QInputDialog.getText(self, "Baudrate Customize:", "Baudrate", QLineEdit.EchoMode.Normal, "")
                if ok and data != "":
                    self.SerialBaudrateComboBox.setItemText(0, data)
                else:
                    self.SerialBaudrateComboBox.setCurrentIndex(12)
            else:
                self.SerialBaudrateComboBox.setItemText(0, "custom")

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
            if value != 0:
                self.SerialHardFlowControlGroupBox.setEnabled(False)
            else:
                self.SerialHardFlowControlGroupBox.setEnabled(True)
            config.configini.setValue("xonxoff", value)
        elif curObjectName == self.SerialHardFlowControlDSRDTRCheckBox.objectName():
            if value != 0 or self.SerialHardFlowControlRTSCTSCheckBox.isChecked():
                self.SerialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.SerialSoftFlowControlGroupBox.setEnabled(True)
            config.configini.setValue("dsrdtr", value)
        elif curObjectName == self.SerialHardFlowControlRTSCTSCheckBox.objectName():
            if value != 0 or self.SerialHardFlowControlDSRDTRCheckBox.isChecked():
                self.SerialSoftFlowControlGroupBox.setEnabled(False)
            else:
                self.SerialSoftFlowControlGroupBox.setEnabled(True)
            config.configini.setValue("rtscts", value)
        
        if self.port.serial is not None:
            self.serialConnectPortSwitch(False)
            self.serialConnectPortSwitch(True)

    def serialReceiveHexCheckBoxCb(self, value):
        config.configini.setValue("receiveHexEn", value)

        if self.receiveArray.isEmpty():
            return
    
        if value:
            hex_string = binascii.hexlify(self.receiveArray.data()).decode('utf-8')
            convertText = ' '.join([hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
        else:
            convertText = self.receiveArray.data().decode('utf-8', errors='replace')
        
        self.SerialReceivePlainTextEdit.setPlainText(convertText)
        self.SerialReceivePlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        


    def serialSendHexCheckBoxCb(self, value):
        config.configini.setValue("sendHexEn", value)

        if self.SerialSendPlainTextEdit.toPlainText() == "":
            return

        if self.SerialSendLineFeedComboBox.currentIndex() == 1:
            newLine = '0d 0a'
        elif self.SerialSendLineFeedComboBox.currentIndex() == 2:
            newLine = '0d'
        elif self.SerialSendLineFeedComboBox.currentIndex() == 3:
            newLine = '0a'
        else:
            newLine = ''
            
        if value:
            text = self.SerialSendPlainTextEdit.toPlainText()
            hex_list = [hex(ord(x))[2:] for x in text]
            convertText = ' '.join(hex_list).replace('a', newLine)
            
        else:
            hexText = self.SerialSendPlainTextEdit.toPlainText().replace(' ', '')
            convertText = ' '.join([chr(int(hexText[i:i+2], 16)) for i in range(0, len(hexText), 2)]).replace(' ', '')
            
        self.SerialSendPlainTextEdit.setPlainText(convertText)
        self.SerialSendPlainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        
    

    def serialLanguageSwitchCb(self, value):
        if value == False:
            return
        curObjectName = self.sender().objectName()
        if curObjectName == self.SimplifiedChineseLanguageAction.objectName():
            config.configini.setValue("language", "简体中文")
            self.trans.load(":translations/translations/简体中文.qm")
        elif curObjectName == self.TraditionalChineseLanguageAction.objectName():
            config.configini.setValue("language", "繁體中文")
            self.trans.load(":translations/translations/繁體中文.qm")
        elif curObjectName == self.EnglishLanguageAction.objectName():
            config.configini.setValue("language", "English")
            self.trans.load(":translations/translations/English.qm")

        for action in self.MenuLanguage.actions():
            if action.objectName() == curObjectName:
                action.setChecked(True)
                action.setEnabled(False)
            else:
                action.setChecked(False)
                action.setEnabled(True)

        self.app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.aboutForm.ui.retranslateUi(self)

    def serialFontSetCb(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.app.setFont(font)
            config.configini.setValue("font", font.toString())
            qss_file = QFile(":sty/sty/" + config.configini.value("theme") + ".qss")
            if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
                stream = QTextStream(qss_file) 
                app.setStyleSheet(stream.readAll()) 


    def serialThemeSwitchCb(self, value):
        if value == False:
            return
        curObjectName = self.sender().objectName()
        if curObjectName == self.LightThemeAction.objectName():
            theme = 'light'
        else:
            theme = 'dark'

        config.configini.setValue("theme", theme)

        for action in self.MenuTheme.actions():
            if action.objectName() == curObjectName:
                action.setChecked(True)
                action.setEnabled(False)
            else:
                action.setChecked(False)
                action.setEnabled(True)

        qss_file = QFile(":sty/sty/" + theme + ".qss") 
        if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
            stream = QTextStream(qss_file) 
            app.setStyleSheet(stream.readAll()) 

    def serialHelpAboutCb(self):
        self.aboutForm.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Initialize or load configuration
    config.init()

    # load theme settings
    qss_file = QFile(":sty/sty/" + config.config_param["theme"] + ".qss") 
    if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
        stream = QTextStream(qss_file) 
        app.setStyleSheet(stream.readAll())
    # load language settings
    _trans = QTranslator()
    _trans.load(":translations/translations/" + config.config_param["language"] +".qm")
    # load font settings
    font = QFont()
    font.fromString(config.config_param["font"])

    app.installTranslator(_trans)
    app.setFont(font)

    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec())
