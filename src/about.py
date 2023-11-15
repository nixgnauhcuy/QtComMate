from ui.Ui_about import Ui_aboutForm
from PyQt6.QtWidgets import QFrame

class AboutForm(QFrame, Ui_aboutForm):
    def __init__(self, parent=None):
        super(AboutForm, self).__init__(parent)
        self.setupUi(self)