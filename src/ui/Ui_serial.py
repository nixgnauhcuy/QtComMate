from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_serialForm(object):
    def setupUi(self, serialForm):
        serialForm.setObjectName("serialForm")
        serialForm.resize(810, 501)
        serialForm.setMinimumSize(QtCore.QSize(810, 501))
        serialForm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(serialForm)
        self.verticalLayout.setContentsMargins(5, 0, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serialReceiveAreaGroupBox = QtWidgets.QGroupBox(parent=serialForm)
        self.serialReceiveAreaGroupBox.setMinimumSize(QtCore.QSize(800, 238))
        self.serialReceiveAreaGroupBox.setCheckable(False)
        self.serialReceiveAreaGroupBox.setObjectName("serialReceiveAreaGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.serialReceiveAreaGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.serialReceiveFormLayout = QtWidgets.QFormLayout()
        self.serialReceiveFormLayout.setObjectName("serialReceiveFormLayout")
        self.serialComboBox = SerialPortComboBox(parent=self.serialReceiveAreaGroupBox)
        self.serialComboBox.setMinimumSize(QtCore.QSize(0, 0))
        self.serialComboBox.setMaximumSize(QtCore.QSize(170, 21))
        self.serialComboBox.setObjectName("serialComboBox")
        self.serialReceiveFormLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.serialComboBox)
        self.serialBaudrateLabel = QtWidgets.QLabel(parent=self.serialReceiveAreaGroupBox)
        self.serialBaudrateLabel.setObjectName("serialBaudrateLabel")
        self.serialReceiveFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialBaudrateLabel)
        self.serialBaudrateComboBox = QtWidgets.QComboBox(parent=self.serialReceiveAreaGroupBox)
        self.serialBaudrateComboBox.setObjectName("serialBaudrateComboBox")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialBaudrateComboBox.addItem("")
        self.serialReceiveFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialBaudrateComboBox)
        self.serialStopBitLabel = QtWidgets.QLabel(parent=self.serialReceiveAreaGroupBox)
        self.serialStopBitLabel.setObjectName("serialStopBitLabel")
        self.serialReceiveFormLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialStopBitLabel)
        self.serialStopBitComboBox = QtWidgets.QComboBox(parent=self.serialReceiveAreaGroupBox)
        self.serialStopBitComboBox.setObjectName("serialStopBitComboBox")
        self.serialStopBitComboBox.addItem("")
        self.serialStopBitComboBox.addItem("")
        self.serialStopBitComboBox.addItem("")
        self.serialReceiveFormLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialStopBitComboBox)
        self.serialDataBitLabel = QtWidgets.QLabel(parent=self.serialReceiveAreaGroupBox)
        self.serialDataBitLabel.setObjectName("serialDataBitLabel")
        self.serialReceiveFormLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialDataBitLabel)
        self.serialDataBitcomboBox = QtWidgets.QComboBox(parent=self.serialReceiveAreaGroupBox)
        self.serialDataBitcomboBox.setObjectName("serialDataBitcomboBox")
        self.serialDataBitcomboBox.addItem("")
        self.serialDataBitcomboBox.addItem("")
        self.serialDataBitcomboBox.addItem("")
        self.serialDataBitcomboBox.addItem("")
        self.serialReceiveFormLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialDataBitcomboBox)
        self.serialChecksumBitLabel = QtWidgets.QLabel(parent=self.serialReceiveAreaGroupBox)
        self.serialChecksumBitLabel.setObjectName("serialChecksumBitLabel")
        self.serialReceiveFormLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialChecksumBitLabel)
        self.serialChecksumBitComboBox = QtWidgets.QComboBox(parent=self.serialReceiveAreaGroupBox)
        self.serialChecksumBitComboBox.setObjectName("serialChecksumBitComboBox")
        self.serialChecksumBitComboBox.addItem("")
        self.serialChecksumBitComboBox.addItem("")
        self.serialChecksumBitComboBox.addItem("")
        self.serialChecksumBitComboBox.addItem("")
        self.serialChecksumBitComboBox.addItem("")
        self.serialReceiveFormLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialChecksumBitComboBox)
        self.serialReceiveHexCheckBox = QtWidgets.QCheckBox(parent=self.serialReceiveAreaGroupBox)
        self.serialReceiveHexCheckBox.setObjectName("serialReceiveHexCheckBox")
        self.serialReceiveFormLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialReceiveHexCheckBox)
        self.serialReceiveTimestampCheckBox = QtWidgets.QCheckBox(parent=self.serialReceiveAreaGroupBox)
        self.serialReceiveTimestampCheckBox.setObjectName("serialReceiveTimestampCheckBox")
        self.serialReceiveFormLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialReceiveTimestampCheckBox)
        self.serialConnectComPushButton = QtWidgets.QPushButton(parent=self.serialReceiveAreaGroupBox)
        self.serialConnectComPushButton.setObjectName("serialConnectComPushButton")
        self.serialReceiveFormLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.serialConnectComPushButton)
        self.serialReceiveClearPushButton = QtWidgets.QPushButton(parent=self.serialReceiveAreaGroupBox)
        self.serialReceiveClearPushButton.setObjectName("serialReceiveClearPushButton")
        self.serialReceiveFormLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.serialReceiveClearPushButton)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.serialReceiveFormLayout)
        self.serialReceivePlainTextEdit = QtWidgets.QPlainTextEdit(parent=self.serialReceiveAreaGroupBox)
        self.serialReceivePlainTextEdit.setUndoRedoEnabled(False)
        self.serialReceivePlainTextEdit.setReadOnly(True)
        self.serialReceivePlainTextEdit.setObjectName("serialReceivePlainTextEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.serialReceivePlainTextEdit)
        self.verticalLayout.addWidget(self.serialReceiveAreaGroupBox)
        self.serialTabWidget = QtWidgets.QTabWidget(parent=serialForm)
        self.serialTabWidget.setObjectName("serialTabWidget")
        self.serialTab_1 = QtWidgets.QWidget()
        self.serialTab_1.setObjectName("serialTab_1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.serialTab_1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.serialSendPlainTextEdit = QtWidgets.QPlainTextEdit(parent=self.serialTab_1)
        self.serialSendPlainTextEdit.setObjectName("serialSendPlainTextEdit")
        self.gridLayout_3.addWidget(self.serialSendPlainTextEdit, 0, 0, 3, 4)
        self.serialSendHexCheckBox = QtWidgets.QCheckBox(parent=self.serialTab_1)
        self.serialSendHexCheckBox.setObjectName("serialSendHexCheckBox")
        self.gridLayout_3.addWidget(self.serialSendHexCheckBox, 0, 4, 1, 1)
        self.serialSendPushButton = QtWidgets.QPushButton(parent=self.serialTab_1)
        self.serialSendPushButton.setObjectName("serialSendPushButton")
        self.gridLayout_3.addWidget(self.serialSendPushButton, 1, 4, 1, 1)
        self.serialSendClearPushButton = QtWidgets.QPushButton(parent=self.serialTab_1)
        self.serialSendClearPushButton.setObjectName("serialSendClearPushButton")
        self.gridLayout_3.addWidget(self.serialSendClearPushButton, 2, 4, 1, 1)
        self.serialSoftFlowControlGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_1)
        self.serialSoftFlowControlGroupBox.setObjectName("serialSoftFlowControlGroupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.serialSoftFlowControlGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.serialSoftFlowControlCheckBox = QtWidgets.QCheckBox(parent=self.serialSoftFlowControlGroupBox)
        self.serialSoftFlowControlCheckBox.setObjectName("serialSoftFlowControlCheckBox")
        self.horizontalLayout.addWidget(self.serialSoftFlowControlCheckBox)
        self.gridLayout_3.addWidget(self.serialSoftFlowControlGroupBox, 3, 0, 1, 1)
        self.serialSendRepeatGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_1)
        self.serialSendRepeatGroupBox.setObjectName("serialSendRepeatGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.serialSendRepeatGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.serialSendRepeatCheckBox = QtWidgets.QCheckBox(parent=self.serialSendRepeatGroupBox)
        self.serialSendRepeatCheckBox.setText("")
        self.serialSendRepeatCheckBox.setObjectName("serialSendRepeatCheckBox")
        self.gridLayout_4.addWidget(self.serialSendRepeatCheckBox, 0, 0, 1, 1)
        self.serialSendRepeatUnitLabel = QtWidgets.QLabel(parent=self.serialSendRepeatGroupBox)
        self.serialSendRepeatUnitLabel.setObjectName("serialSendRepeatUnitLabel")
        self.gridLayout_4.addWidget(self.serialSendRepeatUnitLabel, 0, 2, 1, 1)
        self.serialSendRepeatDurationLineEdit = QtWidgets.QLineEdit(parent=self.serialSendRepeatGroupBox)
        self.serialSendRepeatDurationLineEdit.setObjectName("serialSendRepeatDurationLineEdit")
        self.gridLayout_4.addWidget(self.serialSendRepeatDurationLineEdit, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.serialSendRepeatGroupBox, 3, 2, 1, 1)
        self.serialSendLineFeedGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_1)
        self.serialSendLineFeedGroupBox.setObjectName("serialSendLineFeedGroupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.serialSendLineFeedGroupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.serialSendLineFeedComboBox = QtWidgets.QComboBox(parent=self.serialSendLineFeedGroupBox)
        self.serialSendLineFeedComboBox.setObjectName("serialSendLineFeedComboBox")
        self.serialSendLineFeedComboBox.addItem("")
        self.serialSendLineFeedComboBox.addItem("")
        self.serialSendLineFeedComboBox.addItem("")
        self.serialSendLineFeedComboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.serialSendLineFeedComboBox)
        self.gridLayout_3.addWidget(self.serialSendLineFeedGroupBox, 3, 3, 1, 1)
        self.serialHardFlowControlGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_1)
        self.serialHardFlowControlGroupBox.setObjectName("serialHardFlowControlGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.serialHardFlowControlGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.serialHardFlowControlDSRDTRCheckBox = QtWidgets.QCheckBox(parent=self.serialHardFlowControlGroupBox)
        self.serialHardFlowControlDSRDTRCheckBox.setObjectName("serialHardFlowControlDSRDTRCheckBox")
        self.horizontalLayout_2.addWidget(self.serialHardFlowControlDSRDTRCheckBox)
        self.serialHardFlowControlRTSCTSCheckBox = QtWidgets.QCheckBox(parent=self.serialHardFlowControlGroupBox)
        self.serialHardFlowControlRTSCTSCheckBox.setObjectName("serialHardFlowControlRTSCTSCheckBox")
        self.horizontalLayout_2.addWidget(self.serialHardFlowControlRTSCTSCheckBox)
        self.gridLayout_3.addWidget(self.serialHardFlowControlGroupBox, 3, 1, 1, 1)
        self.serialTabWidget.addTab(self.serialTab_1, "")
        self.serialTab_2 = QtWidgets.QWidget()
        self.serialTab_2.setObjectName("serialTab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.serialTab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.serialFileSendGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_2)
        self.serialFileSendGroupBox.setObjectName("serialFileSendGroupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.serialFileSendGroupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.serialFileSendLabel = QtWidgets.QLabel(parent=self.serialFileSendGroupBox)
        self.serialFileSendLabel.setObjectName("serialFileSendLabel")
        self.horizontalLayout_4.addWidget(self.serialFileSendLabel)
        self.serialFileSendLineEdit = QtWidgets.QLineEdit(parent=self.serialFileSendGroupBox)
        self.serialFileSendLineEdit.setReadOnly(True)
        self.serialFileSendLineEdit.setObjectName("serialFileSendLineEdit")
        self.horizontalLayout_4.addWidget(self.serialFileSendLineEdit)
        self.serialFileSelectPushButton = QtWidgets.QPushButton(parent=self.serialFileSendGroupBox)
        self.serialFileSelectPushButton.setObjectName("serialFileSelectPushButton")
        self.horizontalLayout_4.addWidget(self.serialFileSelectPushButton)
        self.serialFileSendPushButton = QtWidgets.QPushButton(parent=self.serialFileSendGroupBox)
        self.serialFileSendPushButton.setObjectName("serialFileSendPushButton")
        self.horizontalLayout_4.addWidget(self.serialFileSendPushButton)
        self.gridLayout_5.addWidget(self.serialFileSendGroupBox, 0, 1, 1, 1)
        self.serialFileSaveGroupBox = QtWidgets.QGroupBox(parent=self.serialTab_2)
        self.serialFileSaveGroupBox.setObjectName("serialFileSaveGroupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.serialFileSaveGroupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.serialFilePathSaveSelectPushButton = QtWidgets.QPushButton(parent=self.serialFileSaveGroupBox)
        self.serialFilePathSaveSelectPushButton.setObjectName("serialFilePathSaveSelectPushButton")
        self.gridLayout_6.addWidget(self.serialFilePathSaveSelectPushButton, 0, 2, 1, 1)
        self.serialFilePathSaveLineEdit = QtWidgets.QLineEdit(parent=self.serialFileSaveGroupBox)
        self.serialFilePathSaveLineEdit.setReadOnly(True)
        self.serialFilePathSaveLineEdit.setObjectName("serialFilePathSaveLineEdit")
        self.gridLayout_6.addWidget(self.serialFilePathSaveLineEdit, 0, 1, 1, 1)
        self.serialFilePathSaveLabel = QtWidgets.QLabel(parent=self.serialFileSaveGroupBox)
        self.serialFilePathSaveLabel.setObjectName("serialFilePathSaveLabel")
        self.gridLayout_6.addWidget(self.serialFilePathSaveLabel, 0, 0, 1, 1)
        self.serialFileSavePushButton = QtWidgets.QPushButton(parent=self.serialFileSaveGroupBox)
        self.serialFileSavePushButton.setObjectName("serialFileSavePushButton")
        self.gridLayout_6.addWidget(self.serialFileSavePushButton, 0, 3, 1, 1)
        self.gridLayout_5.addWidget(self.serialFileSaveGroupBox, 1, 1, 1, 1)
        self.serialTabWidget.addTab(self.serialTab_2, "")
        self.verticalLayout.addWidget(self.serialTabWidget)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(serialForm)
        self.serialTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(serialForm)

    def retranslateUi(self, serialForm):
        _translate = QtCore.QCoreApplication.translate
        serialForm.setWindowTitle(_translate("serialForm", "Form"))
        self.serialReceiveAreaGroupBox.setTitle(_translate("serialForm", "Receive Area"))
        self.serialBaudrateLabel.setText(_translate("serialForm", "Baudrate"))
        self.serialBaudrateComboBox.setItemText(0, _translate("serialForm", "custom"))
        self.serialBaudrateComboBox.setItemText(1, _translate("serialForm", "110"))
        self.serialBaudrateComboBox.setItemText(2, _translate("serialForm", "300"))
        self.serialBaudrateComboBox.setItemText(3, _translate("serialForm", "600"))
        self.serialBaudrateComboBox.setItemText(4, _translate("serialForm", "1200"))
        self.serialBaudrateComboBox.setItemText(5, _translate("serialForm", "2400"))
        self.serialBaudrateComboBox.setItemText(6, _translate("serialForm", "4800"))
        self.serialBaudrateComboBox.setItemText(7, _translate("serialForm", "9600"))
        self.serialBaudrateComboBox.setItemText(8, _translate("serialForm", "19200"))
        self.serialBaudrateComboBox.setItemText(9, _translate("serialForm", "38400"))
        self.serialBaudrateComboBox.setItemText(10, _translate("serialForm", "57600"))
        self.serialBaudrateComboBox.setItemText(11, _translate("serialForm", "76800"))
        self.serialBaudrateComboBox.setItemText(12, _translate("serialForm", "115200"))
        self.serialBaudrateComboBox.setItemText(13, _translate("serialForm", "128000"))
        self.serialBaudrateComboBox.setItemText(14, _translate("serialForm", "230400"))
        self.serialBaudrateComboBox.setItemText(15, _translate("serialForm", "256000"))
        self.serialBaudrateComboBox.setItemText(16, _translate("serialForm", "460800"))
        self.serialBaudrateComboBox.setItemText(17, _translate("serialForm", "512000"))
        self.serialBaudrateComboBox.setItemText(18, _translate("serialForm", "576000"))
        self.serialBaudrateComboBox.setItemText(19, _translate("serialForm", "921600"))
        self.serialBaudrateComboBox.setItemText(20, _translate("serialForm", "1000000"))
        self.serialBaudrateComboBox.setItemText(21, _translate("serialForm", "1500000"))
        self.serialBaudrateComboBox.setItemText(22, _translate("serialForm", "2000000"))
        self.serialStopBitLabel.setText(_translate("serialForm", "Stopbit"))
        self.serialStopBitComboBox.setItemText(0, _translate("serialForm", "1"))
        self.serialStopBitComboBox.setItemText(1, _translate("serialForm", "1.5"))
        self.serialStopBitComboBox.setItemText(2, _translate("serialForm", "2"))
        self.serialDataBitLabel.setText(_translate("serialForm", "Databit"))
        self.serialDataBitcomboBox.setItemText(0, _translate("serialForm", "5"))
        self.serialDataBitcomboBox.setItemText(1, _translate("serialForm", "6"))
        self.serialDataBitcomboBox.setItemText(2, _translate("serialForm", "7"))
        self.serialDataBitcomboBox.setItemText(3, _translate("serialForm", "8"))
        self.serialChecksumBitLabel.setText(_translate("serialForm", "Checksum"))
        self.serialChecksumBitComboBox.setItemText(0, _translate("serialForm", "None"))
        self.serialChecksumBitComboBox.setItemText(1, _translate("serialForm", "Even"))
        self.serialChecksumBitComboBox.setItemText(2, _translate("serialForm", "Odd"))
        self.serialChecksumBitComboBox.setItemText(3, _translate("serialForm", "Mark"))
        self.serialChecksumBitComboBox.setItemText(4, _translate("serialForm", "Space"))
        self.serialReceiveHexCheckBox.setText(_translate("serialForm", "Hex"))
        self.serialReceiveTimestampCheckBox.setText(_translate("serialForm", "Timestamp"))
        self.serialConnectComPushButton.setText(_translate("serialForm", "Connect"))
        self.serialReceiveClearPushButton.setText(_translate("serialForm", "Clear"))
        self.serialSendHexCheckBox.setText(_translate("serialForm", "Hex"))
        self.serialSendPushButton.setText(_translate("serialForm", "Send"))
        self.serialSendClearPushButton.setText(_translate("serialForm", "Clear"))
        self.serialSoftFlowControlGroupBox.setTitle(_translate("serialForm", "Software Flow Control"))
        self.serialSoftFlowControlCheckBox.setText(_translate("serialForm", "xon/xoff"))
        self.serialSendRepeatGroupBox.setTitle(_translate("serialForm", "Repeat"))
        self.serialSendRepeatUnitLabel.setText(_translate("serialForm", "ms"))
        self.serialSendLineFeedGroupBox.setTitle(_translate("serialForm", "New Line"))
        self.serialSendLineFeedComboBox.setItemText(0, _translate("serialForm", "None"))
        self.serialSendLineFeedComboBox.setItemText(1, _translate("serialForm", "\\r\\n"))
        self.serialSendLineFeedComboBox.setItemText(2, _translate("serialForm", "\\n"))
        self.serialSendLineFeedComboBox.setItemText(3, _translate("serialForm", "\\r"))
        self.serialHardFlowControlGroupBox.setTitle(_translate("serialForm", "Hardware Flow Control"))
        self.serialHardFlowControlDSRDTRCheckBox.setText(_translate("serialForm", "dsr/dtr"))
        self.serialHardFlowControlRTSCTSCheckBox.setText(_translate("serialForm", "rts/cts"))
        self.serialTabWidget.setTabText(self.serialTabWidget.indexOf(self.serialTab_1), _translate("serialForm", "Send Area"))
        self.serialFileSendGroupBox.setTitle(_translate("serialForm", "File Send"))
        self.serialFileSendLabel.setText(_translate("serialForm", "File"))
        self.serialFileSelectPushButton.setText(_translate("serialForm", "Select"))
        self.serialFileSendPushButton.setText(_translate("serialForm", "Send"))
        self.serialFileSaveGroupBox.setTitle(_translate("serialForm", "File Save"))
        self.serialFilePathSaveSelectPushButton.setText(_translate("serialForm", "Select"))
        self.serialFilePathSaveLabel.setText(_translate("serialForm", "Path"))
        self.serialFileSavePushButton.setText(_translate("serialForm", "Start"))
        self.serialTabWidget.setTabText(self.serialTabWidget.indexOf(self.serialTab_2), _translate("serialForm", "File"))
from widgets.serialPortComboBox import SerialPortComboBox