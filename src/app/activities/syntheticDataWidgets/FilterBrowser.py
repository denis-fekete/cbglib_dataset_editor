"""
Module: ModelSelector.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains elements QTreeView for browsing filter presets SyntheticDataCreator.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtWidgets import QSizePolicy

from app.synthetic.FilterPresetTreeView import FilterPresetTreeView
from app.utils import *


class FilterBrowser(QtWidgets.QWidget):
    filterSelected = Signal(QModelIndex)
    filterChanged = Signal(QModelIndex, QModelIndex)
    newFilter = Signal()
    deleteFilter = Signal()

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QGridLayout())
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.selector = FilterPresetTreeView(SharedValues().filterPresets)
        self.selector.clicked.connect(self.filterSelected)
        self.selector.model.dataChanged.connect(self.filterChanged)

        newLabelBtn = QtWidgets.QPushButton("New")
        newLabelBtn.clicked.connect(self.newFilter)

        deleteLabelBtn = QtWidgets.QPushButton("Delete")
        deleteLabelBtn.clicked.connect(self.deleteFilter)

        self.layout().addWidget(QtWidgets.QLabel("Filters:"), 0, 0)
        self.layout().addWidget(newLabelBtn, 1, 0)
        self.layout().addWidget(deleteLabelBtn, 1, 1)
        self.layout().addWidget(self.selector, 2, 0, 1, 2)
