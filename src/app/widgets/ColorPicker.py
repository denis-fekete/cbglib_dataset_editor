"""
Module: ColorPicker.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget for picking color, this UI element appears as a button, upon clicking on, an color picker
    dialog will be opened. Retrieve value by using public `color`.
"""

from PySide6 import QtWidgets
from PySide6.QtGui import QColor


class ColorPicker(QtWidgets.QPushButton):

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.clicked.connect(self.onClick)
        self.color = QColor(0, 0, 0)

    def onClick(self) -> None:
        color = QtWidgets.QColorDialog.getColor(self.color)

        if color.isValid():
            self.color = color

        self.updateBackgroundColor()

    def updateBackgroundColor(self) -> None:
        self.setStyleSheet(f"background-color: {self.color.name()}")
