"""
Module: AutoDetectToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    QWidget that contains GUI elements for automatic detection in DataLabeler.py
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from app.widgets import *


class AutoDetectToolbar(QtWidgets.QWidget):
    autoDetect = Signal()
    openModel = Signal()
    loadModel = Signal()

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(20)

        self.btnAutoDetect = QtWidgets.QPushButton("Detect")
        self.btnAutoDetect.setMaximumWidth(100)
        self.btnAutoDetect.clicked.connect(self.autoDetect)
        self.btnAutoDetect.setEnabled(False)

        self.textEditModelPath = QtWidgets.QLineEdit()

        btnOpenModel = QtWidgets.QPushButton("Open")
        btnOpenModel.setMaximumWidth(100)
        btnOpenModel.clicked.connect(self.openModel)

        btnLoadModel = QtWidgets.QPushButton("Load")
        btnLoadModel.setMaximumWidth(100)
        btnLoadModel.clicked.connect(self.loadModel)

        container = Container(QtWidgets.QHBoxLayout(), maxHeight=20)
        container.addWidgets([QtWidgets.QLabel("Model path:"), self.textEditModelPath])

        self.layout().addWidget(self.btnAutoDetect)
        self.layout().addWidget(container)
        self.layout().addWidget(btnOpenModel)
        self.layout().addWidget(btnLoadModel)
