import sys
import resources_rc
import config

from PyQt6.QtWidgets import QApplication, QMainWindow, QFontDialog
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QTranslator, QFile, QIODeviceBase, QTextStream

from ui.Ui_main import Ui_mainWindow
from about import AboutForm
from serialForm import SerialForm

class MainForm(QMainWindow, Ui_mainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.appInstance = QApplication.instance()
        self.translator = QTranslator()
        self.config = config.ConfigManager()
        self.configParam = self.config.Load()

        self.aboutForm = AboutForm()

        self.serialForm = SerialForm()
        self.mainLayout.addWidget(self.serialForm)

        self.mainUiInit()

        self.serialForm.serialClickEventSignal.connect(self.mainSerialClickEventCb)

        # Menu Settings - Language
        self.enLanguageAction.triggered.connect(self.mainLanguageChangeCb)
        self.cnLanguageAction.triggered.connect(self.mainLanguageChangeCb)
        self.tcLanguageAction.triggered.connect(self.mainLanguageChangeCb)
        # Menu Settings - Font
        self.fontSettingsAction.triggered.connect(self.mainFontChangeCb)
        # Menu Settings - Theme
        self.lightThemeAction.triggered.connect(self.mainThemeChangeCb)
        self.darkThemeAction.triggered.connect(self.mainThemeChangeCb)
        # Menu Help - About
        self.aboutAction.triggered.connect(self.mainHelpAboutCb)

    def mainUiInit(self) -> None:
        languageMap = {
            "enLanguageAction": "en_US",
            "cnLanguageAction": "zh_CN",
            "tcLanguageAction": "zh_TW"
        }

        themeMap = {
            "lightThemeAction": "light",
            "darkThemeAction": "dark"
        }

        for action in self.languageMenu.actions():
            actionLanguage = languageMap.get(action.objectName(), None)
            if actionLanguage is None:
                continue
            is_selected = actionLanguage == self.configParam["language"]
            action.setChecked(is_selected)
            action.setEnabled(not is_selected)

        for action in self.themeMenu.actions():
            actionTheme = themeMap.get(action.objectName(), None)
            if actionTheme is None:
                continue
            is_selected = actionTheme == self.configParam["theme"]
            action.setChecked(is_selected)
            action.setEnabled(not is_selected)

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


    def mainLanguageChangeCb(self) -> None:
        curObjectName = self.sender().objectName()
        if curObjectName == self.cnLanguageAction.objectName():
            self.config.configHandle.setValue("language", "zh_CN")
            self.translator.load(":translations/translations/zh_CN.qm")
        elif curObjectName == self.tcLanguageAction.objectName():
            self.config.configHandle.setValue("language", "zh_TW")
            self.translator.load(":translations/translations/zh_TW.qm")
        elif curObjectName == self.enLanguageAction.objectName():
            self.config.configHandle.setValue("language", "en_US")
            self.translator.load(":translations/translations/en_US.qm")

        for action in self.languageMenu.actions():
            is_selected = action.objectName() == curObjectName
            action.setChecked(is_selected)
            action.setEnabled(not is_selected)

        self.appInstance.installTranslator(self.translator)
        self.aboutForm.retranslateUi(self)
        self.serialForm.retranslateUi(self)
        self.retranslateUi(self)
        

    def mainFontChangeCb(self) -> None:
        font,ok = QFontDialog.getFont()
        if ok:
            self.appInstance.setFont(font)
            self.config.configHandle.setValue("font", font.toString())
            qss_file = QFile(":sty/sty/" + self.config.configHandle.value("theme") + ".qss")
            if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
                stream = QTextStream(qss_file) 
                self.appInstance.setStyleSheet(stream.readAll()) 


    def mainThemeChangeCb(self) -> None:
        curObjectName = self.sender().objectName()
        theme = 'light' if curObjectName == self.lightThemeAction.objectName() else 'dark'

        self.config.configHandle.setValue("theme", theme)

        for action in self.themeMenu.actions():
            is_selected = action.objectName() == curObjectName
            action.setChecked(is_selected)
            action.setEnabled(not is_selected)

        qss_file = QFile(":sty/sty/" + theme + ".qss") 
        if qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text): 
            stream = QTextStream(qss_file) 
            self.appInstance.setStyleSheet(stream.readAll()) 

    def mainHelpAboutCb(self) -> None:
        self.aboutForm.show()


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
