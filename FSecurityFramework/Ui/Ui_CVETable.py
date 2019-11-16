# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CVETable.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CVETable(object):
    def setupUi(self, CVETable):
        CVETable.setObjectName("CVETable")
        CVETable.resize(971, 521)
        CVETable.setMinimumSize(QtCore.QSize(971, 521))
        CVETable.setMaximumSize(QtCore.QSize(971, 521))
        self.tableWidget = QtWidgets.QTableWidget(CVETable)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 971, 521))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)

        self.retranslateUi(CVETable)
        QtCore.QMetaObject.connectSlotsByName(CVETable)

    def retranslateUi(self, CVETable):
        _translate = QtCore.QCoreApplication.translate
        CVETable.setWindowTitle(_translate("CVETable", "CVE"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CVETable", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CVETable", "Title"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("CVETable", "Description"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("CVETable", "Platform"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("CVETable", "Version"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("CVETable", "CVE_Author"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("CVETable", "Documentation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CVETable = QtWidgets.QWidget()
    ui = Ui_CVETable()
    ui.setupUi(CVETable)
    CVETable.show()
    sys.exit(app.exec_())

