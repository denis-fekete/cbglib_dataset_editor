"""
Module: ModelSelector.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains elements for model selection, for ModelTrainer.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from app.widgets import *
from .values import *


class ModelSelector(QtWidgets.QWidget):
    modelChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QGridLayout())

        self.selector = QtWidgets.QComboBox()
        for i in range(0, len(MODELS_NAMES)):
            self.selector.addItem(MODELS_NAMES[i])

        self.selector.currentIndexChanged.connect(self.modelChanged)

        self.layout().addWidget(QtWidgets.QLabel("Model selection:"), 0, 0)
        self.layout().addWidget(self.selector, 1, 0)
