# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AttackOptionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AttackOptionDialog(object):
    def setupUi(self, AttackOptionDialog):
        AttackOptionDialog.setObjectName("AttackOptionDialog")
        AttackOptionDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AttackOptionDialog.resize(716, 513)
        AttackOptionDialog.setMinimumSize(QtCore.QSize(716, 513))
        AttackOptionDialog.setMaximumSize(QtCore.QSize(716, 513))
        AttackOptionDialog.setStyleSheet("QDialog { background-color: black; }")
        self.buttonBox = QtWidgets.QDialogButtonBox(AttackOptionDialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 460, 241, 27))
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStyleSheet("QDialogButtonBox { background-color: black; }")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.Option_Table_Widget = QtWidgets.QTableWidget(AttackOptionDialog)
        self.Option_Table_Widget.setGeometry(QtCore.QRect(10, 10, 701, 441))
        self.Option_Table_Widget.setMaximumSize(QtCore.QSize(701, 441))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Option_Table_Widget.setFont(font)
        self.Option_Table_Widget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Option_Table_Widget.setStyleSheet("QTableWidget { color: white; background-color: #251313; }")
        self.Option_Table_Widget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.Option_Table_Widget.setDragEnabled(True)
        self.Option_Table_Widget.setAlternatingRowColors(False)
        self.Option_Table_Widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.Option_Table_Widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.Option_Table_Widget.setShowGrid(False)
        self.Option_Table_Widget.setGridStyle(QtCore.Qt.DashDotDotLine)
        self.Option_Table_Widget.setObjectName("Option_Table_Widget")
        self.Option_Table_Widget.setColumnCount(2)
        self.Option_Table_Widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Option_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Option_Table_Widget.setHorizontalHeaderItem(1, item)
        self.Option_Table_Widget.horizontalHeader().setCascadingSectionResizes(True)
        self.Option_Table_Widget.horizontalHeader().setDefaultSectionSize(290)
        self.Option_Table_Widget.horizontalHeader().setSortIndicatorShown(True)
        self.Option_Table_Widget.horizontalHeader().setStretchLastSection(True)
        self.Option_Table_Widget.verticalHeader().setDefaultSectionSize(30)
        self.Option_Table_Widget.verticalHeader().setHighlightSections(True)

        self.retranslateUi(AttackOptionDialog)
        self.buttonBox.accepted.connect(AttackOptionDialog.accept)
        self.buttonBox.rejected.connect(AttackOptionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AttackOptionDialog)

    def retranslateUi(self, AttackOptionDialog):
        _translate = QtCore.QCoreApplication.translate
        AttackOptionDialog.setWindowTitle(_translate("AttackOptionDialog", "Dialog"))
        self.Option_Table_Widget.setSortingEnabled(True)
        item = self.Option_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("AttackOptionDialog", "Required Parameters"))
        item = self.Option_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("AttackOptionDialog", "Required Values"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttackOptionDialog = QtWidgets.QDialog()
    ui = Ui_AttackOptionDialog()
    ui.setupUi(AttackOptionDialog)
    AttackOptionDialog.show()
    sys.exit(app.exec_())

