"""
Module: ImageLabelBoxToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    QWidget that contains GUI elements creating, deleting and editing ImageLabelBox items, for
    DataLabeler.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QMargins
from PySide6.QtGui import QColor

from app.widgets import *


class ImageLabelBoxToolbar(QtWidgets.QWidget):
    new = Signal()
    delete = Signal()
    updateColors = Signal()

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 100, 0)
        self.setMaximumHeight(25)

        btnNewLabel = QtWidgets.QPushButton("New label")
        btnNewLabel.setMaximumWidth(100)
        btnNewLabel.clicked.connect(self.new)

        btnDeleteLabel = QtWidgets.QPushButton("Delete label")
        btnDeleteLabel.setMaximumWidth(100)
        btnDeleteLabel.clicked.connect(self.delete)

        self.selectedColorPicker = ColorPicker(
            QColor(160, 255, 160), self.updateColorsCallback
        )
        self.selectedColorPicker.setMaximumWidth(50)

        self.defaultColorPicker = ColorPicker(
            QColor(10, 10, 10), self.updateColorsCallback
        )
        self.defaultColorPicker.setMaximumWidth(50)

        containerNew = Container(QtWidgets.QHBoxLayout(), margins=QMargins(0, 0, 20, 0))
        containerNew.addWidgets([btnNewLabel, QtWidgets.QLabel("(Ctrl+W)")])

        containerDelete = Container(
            QtWidgets.QHBoxLayout(), margins=QMargins(0, 0, 20, 0)
        )
        containerDelete.addWidgets([btnDeleteLabel, QtWidgets.QLabel("(Del)")])

        containerColorPickers = Container(
            QtWidgets.QHBoxLayout(), margins=QMargins(0, 0, 20, 0)
        )
        containerDelete.addWidgets([self.selectedColorPicker, self.defaultColorPicker])

        self.layout().addWidget(containerNew)
        self.layout().addWidget(containerDelete)
        self.layout().addWidget(containerColorPickers)

    def updateColorsCallback(self):
        self.updateColors.emit()
