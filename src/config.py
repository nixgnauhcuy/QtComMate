import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

USER_CONFIG_INI = 'user.ini'

configini = QSettings(USER_CONFIG_INI, QSettings.Format.IniFormat)

config_param = {
    "language": 'English',
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


def configLoad():
    for key in configini.allKeys():
        config_param[key] = configini.value(key)


def configCreate():
    for key, value in config_param.items():
        configini.setValue(key, value)

    config_param["font"] = QApplication.instance().font().toString()
    configini.setValue("font", QApplication.instance().font().toString())
    configini.sync()

def init():
    if os.path.exists(f'{USER_CONFIG_INI}'):
        configLoad()
    else:
        configCreate()
