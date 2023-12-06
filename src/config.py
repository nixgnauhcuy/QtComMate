import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
class ConfigManager(object):
    USER_CONFIG_INI = 'user.ini'

    def __init__(self) -> None:
        self.configHandle = QSettings(self.USER_CONFIG_INI, QSettings.Format.IniFormat)
        self.configParam = {
                "language": 'en_US',
                "encoding": 'GB2312',
                "baudrateIndex": '12',
                "stopBitIndex": '0',
                "dataBitIndex": '3',
                "checkSumIndex": '0',
                "receiveHexEn": '0',
                "timestampEn": '0',
                "sendHexEn": '0',
                "sendRepeatentDuration": '1000',
                "sendLineFeedIndex": '0',
                "xonxoff": '0',
                "rtscts": '0',
                "dsrdtr": '0',

                "font": '',
                "theme": 'light'
        }

    def Init(self) -> None:
        if os.path.exists(f'{self.USER_CONFIG_INI}'):
            self.Load()
        else:
            self.Create()

    def Load(self) -> dict:
        for key in self.configHandle.allKeys():
            self.configParam[key] = self.configHandle.value(key)
        return self.configParam
    
    def Create(self) -> None:
        for key, value in self.configParam.items():
            self.configHandle.setValue(key, value)

        self.configParam['font'] = QApplication.instance().font().toString()
        self.configHandle.setValue("font", QApplication.instance().font().toString())
        self.configHandle.sync()