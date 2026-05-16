import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

logger = logging.getLogger(__name__)


class ConfigManager(object):
    USER_CONFIG_INI = 'user.ini'
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
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
        self._initialized = True

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
