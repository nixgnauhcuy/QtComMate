from enum import Enum
from ui.Ui_setting import Ui_settingForm
from PyQt6.QtWidgets import QFrame, QFontDialog
from PyQt6.QtCore import pyqtSignal

from config import ConfigManager

class SettingForm(QFrame, Ui_settingForm):

    class SerialSettingEvent(Enum):
        SettingLanguageChangeEvent = 0
        SettingThemeChangeEvent = 1
        SettingFontChangeEvent = 2
        SettingEncodingChangeEvent = 3

    serialSettingEventSignal = pyqtSignal(SerialSettingEvent, object)

    def __init__(self, parent=None):
        super(SettingForm, self).__init__(parent)
        self.setupUi(self)

        self.config = ConfigManager()
        self.configParam = self.config.Load()

        self.UiInit()

        self.LanguageComboBox.currentIndexChanged.connect(self.SettingLanguageChangeCb)
        self.ThemeComboBox.currentIndexChanged.connect(self.SettingThemeChangeCb)
        self.EncodingComboBox.currentIndexChanged.connect(self.SettingEncodingChangeCb)
        self.FontPushButton.clicked.connect(self.SettingFontChangeCb)


    def UiInit(self):
        language_dict = {
            "en_US": 0,
            "zh_CN": 1,
            "zh_TW": 2
        }
        theme_dict = {
            "light": 0,
            "dark": 1,
        }
        encodings_dict = {
            "UTF-8": 0,
            "UTF-32": 1,
            "GBK": 2,
            "GB2312": 3,
            "ISO-8859-1": 4,
            "BIG5": 5,
        }
        language = language_dict.get(self.configParam["language"], None)
        self.LanguageComboBox.setCurrentIndex(language)
        theme = theme_dict.get(self.configParam["theme"], None)
        self.ThemeComboBox.setCurrentIndex(theme)
        encoding = encodings_dict.get(self.configParam["encoding"], None)
        self.EncodingComboBox.setCurrentIndex(encoding)
        self.FontPushButton.setText(self.configParam["font"].split(",")[0])

    def SettingLanguageChangeCb(self, value) -> None:
        languages = [
            "en_US",
            "zh_CN",
            "zh_TW"
        ]
        self.config.configHandle.setValue("language", languages[value])
        self.serialSettingEventSignal.emit(self.SerialSettingEvent.SettingLanguageChangeEvent, languages[value])


    def SettingThemeChangeCb(self, value) -> None:
        theme = 'light' if value == 0 else 'dark'
        self.config.configHandle.setValue("theme", theme)
        self.serialSettingEventSignal.emit(self.SerialSettingEvent.SettingThemeChangeEvent, theme)

    def SettingEncodingChangeCb(self, value) -> None:
        encodings = [
            "UTF-8",
            "UTF-32",
            "GBK",
            "GB2312",
            "ISO-8859-1",
            "BIG5"
        ]
        self.config.configHandle.setValue("encoding", encodings[value])
        self.serialSettingEventSignal.emit(self.SerialSettingEvent.SettingEncodingChangeEvent, encodings[value])

    def SettingFontChangeCb(self) -> None:
        font,ok = QFontDialog.getFont()
        if ok:
            self.config.configHandle.setValue("font", font.toString())
            self.FontPushButton.setText(font.toString().split(",")[0])
            self.serialSettingEventSignal.emit(self.SerialSettingEvent.SettingFontChangeEvent, font)