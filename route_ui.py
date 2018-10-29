# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'route.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_route(object):
    def setupUi(self, route):
        route.setObjectName("route")
        route.resize(644, 461)
        self.buttonBox = QtWidgets.QDialogButtonBox(route)
        self.buttonBox.setGeometry(QtCore.QRect(30, 170, 571, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.textBrowser = QtWidgets.QTextBrowser(route)
        self.textBrowser.setGeometry(QtCore.QRect(60, 40, 521, 91))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(route)
        self.textBrowser_2.setGeometry(QtCore.QRect(60, 220, 511, 192))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.retranslateUi(route)
        self.buttonBox.accepted.connect(route.accept)
        self.buttonBox.rejected.connect(route.reject)
        QtCore.QMetaObject.connectSlotsByName(route)

    def retranslateUi(self, route):
        _translate = QtCore.QCoreApplication.translate
        route.setWindowTitle(_translate("route", "route"))

