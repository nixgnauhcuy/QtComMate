import sys
import logging
import resources.resources_rc
import config
import app_style

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTranslator

from ui.Ui_main import Ui_mainWindow
from settingForm import SettingForm
from serialForm import SerialForm

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")


class MainForm(QMainWindow, Ui_mainWindow):
    def closeEvent(self, event):
        self.serialForm.closeEvent(event)

    def __init__(self, translator=None) -> None:
        super().__init__()
        self.setupUi(self)

        self.appInstance = QApplication.instance()
        self.translator = translator or QTranslator()
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
            app_style.install_language(self.appInstance, self.translator, value)
            self.settingForm.retranslateUi(self.settingForm)
            self.serialForm.retranslateUi(self.serialForm)
            self.retranslateUi(self)
        elif type == self.settingForm.SerialSettingEvent.SettingThemeChangeEvent:
            app_style.apply_theme(self.appInstance, value)
        elif type == self.settingForm.SerialSettingEvent.SettingFontChangeEvent:
            app_style.apply_font(self.appInstance, value)
            app_style.apply_theme(self.appInstance, self.config.configHandle.value("theme"))
        elif type == self.settingForm.SerialSettingEvent.SettingEncodingChangeEvent:
            self.serialForm.encoding = value


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize or load configuration
    _config = config.ConfigManager()
    _config.Init()

    # load theme settings
    app_style.apply_theme(app, _config.configParam["theme"])

    # load language settings
    _trans = QTranslator()
    app_style.install_language(app, _trans, _config.configParam["language"])
    # load font settings
    app_style.apply_font_from_config(app, _config.configParam["font"])

    mainForm = MainForm(_trans)
    mainForm.show()
    sys.exit(app.exec())
