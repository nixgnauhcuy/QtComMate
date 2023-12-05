import sys
import resources.resources_rc
import config

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QTranslator, QFile, QIODeviceBase, QTextStream

from ui.Ui_main import Ui_mainWindow
from settingForm import SettingForm
from serialForm import SerialForm

class MainForm(QMainWindow, Ui_mainWindow):
    def closeEvent(self, event):
        self.serialForm.closeEvent(event)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.appInstance = QApplication.instance()
        self.translator = QTranslator()
        self.config = config.ConfigManager()
        self.configParam = self.config.Load()

        self.settingForm = SettingForm()

        self.serialForm = SerialForm()
        self.mainLayout.addWidget(self.serialForm)

        self.serialForm.serialClickEventSignal.connect(self.mainSerialClickEventCb)
        self.mainStatusBar.serialStatusBarClickEventSignal.connect(self.mainSerialStatusBarClickEventCb)
        self.settingForm.serialSettingEventSignal.connect(self.mainSettingEventCb)


    def mainSerialClickEventCb(self, type, value):
        if type == self.serialForm.SerialClickEvent.ConnectClickEvent:
            image_path = ":img/img/connect.png" if value else ":img/img/unconnect.png"
            self.mainStatusBar.connStatusLabel.setPixmap(QPixmap(image_path))
        elif type == self.serialForm.SerialClickEvent.ReceiveClearClickEvent:
            self.mainStatusBar.receiveByteCountLabel.setText("R:0")
        elif type == self.serialForm.SerialClickEvent.ReceiveDataClickEvent:
            self.mainStatusBar.receiveByteCountLabel.setText(f"R:{value}")
        elif type == self.serialForm.SerialClickEvent.SendClearClickEvent:
            self.mainStatusBar.sendByteCountLabel.setText("S:0")
        elif type == self.serialForm.SerialClickEvent.SendDataClickEvent:
            self.mainStatusBar.sendByteCountLabel.setText(f"S:{value}")

    def mainSerialStatusBarClickEventCb(self, type, value) -> None:
        if type == self.mainStatusBar.SerialStatusBarClickEvent.SettingClickEvent:
            self.settingForm.show()

    def mainSettingEventCb(self, type, value) -> None:
        if type == self.settingForm.SerialSettingEvent.SettingLanguageChangeEvent:
            self.translator.load(":translations/translations/"+ value + ".qm")
            self.appInstance.installTranslator(self.translator)
            self.settingForm.retranslateUi(self)
            self.serialForm.retranslateUi(self)
            self.retranslateUi(self)
        elif type == self.settingForm.SerialSettingEvent.SettingThemeChangeEvent:
            qss_file = QFile(":sty/sty/" + value + ".qss") 
            if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
                stream = QTextStream(qss_file) 
                self.appInstance.setStyleSheet(stream.readAll()) 
        elif type == self.settingForm.SerialSettingEvent.SettingFontChangeEvent:
            self.appInstance.setFont(value)
            qss_file = QFile(":sty/sty/" + self.config.configHandle.value("theme") + ".qss")
            if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
                stream = QTextStream(qss_file) 
                self.appInstance.setStyleSheet(stream.readAll()) 

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize or load configuration
    _config = config.ConfigManager()
    _config.Init()

    # load theme settings
    qss_file = QFile(":sty/sty/" + _config.configParam["theme"] + ".qss") 
    if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
        stream = QTextStream(qss_file) 
        app.setStyleSheet(stream.readAll())

    # load language settings
    _trans = QTranslator()
    _trans.load(":translations/translations/" + _config.configParam["language"] +".qm")

    # load font settings
    font = QFont()
    font.fromString(_config.configParam["font"])

    app.installTranslator(_trans)
    app.setFont(font)

    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
