# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetColName.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(410, 300)
        Dialog.setMinimumSize(QtCore.QSize(410, 300))
        Dialog.setMaximumSize(QtCore.QSize(410, 300))
        self.PageSelect = QtWidgets.QComboBox(Dialog)
        self.PageSelect.setGeometry(QtCore.QRect(40, 80, 111, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.PageSelect.setFont(font)
        self.PageSelect.setObjectName("PageSelect")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.PageSelect.addItem("")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(200, 80, 171, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.CommitChange = QtWidgets.QPushButton(Dialog)
        self.CommitChange.setGeometry(QtCore.QRect(230, 170, 111, 41))
        self.CommitChange.setObjectName("CommitChange")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 50, 141, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 50, 111, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.PageSelect.setItemText(0, _translate("Dialog", "第一页"))
        self.PageSelect.setItemText(1, _translate("Dialog", "第二页"))
        self.PageSelect.setItemText(2, _translate("Dialog", "第三页"))
        self.PageSelect.setItemText(3, _translate("Dialog", "第四页"))
        self.PageSelect.setItemText(4, _translate("Dialog", "第五页"))
        self.PageSelect.setItemText(5, _translate("Dialog", "第六页"))
        self.PageSelect.setItemText(6, _translate("Dialog", "第七页"))
        self.PageSelect.setItemText(7, _translate("Dialog", "第八页"))
        self.PageSelect.setItemText(8, _translate("Dialog", "第九页"))
        self.CommitChange.setText(_translate("Dialog", "确认更改"))
        self.label.setText(_translate("Dialog", "请输入新栏目名"))
        self.label_2.setText(_translate("Dialog", "请选择栏目"))
