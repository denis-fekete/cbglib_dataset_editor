"""
Module: ModelSelector.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains elements showing output of the model, for ModelSelector.py.
"""

from PySide6 import QtWidgets

from app.widgets import *
from .values import *


class ModelOutput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QGridLayout())

        self.statusTextEdit = QtWidgets.QTextEdit()
        self.statusTextEdit.setReadOnly(True)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setMaximum(100)

        self.layout().addWidget(self.statusTextEdit, 0, 0)
        self.layout().addWidget(self.progressBar, 1, 0)
