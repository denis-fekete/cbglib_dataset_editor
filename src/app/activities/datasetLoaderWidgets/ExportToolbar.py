"""
Module: ExportToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    QWidget that contains export part of GUI for DatasetLoader.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy

from app.widgets import *


class ExportToolbar(QtWidgets.QWidget):
    exportPathChanged = Signal(str)
    exportDialog = Signal()
    exportClicked = Signal()

    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QGridLayout())
        exportPathLabel = QtWidgets.QLabel("Path to export dataset to")
        exportPathLabel.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.exportPathTextEdit = QtWidgets.QLineEdit()
        self.exportPathTextEdit.textChanged.connect(self.exportPathChanged)

        btnExportDialog = QtWidgets.QPushButton("Open")
        btnExportDialog.clicked.connect(self.exportDialog)

        self.btnExport = QtWidgets.QPushButton("Start Export")
        self.btnExport.clicked.connect(self.exportClicked)

        self.applyFiltersCheckBox = QtWidgets.QCheckBox("Apply filters")
        self.applyFiltersCheckBox.setChecked(True)

        self.generateNameCheckBox = QtWidgets.QCheckBox("Generate name from class")
        self.generateNameCheckBox.setChecked(True)

        self.trainDataPercentageSpinBox = QtWidgets.QSpinBox(prefix="Train data %:")
        self.trainDataPercentageSpinBox.setMinimum(0)
        self.trainDataPercentageSpinBox.setMaximum(100)
        self.trainDataPercentageSpinBox.setValue(100)

        self.separateByClassesCheckBox = QtWidgets.QCheckBox(
            "Separate classes into subdirectories"
        )
        self.separateByClassesCheckBox.setChecked(True)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setEnabled(False)

        self.layout().addWidget(exportPathLabel, 0, 0, 1, 2)
        self.layout().addWidget(self.exportPathTextEdit, 1, 0)
        self.layout().addWidget(btnExportDialog, 1, 1)
        self.layout().addWidget(self.trainDataPercentageSpinBox, 2, 0)
        self.layout().addWidget(self.generateNameCheckBox, 2, 1)
        self.layout().addWidget(self.separateByClassesCheckBox, 2, 2)
        self.layout().addWidget(self.applyFiltersCheckBox, 2, 3)
        self.layout().addWidget(self.btnExport, 3, 0)
        self.layout().addWidget(QtWidgets.QLabel("Export progress:"), 4, 0)
        self.layout().addWidget(self.progressBar, 5, 0, 1, 2)
