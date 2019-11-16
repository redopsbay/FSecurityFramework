# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GetInterfaceDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GetInterface_Dialog(object):
    def setupUi(self, GetInterface_Dialog):
        GetInterface_Dialog.setObjectName("GetInterface_Dialog")
        GetInterface_Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        GetInterface_Dialog.resize(391, 33)
        GetInterface_Dialog.setMinimumSize(QtCore.QSize(391, 33))
        GetInterface_Dialog.setMaximumSize(QtCore.QSize(391, 33))
        font = QtGui.QFont()
        font.setItalic(True)
        GetInterface_Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icons/FSecurity.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GetInterface_Dialog.setWindowIcon(icon)
        GetInterface_Dialog.setModal(True)
        self.horizontalLayoutWidget = QtWidgets.QWidget(GetInterface_Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 381, 29))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.horizontalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GetInterface_Dialog)
        self.buttonBox.accepted.connect(GetInterface_Dialog.accept)
        self.buttonBox.rejected.connect(GetInterface_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GetInterface_Dialog)

    def retranslateUi(self, GetInterface_Dialog):
        _translate = QtCore.QCoreApplication.translate
        GetInterface_Dialog.setWindowTitle(_translate("GetInterface_Dialog", "Enter the network interface to be use"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GetInterface_Dialog = QtWidgets.QDialog()
    ui = Ui_GetInterface_Dialog()
    ui.setupUi(GetInterface_Dialog)
    GetInterface_Dialog.show()
    sys.exit(app.exec_())

