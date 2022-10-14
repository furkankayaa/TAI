import sys
import os
from functools import partial
from hashlib import sha256
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ui_main import Ui_MainWindow
from components import *

import requests
import http.client
import json
import csv

import sqlite3

connection = sqlite3.connect("stock_seller.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE if not exists users(
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)""")
cursor.execute("""CREATE TABLE if not exists stocks(
    userid INTEGER NOT NULL UNIQUE,
    shares text,
    quantity int
)""")

connection.commit()
connection.close()


class Login_screen(QDialog):
    def __init__(self):
        super(Login_screen, self).__init__()
        loadUi("login.ui", self)
        self.loginButton.clicked.connect(self.logIn)
        self.signupButton.clicked.connect(self.signUp_screen)

        self.show()

    def success(self, uid):
        self.program = StockSeller(uid)
        self.accept()
        # self.program.show()

    @pyqtSlot()
    def signUp_screen(self):
        self.createAcc = SignUp_screen()
        self.createAcc.open()

    @pyqtSlot()
    def logIn(self):
        user = self.nameEdit.text()
        password = self.pwEdit.text()

        hashed = hash_pw(password)

        if user == "" or password == "":
            self.status.setText("Please input all fields!")
        else:
            conn = sqlite3.connect("stock_seller.db")
            cur = conn.cursor()
            find = """SELECT password, userid FROM users WHERE username = ?"""
            cur.execute(find, (user,))
            result = cur.fetchone()
            conn.close()
            if result != None:
                result_pw = result[0]
                uid = result[1]
                if result_pw == hashed:
                    self.success(uid)
                    # self.close()
                    self.status.setText("")
                else:
                    self.status.setText("Invalid username or password!")
            else:
                self.status.setText("Invalid username or password!")

    def closeEvent(self, event):
        sys.exit()


@pyqtSlot()
class SignUp_screen(QDialog):
    def __init__(self):
        super(SignUp_screen, self).__init__()
        loadUi("signup.ui", self)
        self.setWindowModality(Qt.ApplicationModal)
        self.signupButton.clicked.connect(self.signUp)

    @pyqtSlot()
    def signUp(self):
        user = self.nameEdit.text()
        password = self.pwEdit.text()
        confirm_pw = self.confirm_pw.text()

        hashed = hash_pw(password)

        isExists = self.user_exists(user)

        if user == "" or password == "" or confirm_pw == "":
            self.status.setText("Please input all fields!")
        elif password != confirm_pw:
            self.status.setText("Confirm password does not match!")
        elif isExists:
            self.status.setText("Username is already taken!")
        else:
            try:
                conn = sqlite3.connect("stock_seller.db")
                cur = conn.cursor()
                insert = """INSERT into users (username, password) values (?,?)"""
                cur.execute(insert, (user, hashed))
                conn.commit()
                conn.close()

                self.status.setText("Successfully signed up!")
            except Exception as error:
                self.status.setText("err code: " + str(error))

    def user_exists(self, username):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        query = "SELECT count(*) from users WHERE username = ?"
        cur.execute(query, (username,))
        fetch = cur.fetchone()[0]
        conn.close()
        if fetch != 0:
            return True
        return False


# loading modal self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.FramelessWindowHint)
class Loading_modal(QDialog):
    pass


class StockSeller(QMainWindow, Ui_MainWindow):
    def __init__(self, userid, parent=None):
        super(StockSeller, self).__init__()
        self.shares_list = []
        self.quantity_list = []
        self.stocks_dict = {}

        self.to_be_sold = []
        self.shares_widgets = []
        self.uid = userid
        self.totalSharesValue = 0
        self.sellVal = 0
        self.allDoneClicked = False
        self.return_to_login = False

        self.setupUi(self)
        self.get_stocks()
        self.events()
        self.append_stocks_to_list()

        self.show()

    def events(self):
        self.addbutton.clicked.connect(self.addShares)
        self.applybutton.clicked.connect(self.toSellApply)
        self.donebutton.clicked.connect(self.allDone)
        self.logOut_button.clicked.connect(self.logOut)
        self.remove_button.clicked.connect(self.removeStock)

    def append_stocks_to_list(self):
        self.shares_widgets.clear()
        for i in range(self.vl.count()):
            widget_i = self.vl.itemAt(i).widget()
            self.shares_widgets.append(widget_i)

    def get_stocks(self):

        # Güncel fiyatlar, API request

        # conn = http.client.HTTPSConnection("api.collectapi.com")
        # headers = {
        #         'content-type': "application/json",
        #         'authorization': "apikey apikey 6OAMWx40dqREJs2f3CQtT9:0nkBODcCViCZpC8zvsM2I0"
        #         }

        # conn.request("GET", "/economy/liveBorsa", headers=headers)

        # res = conn.getresponse()
        # self.data = res.read()

        # self.data = self.data.decode("utf-8")
        # self.data = json.loads(self.data)

        # with open("stocks.json","w") as out:
        #     json.dump(self.data, out)
        ###

        # Json dosyasına kaydedilmiş data
        self.data = ""
        with open("stocks.json") as readFile:
            self.data = json.load(readFile)
        ###

        # add stock name and corresponding prices into dict
        for i in self.data['result']:
            if not i['name'].startswith('X'):
                self.stocks_dict[i['name']] = i['price']

        for symbol in self.stocks_dict.keys():
            self.model.appendRow(QStandardItem(symbol))
        self.show_shares()

    def generateSharesBlock(self, symbol, quantity, id):
        listitem = List_item()
        listitem.item_id = id
        listitem.stock_symbol.setText(symbol)
        listitem.stock_price.setText(str(self.stocks_dict[symbol]))
        listitem.stock_quantity.setText(str(quantity))
        listitem.setMaximumHeight(50)
        self.vl.addWidget(listitem)

    @pyqtSlot()
    def addShares(self):
        if self.allDoneClicked == True and self.symboledit.text() != '' and self.quantityedit.text() != '':
            self.hideSellBlockHeader()
            self.selledit.clear()
            self.allDoneClicked = False

        if self.symboledit.text() != '' and self.quantityedit.text() != '' and int(self.quantityedit.text()) != 0:
            symbol = self.symboledit.text().upper().strip()
            quantity = self.quantityedit.text()

            if symbol in self.stocks_dict.keys() and quantity.isdigit():
                quantity = int(quantity)
                self.status_success()
                # insert stock into database
                self.insert_stock(self.uid, symbol, quantity)
                self.show_shares()
                self.append_stocks_to_list()

                # log csv
                buy_value = self.stocks_dict[symbol]*quantity
                log_shares(self.uid, symbol, quantity, buy_value, "BUY")

                self.symboledit.clear()
                self.quantityedit.clear()
            else:
                self.status_fail("WRONG_SYM")
        else:
            self.status_fail("MISSING_INP")

    def show_shares(self):
        # delete all widgets in layout
        for i in reversed(range(self.vl.count())):
            self.vl.itemAt(i).widget().setParent(None)
        # clear list before appending all from db again
        self.shares_list.clear()
        self.quantity_list.clear()
        self.totalSharesValue = 0
        for stock_sym, stock_qt in self.stocks_in_db(self.uid):
            # update total shares value
            self.totalSharesValue += self.stocks_dict[stock_sym]*stock_qt

            self.shares_list.append(stock_sym)
            self.quantity_list.append(stock_qt)
            self.generateSharesBlock(stock_sym, stock_qt, self.uid)

    def stocks_in_db(self, id):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        query = "SELECT shares, quantity FROM stocks WHERE userid = ?"
        cur.execute(query, (id,))
        fetch = cur.fetchall()
        conn.close()
        return fetch

    def count_stocks(self, id):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        query = "SELECT count(*) FROM stocks WHERE userid = ?"
        cur.execute(query, (id,))
        fetch = cur.fetchone()
        conn.close()
        if fetch != None:
            return fetch[0]
        return 0

    def insert_stock(self, id, share, qt):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        query = """SELECT quantity FROM stocks WHERE shares = ? and userid = ?"""
        cur.execute(query, (share, id))
        fetch = cur.fetchone()
        if fetch == None:
            insert = """INSERT into stocks (userid, shares, quantity) values (?,?,?)"""
            cur.execute(insert, (id, share, qt))
            conn.commit()
        else:
            update = """UPDATE stocks SET quantity = ? WHERE shares = ? and userid = ?"""
            new_qt = qt + fetch[0]
            cur.execute(update, (new_qt, share, id))
            conn.commit()
        conn.close()

    # 07.07 sadece ilk item için işlemler yapıldı
    @pyqtSlot()
    def toSellApply(self):

        if self.selledit.text() != '' and int(self.selledit.text()) <= self.totalSharesValue and int(self.selledit.text()) != 0:
            for w in self.shares_widgets:
                w.resetSlider()
                w.hideSellBlockWidget()
                self.hideRatioLabels
                w.hideResult()
                self.result_label.hide()
                if w.checkBox.isChecked():
                    self.to_be_sold.append(w)

            if len(self.to_be_sold) != 0:
                for w in self.shares_widgets:
                    w.checkBox.setEnabled(False)
                self.sellVal = int(self.selledit.text())
                self.sell_value_label.setText(
                    f"Sell Value: {0}/{self.sellVal}")

                widget_i = self.to_be_sold[0]
                slider_i = widget_i.horizontalSlider
                if len(self.to_be_sold) != 0:

                    widget_i.showSellBlockWidget()
                    self.showRatioLabels()
                    list_index = self.shares_list.index(
                        widget_i.stock_symbol.text())
                    curr_stock_value = float(
                        self.stocks_dict[self.shares_list[list_index]])*int(self.quantity_list[list_index])
                    ratio = 100 if curr_stock_value > self.sellVal \
                        else 100*curr_stock_value/self.sellVal
                    widget_i.initSlider(int(ratio))
                    slider_i.valueChanged.connect(
                        partial(self.sliderOnChange, widget_i))

                    widget_i.buttonBox.accepted.connect(partial(self.OK, 1))
                    widget_i.buttonBox.rejected.connect(
                        partial(self.CANCEL, 0))

                    self.selledit.clear()

    @pyqtSlot()
    def sell_stock(self):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        for widget in self.to_be_sold:
            share = widget.stock_symbol.text()
            price = float(widget.stock_price.text())
            list_index = self.shares_list.index(share)

            sell_qt = int(widget.result_sell_quantity.text())
            update = """UPDATE stocks SET quantity = quantity - ? WHERE shares = ? and userid = ?"""
            cur.execute(update, (sell_qt, share, self.uid))

            # log into csv file
            value_sold = price*sell_qt
            if value_sold != 0:
                log_shares(self.uid, share, sell_qt, -value_sold, "SELL")

            # update totalSharesValue
            self.totalSharesValue -= sell_qt*self.stocks_dict[share]
            get = """SELECT quantity FROM stocks WHERE shares = ? and userid = ?"""
            cur.execute(get, (share, self.uid))
            new_qt = cur.fetchone()[0]

            self.remaining_ratio_label.setText("Remaining ratio: 100")
            self.sell_value_label.setText("Sell value: 0/0")
            self.hideRatioLabels()
            self.result_label.hide()

            if new_qt > 0:
                self.quantity_list[list_index] = new_qt
                widget.stock_quantity.setText(str(new_qt))
                widget.hideSellBlockWidget()
                widget.hideResult()

            else:
                delete = """DELETE FROM stocks WHERE shares = ? and userid = ?"""
                cur.execute(delete, (share, self.uid))
                cancel_index = self.to_be_sold.index(widget)
                delete_index = self.shares_widgets.index(widget)

                # UPDATE UI after deletion
                w_prev = self.to_be_sold[self.to_be_sold.index(widget)-1]
                self.CANCEL(cancel_index)
                self.vl.itemAt(delete_index).widget().setParent(None)
                self.shares_widgets.remove(widget)

                del self.shares_list[list_index]
                del self.quantity_list[list_index]
                w_prev.hideSellBlockWidget()
                w_prev.hideResult()
            conn.commit()
        conn.close()

        # Reset checkboxes
        self.to_be_sold.clear()
        for w in self.shares_widgets:
            w.checkBox.setEnabled(True)
            w.checkBox.setChecked(False)

    @pyqtSlot()
    def removeStock(self):
        conn = sqlite3.connect("stock_seller.db")
        cur = conn.cursor()
        for widget in list(self.shares_widgets):
            share = widget.stock_symbol.text()
            remove_qt = int(widget.stock_quantity.text())
            price = float(widget.stock_price.text())
            if widget.checkBox.isChecked() and widget.checkBox.isEnabled():
                delete = """DELETE FROM stocks WHERE shares = ? and userid = ?"""
                cur.execute(delete, (share, self.uid))

                # log csv
                remove_value = remove_qt*price
                log_shares(self.uid, share, remove_qt, remove_value, "REMOVE")

                self.totalSharesValue -= remove_value
                delete_index = self.shares_widgets.index(widget)
                self.vl.itemAt(delete_index).widget().setParent(None)
                self.shares_widgets.remove(widget)

                list_index = self.shares_list.index(share)
                del self.shares_list[list_index]
                del self.quantity_list[list_index]
            conn.commit()
        conn.close()

    # 07.07.22
    @pyqtSlot()
    def OK(self, index):

        if index <= len(self.to_be_sold):
            for widgets in self.shares_widgets:
                widgets.buttonBox.hide()
                widgets.isHidden = True

            w_prev = self.to_be_sold[index-1]
            s_prev = w_prev.horizontalSlider
            w_prev.releaseVal = s_prev.value()

            if index != len(self.to_be_sold):
                widget_i = self.to_be_sold[index]
                slider_i = widget_i.horizontalSlider

                widget_i.buttonBox.accepted.connect(
                    partial(self.OK, index+1), type=Qt.UniqueConnection)
                widget_i.buttonBox.rejected.connect(
                    partial(self.CANCEL, index), type=Qt.UniqueConnection)

                widget_i.showSellBlockWidget()
                self.showRatioLabels()

                list_index = self.shares_list.index(
                    widget_i.stock_symbol.text())

                self.curr_stock_value = float(
                    self.stocks_dict[self.shares_list[list_index]])*int(self.quantity_list[list_index])
                remaining_ratio = self.ratioRemainsCalc(index)
                self.ratio = remaining_ratio if self.curr_stock_value > self.sellVal else (100*self.curr_stock_value/self.sellVal
                                                                                           if remaining_ratio >= 100*self.curr_stock_value/self.sellVal
                                                                                           else remaining_ratio)
                widget_i.initSlider(self.ratio)

                # add onChange event handler
                slider_i.valueChanged.connect(
                    partial(self.sliderOnChange, widget_i))
            else:
                self.to_be_sold[index-1].sell_stock_button.show()
                for widgets in self.to_be_sold:
                    widgets.showResult(self.sellVal)
                    self.result_label.show()

    # 07.07.22
    @pyqtSlot()
    def CANCEL(self, index):
        if index == len(self.to_be_sold) - 1:
            for widget in self.shares_widgets:
                widget.hideResult()
                self.result_label.hide()
        if index >= 0:
            widget_i = self.to_be_sold[index]

            widget_i.resetSlider()
            widget_i.hideSellBlockWidget()
            widget_i.hideResult()
            self.result_label.hide()

            if index != 0:
                self.to_be_sold[index-1].buttonBox.show()
                self.to_be_sold[index-1].isHidden = False
                remains = self.ratioRemainsCalc(index-1)
                self.remaining_ratio_label.setText(
                    "Remaining ratio: " + str(remains))
            else:
                for widget in self.shares_widgets:
                    widget.checkBox.setEnabled(True)
                self.remaining_ratio_label.setText("Remaining ratio: 100")

                self.hideRatioLabels()
                for w in self.to_be_sold:
                    try:
                        w.buttonBox.accepted.disconnect()
                        w.buttonBox.rejected.disconnect()
                    except Exception:
                        pass
                self.to_be_sold.clear()

    @pyqtSlot()
    def allDone(self):

        if self.vl.count() != 0 and self.allDoneClicked == False:
            # add widgets into shares_widgets list
            for i in range(self.vl.count()):
                widget_i = self.vl.itemAt(i).widget()
                widget_i.sell_stock_button.clicked.connect(self.sell_stock)

            self.allDoneClicked = True
            # SHOW SELL BLOCK HEADERS
            self.showSellBlockHeader()

    @pyqtSlot()
    # 07.07 sadeleştirildi
    def sliderOnChange(self, passed_widget):
        if not passed_widget.isHidden:
            slider = passed_widget.horizontalSlider
            ratio = slider.value()
            passed_widget.slider_label.setText(str(ratio))

            index = self.to_be_sold.index(passed_widget)
            if self.remaining_ratio_label.isHidden:
                self.showRatioLabels()
            remains = self.ratioRemainsCalc(index)
            self.remaining_ratio_label.setText(
                "Remaining ratio: " + str(remains))

            self.sell_value_label.setText(
                f"Sell value: {(100-remains)*self.sellVal/100}/{self.sellVal}")

        else:
            passed_widget.horizontalSlider.setValue(passed_widget.releaseVal)

    # 07.07.22
    def ratioRemainsCalc(self, until):
        ret_val = 0
        for i in range(until+1):
            widget_i = self.to_be_sold[i]
            slider_i = widget_i.horizontalSlider
            ret_val += slider_i.value()
        return 100-ret_val

    @pyqtSlot()
    def logOut(self):
        self.return_to_login = True
        self.close()

    def closeEvent(self, event):
        if not self.return_to_login:
            sys.exit()


def log_shares(id, stock_symbol, stock_quantity, value, operation):
    try:
        conn = sqlite3.connect('stock_seller.db')
        cursor = conn.cursor()
        query = "SELECT username FROM users WHERE userid = ?"
        cursor.execute(query, (id,))
        client = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data!")
    finally:
        if conn:
            conn.close()

    with open('log_shares.csv', 'a+', encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        reader = csv.reader(file)
        log_time = datetime.now()

        if os.stat('log_shares.csv').st_size == 0:
            writer.writerow(['Client', 'Time', 'Symbol',
                            'Quantity', 'Operation', 'Value'])
        writer.writerow([client, log_time, stock_symbol,
                        stock_quantity, operation, value])


def hash_pw(pw):
    h = sha256()
    pw = pw.encode("utf-8")
    h.update(pw)
    return h.hexdigest()


def main():
    app = QtWidgets.QApplication(sys.argv)
    #login = Login_screen()
    # login.show()
    # sys.exit(app.exec())
    while True:
        login = Login_screen()
        if login.exec_() == QDialog.Accepted:
            app.exec()


if __name__ == "__main__":
    main()
