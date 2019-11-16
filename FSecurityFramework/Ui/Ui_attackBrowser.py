# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attackBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AttackBrowser(object):
    def setupUi(self, AttackBrowser):
        AttackBrowser.setObjectName("AttackBrowser")
        AttackBrowser.resize(971, 521)
        AttackBrowser.setStyleSheet("QWidget { background-color : black; }")
        self.verticalLayoutWidget = QtWidgets.QWidget(AttackBrowser)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 5, 951, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.textBrowser.setFont(font)
        self.textBrowser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textBrowser.setStyleSheet("QTextBrowser { color: white; background-color: #251313; }")
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit { background-color : white; color : black; }")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton { color: black; background-color: #6B00FF; }")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(AttackBrowser)
        QtCore.QMetaObject.connectSlotsByName(AttackBrowser)

    def retranslateUi(self, AttackBrowser):
        _translate = QtCore.QCoreApplication.translate
        AttackBrowser.setWindowTitle(_translate("AttackBrowser", "Form"))
        self.pushButton.setText(_translate("AttackBrowser", "Enter Command"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttackBrowser = QtWidgets.QWidget()
    ui = Ui_AttackBrowser()
    ui.setupUi(AttackBrowser)
    AttackBrowser.show()
    sys.exit(app.exec_())

