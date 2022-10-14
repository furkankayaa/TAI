from PyQt5 import uic

with open("temp_ui.py","w", encoding="utf-8") as fout:
    uic.compileUi("list_item.ui", fout)