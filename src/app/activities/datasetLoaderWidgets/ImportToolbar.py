"""
Module: ImportToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains import parts for DatasetLoader.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy

from app.widgets import *
from app.utils import SharedValues


class ImportToolbar(QtWidgets.QWidget):
    importPathChanged = Signal(str)
    importDialog = Signal()

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QGridLayout())
        importPathLabel = QtWidgets.QLabel(
            "Path to import dataset from (subdirectories will be imported as well)"
        )
        importPathLabel.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.importPathTextEdit = QtWidgets.QLineEdit()
        self.importPathTextEdit.textChanged.connect(self.importPathChanged)

        self.btnImportDialog = QtWidgets.QPushButton("Import")
        self.btnImportDialog.clicked.connect(self.importDialog)

        self.treeView = ImageSampleTreeView(SharedValues().imageSamples)

        self.layout().addWidget(importPathLabel, 0, 0, 1, 2)
        self.layout().addWidget(self.importPathTextEdit, 1, 0)
        self.layout().addWidget(self.btnImportDialog, 1, 1)
        self.layout().addWidget(self.treeView, 2, 0, 1, 2)
