from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTranslator, QFile, QIODeviceBase, QTextStream


def read_resource_text(resource_path: str) -> str:
    qfile = QFile(resource_path)
    if not qfile.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text):
        return ""
    try:
        return QTextStream(qfile).readAll()
    finally:
        qfile.close()


def apply_theme(app: QApplication, theme_name: str) -> None:
    qss = read_resource_text(f":sty/sty/{theme_name}.qss")
    if qss:
        app.setStyleSheet(qss)


def apply_font(app: QApplication, font: QFont) -> None:
    app.setFont(font)


def apply_font_from_config(app: QApplication, font_string: str) -> None:
    font = QFont()
    font.fromString(font_string)
    apply_font(app, font)


def apply_language(translator: QTranslator, language: str) -> bool:
    return translator.load(f":translations/translations/{language}.qm")


def install_language(app: QApplication, translator: QTranslator, language: str) -> bool:
    if apply_language(translator, language):
        app.installTranslator(translator)
        return True
    return False
