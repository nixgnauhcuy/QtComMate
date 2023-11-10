from ui.Ui_about import Ui_aboutForm
from PyQt6.QtWidgets import QApplication, QFrame

class AboutForm(QFrame):
    def __init__(self, parent=None):
        super(AboutForm, self).__init__(parent)
        self.ui = Ui_aboutForm()
        self.ui.setupUi(self)