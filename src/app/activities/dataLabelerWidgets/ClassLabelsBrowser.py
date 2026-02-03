"""
Module: ClassLabelBrowser.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    QWidget that contains GUI elements for labels browsing and editing, for DataLabeler.py
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import QModelIndex

from app.utils import SharedValues
from app.widgets import *


class ClassLabelsBrowser(QtWidgets.QWidget):
    new = Signal()
    delete = Signal()
    labelsChanged = Signal(QModelIndex)
    dataEdited = Signal(QModelIndex, QModelIndex, list)

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setSpacing(0)
        self.setMaximumWidth(300)

        self.treeView = LabelSelectorTreeView(SharedValues().labelsDict)
        self.treeView.setMaximumWidth(280)
        self.treeView.clicked.connect(self.labelsChanged)
        self.treeView.model.dataChanged.connect(self._onModelDataChanged)

        self._btnNewLabel = QtWidgets.QPushButton("New")
        self._btnNewLabel.clicked.connect(self.new)

        self._btnDeleteLabel = QtWidgets.QPushButton("Delete")
        self._btnDeleteLabel.clicked.connect(self.delete)

        self.layout().addWidget(QtWidgets.QLabel("Labels:"), 0, 0)
        self.layout().addWidget(self._btnNewLabel, 1, 0)
        self.layout().addWidget(self._btnDeleteLabel, 1, 1)
        self.layout().addWidget(self.treeView, 2, 0, 1, 2)

    @Slot(QModelIndex, QModelIndex, list)
    def _onModelDataChanged(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]
    ):
        # WORK-AROUND : on compilation time QList cannot be converted to python list
        self.dataEdited.emit(topLeft, bottomRight, roles)
