# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'mainZfHCWm.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time
from components import *

from PyQt5 import QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(735, 530)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")


        # self.scrollArea = QScrollArea(self.centralwidget)
        # self.scrollArea.setGeometry(QRect(20, 150, 701, 341))
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 699, 339))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.vl = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        # self.vl.setContentsMargins(0, 0, 0, 0)
        # self.vl.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        # self.vl.setObjectName("vl")
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QRect(20, 150, 701, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 699, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(
            self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 701, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        # self.verticalLayoutWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # self.verticalLayoutWidget.setMaximumHeight(200)
        self.vl = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.vl.setObjectName("vl")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidgetResizable(True)

        ####### Daha sonra Qt designerla düzenle
        self.logOut_button = QPushButton(self.centralwidget)
        self.logOut_button.setObjectName("logOut_button")
        self.logOut_button.setGeometry(QRect(670,10,50,25))
        self.logOut_button.setText("Log Out")
        #######
        self.symboledit = QLineEdit(self.centralwidget)
        self.symboledit.setObjectName(u"symboledit")
        self.symboledit.setGeometry(QRect(20, 60, 101, 23))
        self.model = QStandardItemModel()
        completer = QCompleter(self.model)
        completer.setCaseSensitivity(0)
        self.symboledit.setCompleter(completer)

        self.quantityedit = QLineEdit(self.centralwidget)
        self.quantityedit.setObjectName(u"quantityedit")
        self.quantityedit.setGeometry(QRect(130, 60, 51, 23))

        self.status = QLabel(self.centralwidget)
        self.status.setObjectName(u"status")
        self.status.setGeometry(QRect(20,85, 200,23))
        self.status.hide()
        

        self.addbutton = QPushButton(self.centralwidget)
        self.addbutton.setObjectName(u"addbutton")
        self.addbutton.setGeometry(QRect(190, 60, 51, 23))
        self.donebutton = QPushButton(self.centralwidget)
        self.donebutton.setObjectName(u"donebutton")
        self.donebutton.setGeometry(QRect(240, 60, 51, 23))

        self.sharesheader = QLabel(self.centralwidget)
        self.sharesheader.setObjectName(u"sharesheader")
        self.sharesheader.setGeometry(QRect(20, 30, 61, 16))
        self.sharesheader.setStyleSheet(u"font: 12pt bold \"Sans Serif\";")

        # SELL BLOCK
        self.selledit = QLineEdit(self.centralwidget)
        self.selledit.setObjectName(u"selledit")
        self.selledit.setGeometry(QRect(310, 60, 91, 23))
        self.applybutton = QPushButton(self.centralwidget)
        self.applybutton.setObjectName(u"applybutton")
        self.applybutton.setGeometry(QRect(410, 60, 41, 23))
        self.sellheader = QLabel(self.centralwidget)
        self.sellheader.setObjectName(u"sellheader")
        self.sellheader.setGeometry(QRect(300, 30, 31, 16))
        self.sellheader.setStyleSheet(u"font: 12pt bold \"Sans Serif\";")

        self.sell = sell_widget(self.centralwidget)

        # hide Sell block elements
        self.hideSellBlockHeader()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 585, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def status_success(self):
        self.status.show()
        self.status.setStyleSheet("color: green")
        self.status.setText("Successfully added!")
        
        timer = QTimer()
        timer.singleShot(2000, self.status.hide)

    def status_fail(self, error):
        
        self.status.show()
        self.status.setStyleSheet("color: red")
        
        if error == "WRONG_SYM":
            self.status.setText("Please enter a valid symbol or quantity!")
        elif error == "MISSING_INP":    
            self.status.setText("Please input all fields!")

        timer = QTimer()
        timer.singleShot(2000, self.status.hide)


    def hideSellBlockHeader(self):
        self.selledit.hide()
        self.applybutton.hide()
        self.sellheader.hide()

    def showSellBlockHeader(self):
        self.sellheader.show()
        self.selledit.show()
        self.applybutton.show()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.symboledit.setText("")
        self.symboledit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Stock symbol", None))
        self.quantityedit.setText("")
        self.quantityedit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Quantity", None))
        self.selledit.setText("")
        self.selledit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"To sell (TL)", None))
        self.addbutton.setText(
            QCoreApplication.translate("MainWindow", u"Add", None))
        self.donebutton.setText(
            QCoreApplication.translate("MainWindow", u"Done", None))
        self.applybutton.setText(
            QCoreApplication.translate("MainWindow", u"Apply", None))
        self.sharesheader.setText(
            QCoreApplication.translate("MainWindow", u"Shares", None))
        self.sellheader.setText(
            QCoreApplication.translate("MainWindow", u"Sell", None))
    # retranslateUi


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
