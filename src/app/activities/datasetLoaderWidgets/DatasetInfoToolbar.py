from PySide6 import QtWidgets

"""
Module: DatasetInfoToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains information about dataset loaded from `data.yaml`, for DatasetLoader.py.
"""

from app.widgets import *
from app.utils import SharedValues


class DatasetInfoToolbar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(300)
        self.setLayout(QtWidgets.QGridLayout())

        spacer = QtWidgets.QWidget()
        spacer.setMinimumHeight(10)

        self.dataPath = QtWidgets.QLineEdit()
        self.trainPath = QtWidgets.QLineEdit()
        self.valPath = QtWidgets.QLineEdit()
        self.testPath = QtWidgets.QLineEdit()
        self.treeView = LabelSelectorTreeView(SharedValues().labelsDict)

        self.layout().addWidget(QtWidgets.QLabel("data.yaml"), 0, 0)
        self.layout().addWidget(spacer, 1, 0)
        self.layout().addWidget(QtWidgets.QLabel("path:"), 2, 0)
        self.layout().addWidget(self.dataPath, 2, 1)
        self.layout().addWidget(QtWidgets.QLabel("train:"), 3, 0)
        self.layout().addWidget(self.trainPath, 3, 1)
        self.layout().addWidget(QtWidgets.QLabel("val:"), 4, 0)
        self.layout().addWidget(self.valPath, 4, 1)
        self.layout().addWidget(QtWidgets.QLabel("test:"), 5, 0)
        self.layout().addWidget(self.testPath, 5, 1)
        self.layout().addWidget(QtWidgets.QLabel("names:"), 6, 0)
        self.layout().addWidget(self.treeView, 7, 0, 1, 2)
