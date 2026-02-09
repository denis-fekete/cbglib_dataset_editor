"""
Module: ColorPicker.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget for picking color.
"""

from PySide6 import QtWidgets
from PySide6.QtGui import QColor

from typing import Callable


class ColorPicker(QtWidgets.QPushButton):
    def __init__(
        self, defaultColor: QColor, callback_fn: Callable[[], None] | None = None
    ) -> None:
        super().__init__()

        self.clicked.connect(self.onClicked_slot)
        self.color = defaultColor
        self.callback_fn = callback_fn
        self.updateBackgroundColor()

    def onClicked_slot(self) -> None:
        color = QtWidgets.QColorDialog.getColor(self.color)

        if color.isValid():
            self.color = color

        self.updateBackgroundColor()

        if self.callback_fn is not None:
            self.callback_fn()

    def updateBackgroundColor(self) -> None:
        self.setStyleSheet(f"background-color: {self.color.name()}")
