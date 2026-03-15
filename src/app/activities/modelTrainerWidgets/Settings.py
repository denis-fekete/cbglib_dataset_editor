"""
Module: Settings.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains elements for model training, for ModelTrainer.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy

from app.widgets import *
from .values import *


class Settings(QtWidgets.QWidget):
    generateModelPath = Signal()
    generateModelName = Signal()
    datasetPathEdited = Signal(str)
    datasetPathChanged = Signal(int)
    validateDataset = Signal()
    startTraining = Signal()

    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QGridLayout())

        self.settingsLabel = QtWidgets.QLabel("Settings:")

        self.workerSpinBox = QtWidgets.QSpinBox()
        self.workerSpinBox.setValue(0)
        self.workerSpinBox.setMinimum(0)
        self.workerSpinBox.setMaximum(99999)

        self.epochsSpinBox = QtWidgets.QSpinBox()
        self.epochsSpinBox.setValue(20)
        self.epochsSpinBox.setMinimum(0)
        self.epochsSpinBox.setMaximum(99999)

        self.batchSpinBox = QtWidgets.QSpinBox()
        self.batchSpinBox.setValue(4)
        self.batchSpinBox.setMinimum(0)
        self.batchSpinBox.setMaximum(99999)

        self.modelPathTextEdit = QtWidgets.QLineEdit()
        generateModelPathBtn = QtWidgets.QPushButton("Generate")
        generateModelPathBtn.clicked.connect(self.generateModelPath)

        self.modelNameTextEdit = QtWidgets.QLineEdit()
        modelNameGenerateBtn = QtWidgets.QPushButton("Generate")
        modelNameGenerateBtn.clicked.connect(self.generateModelName)

        labelDatasetPath = QtWidgets.QLabel("Dataset path:")
        labelDatasetPath.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.datasetPathTextEdit = QtWidgets.QLineEdit()
        self.datasetPathTextEdit.textChanged.connect(self.datasetPathEdited)

        validateDatasetBtn = QtWidgets.QPushButton("Validate")
        validateDatasetBtn.clicked.connect(self.validateDataset)

        self.startTrainingBtn = QtWidgets.QPushButton("Start training")
        self.startTrainingBtn.clicked.connect(self.startTraining)

        self.datasetPathSelector = QtWidgets.QComboBox()
        self.datasetPathSelector.addItem(DATASET_PATHS[0])
        self.datasetPathSelector.addItem(DATASET_PATHS[1])
        self.datasetPathSelector.currentIndexChanged.connect(self.datasetPathChanged)
        self.datasetPathChanged.emit(0)

        subSettingsContainer = QtWidgets.QWidget()
        subSettingsContainer.setLayout(QtWidgets.QGridLayout())
        subSettingsContainer.layout().addWidget(self.settingsLabel, 0, 0)
        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Number of additional workers (0 = single worker):"), 1, 0
        )
        subSettingsContainer.layout().addWidget(self.workerSpinBox, 1, 1, 1, 2)

        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Number of epochs (training runs):"), 2, 0
        )
        subSettingsContainer.layout().addWidget(self.epochsSpinBox, 2, 1, 1, 2)
        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Batch size:"), 3, 0)
        subSettingsContainer.layout().addWidget(self.batchSpinBox, 3, 1, 1, 2)

        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Model output path:"), 4, 0
        )
        subSettingsContainer.layout().addWidget(generateModelPathBtn, 4, 1)
        subSettingsContainer.layout().addWidget(self.modelPathTextEdit, 4, 2, 1, 2)

        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Model name:"), 5, 0)
        subSettingsContainer.layout().addWidget(modelNameGenerateBtn, 5, 1)
        subSettingsContainer.layout().addWidget(self.modelNameTextEdit, 5, 2, 1, 2)

        self.layout().addWidget(subSettingsContainer, 0, 0, 1, 2)
        self.layout().addWidget(labelDatasetPath, 1, 0)
        self.layout().addWidget(self.datasetPathSelector, 1, 1)

        self.layout().addWidget(self.datasetPathTextEdit, 2, 0, 1, 2)
        self.layout().addWidget(validateDatasetBtn, 3, 0)
        self.layout().addWidget(self.startTrainingBtn, 3, 1)
