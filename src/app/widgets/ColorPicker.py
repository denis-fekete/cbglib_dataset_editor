"""
Module: ColorPicker.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget for picking color.
"""

from PySide6 import QtWidgets


class ColorPicker(QtWidgets.QPushButton):

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.clicked.connect(self.onClick)

    def onClick(self) -> None:
        color = QtWidgets.QColorDialog.getColor(self.color)

        if color.isValid():
            self.color = color

        self.updateBackgroundColor()

    def updateBackgroundColor(self) -> None:
        self.setStyleSheet(f"background-color: {self.color.name()}")
