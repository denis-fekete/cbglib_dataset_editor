from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy

class Container(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout):
        super().__init__()

        self.setLayout(layout)

    def addWidgets(self, widgetList):
        for widget in widgetList:
            self.layout().addWidget(widget)