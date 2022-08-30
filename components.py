from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import sys

####################################################################

class List_item(QWidget):
    def __init__(self):
        super(List_item, self).__init__()
        self.item_id = -1
        self.isHidden = True
        self.releaseVal = 0

        self.resize(733, 78	)
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 711, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.stock_symbol = QLabel(self.horizontalLayoutWidget)
        self.stock_symbol.setObjectName(u"stock_symbol")
        self.horizontalLayout.addWidget(self.stock_symbol)

        self.stock_price = QLabel(self.horizontalLayoutWidget)
        self.stock_price.setObjectName(u"stock_price")
        self.horizontalLayout.addWidget(self.stock_price)

        self.stock_quantity = QLabel(self.horizontalLayoutWidget)
        self.stock_quantity.setObjectName(u"stock_quantity")
        self.horizontalLayout.addWidget(self.stock_quantity)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setMaximumSize(QSize(16777215, 50))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)

        # !!!!!!! bu olmazsa list item olarak gözükmüyor
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        ##

        self.horizontalSlider = QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximumSize(QSize(450, 16777215))

        self.slider_label = QLabel(self.horizontalLayoutWidget)
        self.slider_label.setMaximumSize(QSize(45, 16777215))
        self.slider_label.setObjectName("slider_label")
        self.horizontalLayout.addWidget(self.slider_label)

        self.max_label = QLabel(self.horizontalLayoutWidget)
        self.max_label.setMaximumSize(QSize(45, 16777215))
        self.max_label.setObjectName("max_label")
        self.horizontalLayout.addWidget(self.max_label)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.buttonBox = QDialogButtonBox(self.horizontalLayoutWidget)
        self.buttonBox.setMaximumSize(QSize(125, 16777215))
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.line_2 = QFrame(self.horizontalLayoutWidget)
        self.line_2.setMaximumSize(QSize(16777215, 50))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)

        self.result_sell_quantity = QLabel(self.horizontalLayoutWidget)
        self.result_sell_quantity.setObjectName(u"result_sell_quantity")
        self.horizontalLayout.addWidget(self.result_sell_quantity)
         #####Qt designerda düzenle
        self.sell_stock_button = QPushButton(self.horizontalLayoutWidget)
        self.sell_stock_button.setMaximumSize(QSize(50,50))
        self.sell_stock_button.setText("SELL")
        self.horizontalLayout.addWidget(self.sell_stock_button)
        self.sell_stock_button.hide()    
        ######
        self.hideSellBlockWidget()
        self.hideResult()

        self.stock_symbol.setText(u"Symbol")
        self.stock_price.setText(u"Price")
        self.stock_quantity.setText(u"Quantity")
        self.result_sell_quantity.setText(u"Sell")

    def initSlider(self, ratio):
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(ratio)
        self.slider_label.setText(str(self.horizontalSlider.value()))
        self.max_label.setText(str(ratio))

    def resetSlider(self):
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(0)
        self.slider_label.setText(str(self.horizontalSlider.value()))
        self.max_label.setText(str(0))

    def showSellBlockWidget(self):
        self.slider_label.show()
        self.horizontalSlider.show()
        self.max_label.show()
        self.buttonBox.show()
        self.isHidden = False
        self.line.show()

    def hideSellBlockWidget(self):
        self.slider_label.hide()
        self.horizontalSlider.hide()
        self.max_label.hide()
        self.buttonBox.hide()
        self.isHidden = True
        self.line.hide()

    def hideResult(self):
        self.result_sell_quantity.setText("")
        self.result_sell_quantity.hide()
        self.line_2.hide()
        self.sell_stock_button.hide()

    def showResult(self,sell):
        ratio = self.releaseVal/100
        show = sell*ratio/float(self.stock_price.text())
        result = str(round(show))
        self.result_sell_quantity.setText(result)
        self.result_sell_quantity.show()
        self.line_2.show()
#####################

class sell_widget(QWidget):
    def __init__(self,parent):
        super(sell_widget, self).__init__()
        loadUi("sell_widget.ui", self)
        self.sell_button.clicked.connect(self.sell)

    def sell(self):
        print("Sold")

def main():
    app = QApplication(sys.argv)
    mw = List_item()
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
