from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_settingForm(object):
    def setupUi(self, settingForm):
        settingForm.setObjectName("settingForm")
        settingForm.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        settingForm.resize(640, 220)
        settingForm.setMinimumSize(QtCore.QSize(640, 220))
        settingForm.setMaximumSize(QtCore.QSize(640, 220))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/setting.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        settingForm.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(settingForm)
        self.gridLayout.setObjectName("gridLayout")
        self.TabWidget = QtWidgets.QTabWidget(settingForm)
        self.TabWidget.setObjectName("TabWidget")
        self.GeneralTab = QtWidgets.QWidget()
        self.GeneralTab.setObjectName("GeneralTab")
        self.LanguageLabel = QtWidgets.QLabel(self.GeneralTab)
        self.LanguageLabel.setGeometry(QtCore.QRect(10, 10, 60, 20))
        self.LanguageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.LanguageLabel.setObjectName("LanguageLabel")
        self.LanguageComboBox = QtWidgets.QComboBox(self.GeneralTab)
        self.LanguageComboBox.setGeometry(QtCore.QRect(80, 10, 101, 25))
        self.LanguageComboBox.setObjectName("LanguageComboBox")
        self.LanguageComboBox.addItem("")
        self.LanguageComboBox.addItem("")
        self.LanguageComboBox.addItem("")
        self.ThemeLabel = QtWidgets.QLabel(self.GeneralTab)
        self.ThemeLabel.setGeometry(QtCore.QRect(10, 40, 60, 20))
        self.ThemeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ThemeLabel.setObjectName("ThemeLabel")
        self.ThemeComboBox = QtWidgets.QComboBox(self.GeneralTab)
        self.ThemeComboBox.setGeometry(QtCore.QRect(80, 40, 101, 25))
        self.ThemeComboBox.setObjectName("ThemeComboBox")
        self.ThemeComboBox.addItem("")
        self.ThemeComboBox.addItem("")
        self.FontLabel = QtWidgets.QLabel(self.GeneralTab)
        self.FontLabel.setGeometry(QtCore.QRect(10, 70, 60, 20))
        self.FontLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.FontLabel.setObjectName("FontLabel")
        self.FontPushButton = QtWidgets.QPushButton(self.GeneralTab)
        self.FontPushButton.setGeometry(QtCore.QRect(80, 70, 161, 25))
        self.FontPushButton.setObjectName("FontPushButton")
        self.EncodingLabel = QtWidgets.QLabel(self.GeneralTab)
        self.EncodingLabel.setGeometry(QtCore.QRect(10, 100, 60, 20))
        self.EncodingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.EncodingLabel.setObjectName("EncodingLabel")
        self.EncodingComboBox = QtWidgets.QComboBox(self.GeneralTab)
        self.EncodingComboBox.setGeometry(QtCore.QRect(80, 100, 101, 25))
        self.EncodingComboBox.setObjectName("EncodingComboBox")
        self.EncodingComboBox.addItem("")
        self.EncodingComboBox.addItem("")
        self.EncodingComboBox.addItem("")
        self.EncodingComboBox.addItem("")
        self.EncodingComboBox.addItem("")
        self.EncodingComboBox.addItem("")
        self.TabWidget.addTab(self.GeneralTab, "")
        self.AboutTab = QtWidgets.QWidget()
        self.AboutTab.setObjectName("AboutTab")
        self.IconLabel = QtWidgets.QLabel(self.AboutTab)
        self.IconLabel.setGeometry(QtCore.QRect(15, 5, 40, 40))
        self.IconLabel.setText("")
        self.IconLabel.setPixmap(QtGui.QPixmap(":/icon/icon/main.ico"))
        self.IconLabel.setObjectName("IconLabel")
        self.IssueLabel = QtWidgets.QLabel(self.AboutTab)
        self.IssueLabel.setGeometry(QtCore.QRect(20, 110, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.IssueLabel.setFont(font)
        self.IssueLabel.setOpenExternalLinks(True)
        self.IssueLabel.setObjectName("IssueLabel")
        self.LatestVersionLabel = QtWidgets.QLabel(self.AboutTab)
        self.LatestVersionLabel.setGeometry(QtCore.QRect(20, 90, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LatestVersionLabel.setFont(font)
        self.LatestVersionLabel.setOpenExternalLinks(True)
        self.LatestVersionLabel.setObjectName("LatestVersionLabel")
        self.LicenseLabel = QtWidgets.QLabel(self.AboutTab)
        self.LicenseLabel.setGeometry(QtCore.QRect(20, 130, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LicenseLabel.setFont(font)
        self.LicenseLabel.setOpenExternalLinks(True)
        self.LicenseLabel.setObjectName("LicenseLabel")
        self.VersionLabel = QtWidgets.QLabel(self.AboutTab)
        self.VersionLabel.setGeometry(QtCore.QRect(20, 70, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.VersionLabel.setFont(font)
        self.VersionLabel.setObjectName("VersionLabel")
        self.SubTitleLabel = QtWidgets.QLabel(self.AboutTab)
        self.SubTitleLabel.setGeometry(QtCore.QRect(60, 30, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.SubTitleLabel.setFont(font)
        self.SubTitleLabel.setObjectName("SubTitleLabel")
        self.TabWidget.addTab(self.AboutTab, "")
        self.gridLayout.addWidget(self.TabWidget, 0, 0, 1, 1)

        self.retranslateUi(settingForm)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settingForm)

    def retranslateUi(self, settingForm):
        _translate = QtCore.QCoreApplication.translate
        settingForm.setWindowTitle(_translate("settingForm", "Settings"))
        self.LanguageLabel.setText(_translate("settingForm", "Language:"))
        self.LanguageComboBox.setItemText(0, _translate("settingForm", "English"))
        self.LanguageComboBox.setItemText(1, _translate("settingForm", "简体中文"))
        self.LanguageComboBox.setItemText(2, _translate("settingForm", "繁體中文"))
        self.ThemeLabel.setText(_translate("settingForm", "Theme:"))
        self.ThemeComboBox.setItemText(0, _translate("settingForm", "Light"))
        self.ThemeComboBox.setItemText(1, _translate("settingForm", "Dark"))
        self.FontLabel.setText(_translate("settingForm", "Font:"))
        self.FontPushButton.setText(_translate("settingForm", "Font"))
        self.EncodingLabel.setText(_translate("settingForm", "Encoding:"))
        self.EncodingComboBox.setItemText(0, _translate("settingForm", "UTF-8"))
        self.EncodingComboBox.setItemText(1, _translate("settingForm", "UTF-32"))
        self.EncodingComboBox.setItemText(2, _translate("settingForm", "GBK"))
        self.EncodingComboBox.setItemText(3, _translate("settingForm", "GB2312"))
        self.EncodingComboBox.setItemText(4, _translate("settingForm", "ISO-8859-1"))
        self.EncodingComboBox.setItemText(5, _translate("settingForm", "BIG5"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.GeneralTab), _translate("settingForm", "General"))
        self.IssueLabel.setText(_translate("settingForm", "<html><head/><body><p>Issue:&ensp;<a href=\"https://github.com/nixgnauhcuy/QtComMate/issues\"><span style=\" color:#0000ff;\">https://github.com/nixgnauhcuy/QtComMate/issues</span></a></p></body></html>"))
        self.LatestVersionLabel.setText(_translate("settingForm", "<html><head/><body><p>Latest Version:&ensp;<a href=\"https://github.com/nixgnauhcuy/QtComMate/releases\"><span style=\" color:#0000ff;\">https://github.com/nixgnauhcuy/QtComMate/releases</span></a></p></body></html>"))
        self.LicenseLabel.setText(_translate("settingForm", "<html><head/><body><p>License:&ensp;<a href=\"https://github.com/nixgnauhcuy/QtComMate/blob/main/LICENSE\"><span style=\" color:#0000ff;\">https://github.com/nixgnauhcuy/QtComMate/blob/main/LICENSE</span></a></p></body></html>"))
        self.VersionLabel.setText(_translate("settingForm", "Version: 1.1.0"))
        self.SubTitleLabel.setText(_translate("settingForm", "Simple Serial Port Tool Based on pyqt6"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.AboutTab), _translate("settingForm", "About"))
