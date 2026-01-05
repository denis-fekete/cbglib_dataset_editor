from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QTextCursor

import os
from pathlib import Path
from datetime import datetime
from typing import Callable

from app.widgets import *
from app.image_manipulation import *
from app.utils import *
from app.data_classes import *
from app.model_training import *
from .AbstractTabWidget import AbstractTabWidget


class ModelTrainer(AbstractTabWidget):
    def __init__(self, setTabsEnabled_fn: Callable[[bool], None]) -> None:
        super().__init__()
        self.pathValidated: bool = False
        self.setTabsEnabled_fn = setTabsEnabled_fn
        self.trainerThread: QtCore.QThread | None = None
        self.currentModelTrainer: YoloUltralyticsTrainer | None = None
        self._initUI()

    YOLO_V8_MODEL_INDEX = 0
    YOLO_V11_MODEL_INDEX = 1
    FASTER_RCNN_MODEL_INDEX = 2
    MODELS = {
        0: "Yolo V8 (Ultralytics)",
        1: "Yolo V11 (Ultralytics)",
        2: "Faster RCNN",
    }

    DATASET_PATHS = {
        0: "Dataset export path",
        1: "Dataset import path",
    }

    def _initUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self.currentModelTrainer = None

        self._initModelSelectorContainer()
        self._initSettingsContainer()
        self._initProgressContainer()

        self.layout().addWidget(self._modelSelectorContainer, 0, 0)
        self.layout().addWidget(self._settingsContainer, 1, 0)
        self.layout().addWidget(self._progressContainer, 2, 0)

    def _initModelSelectorContainer(self) -> None:
        self._modelSelectorContainer = QtWidgets.QWidget()
        self._modelSelectorContainer.setLayout(QtWidgets.QGridLayout())

        self.modelSelector = QtWidgets.QComboBox()
        for i in range(0, len(self.MODELS)):
            self.modelSelector.addItem(self.MODELS[i])

        self.modelSelector.currentIndexChanged.connect(self.modelChanged_slot)

        self._modelSelectorContainer.layout().addWidget(
            QtWidgets.QLabel("Model selection:"), 0, 0
        )
        self._modelSelectorContainer.layout().addWidget(self.modelSelector, 1, 0)

    def _initSettingsContainer(self) -> None:
        self._settingsContainer = QtWidgets.QWidget()
        self._settingsContainer.setLayout(QtWidgets.QGridLayout())

        self._settingsLabel = QtWidgets.QLabel("Settings:")

        self._workerSpinBox = QtWidgets.QSpinBox()
        self._workerSpinBox.setValue(0)
        self._workerSpinBox.setMinimum(0)
        self._workerSpinBox.setMaximum(99999)

        self._epochsSpinBox = QtWidgets.QSpinBox()
        self._epochsSpinBox.setValue(20)
        self._epochsSpinBox.setMinimum(0)
        self._epochsSpinBox.setMaximum(99999)

        self._batchSpinBox = QtWidgets.QSpinBox()
        self._batchSpinBox.setValue(4)
        self._batchSpinBox.setMinimum(0)
        self._batchSpinBox.setMaximum(99999)

        self._modelPathTextEdit = QtWidgets.QLineEdit()
        self._modelPathGenerateBtn = QtWidgets.QPushButton("Generate")
        self._modelPathGenerateBtn.clicked.connect(self.generateModelPath)

        self._modelNameTextEdit = QtWidgets.QLineEdit()
        self._modelNameGenerateBtn = QtWidgets.QPushButton("Generate")
        self._modelNameGenerateBtn.clicked.connect(self.generateModelName)

        labelDatasetPath = QtWidgets.QLabel("Dataset path")
        labelDatasetPath.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self._datasetPathTextEdit = QtWidgets.QLineEdit()
        self._datasetPathTextEdit.textChanged.connect(
            self._datasetPathTextEditChanged_slot
        )

        self._btnValidateDataset = QtWidgets.QPushButton("Validate")
        self._btnValidateDataset.clicked.connect(self.validateDataset)

        self._btnStartTraining = QtWidgets.QPushButton("Start training")
        self._btnStartTraining.clicked.connect(self.startTraining)

        self._datasetPathSelector = QtWidgets.QComboBox()
        self._datasetPathSelector.addItem(self.DATASET_PATHS[0])
        self._datasetPathSelector.addItem(self.DATASET_PATHS[1])
        self._datasetPathSelector.currentIndexChanged.connect(
            self.datasetPathChanged_slot
        )
        self.datasetPathChanged_slot(0)

        subSettingsContainer = QtWidgets.QWidget()
        subSettingsContainer.setLayout(QtWidgets.QGridLayout())
        subSettingsContainer.layout().addWidget(self._settingsLabel, 0, 0)
        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Number of workers (0 = single worker):"), 1, 0
        )
        subSettingsContainer.layout().addWidget(self._workerSpinBox, 1, 1, 1, 2)

        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Number of epochs (training runs):"), 2, 0
        )
        subSettingsContainer.layout().addWidget(self._epochsSpinBox, 2, 1, 1, 2)
        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Batch size:"), 3, 0)
        subSettingsContainer.layout().addWidget(self._batchSpinBox, 3, 1, 1, 2)

        subSettingsContainer.layout().addWidget(
            QtWidgets.QLabel("Model output path:"), 4, 0
        )
        subSettingsContainer.layout().addWidget(self._modelPathGenerateBtn, 4, 1)
        subSettingsContainer.layout().addWidget(self._modelPathTextEdit, 4, 2, 1, 2)

        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Model name:"), 5, 0)
        subSettingsContainer.layout().addWidget(self._modelNameGenerateBtn, 5, 1)
        subSettingsContainer.layout().addWidget(self._modelNameTextEdit, 5, 2, 1, 2)

        self._settingsContainer.layout().addWidget(subSettingsContainer, 0, 0, 1, 2)
        self._settingsContainer.layout().addWidget(labelDatasetPath, 1, 0)
        self._settingsContainer.layout().addWidget(self._datasetPathSelector, 1, 1)

        self._settingsContainer.layout().addWidget(
            self._datasetPathTextEdit, 2, 0, 1, 2
        )
        self._settingsContainer.layout().addWidget(self._btnValidateDataset, 3, 0)
        self._settingsContainer.layout().addWidget(self._btnStartTraining, 3, 1)

    def _initProgressContainer(self) -> None:
        self._progressContainer = QtWidgets.QWidget()
        self._progressContainer.setLayout(QtWidgets.QGridLayout())

        self._statusTextEdit = QtWidgets.QTextEdit()
        self._statusTextEdit.setReadOnly(True)

        self._progressBar = QtWidgets.QProgressBar()
        self._progressBar.setMaximum(100)

        self._progressContainer.layout().addWidget(self._statusTextEdit, 0, 0)
        self._progressContainer.layout().addWidget(self._progressBar, 1, 0)

    @Slot(int)
    def modelChanged_slot(self, index: int) -> None:
        self._settingsLabel.setText(f"Settings for {self.MODELS[index]}:")

    @Slot(int)
    def datasetPathChanged_slot(self, index: int) -> None:
        if index == 0:  # dataset export path
            self._datasetPathTextEdit.setText(SharedValues().datasetExportPath)
        elif index == 1:
            self._datasetPathTextEdit.setText(SharedValues().datasetImportPath)

        self.pathValidated = False
        self._btnStartTraining.setEnabled(False)

    @Slot(str)
    def _datasetPathTextEditChanged_slot(self, text: str) -> None:
        self.pathValidated = False
        self._btnStartTraining.setEnabled(False)

    def validateDataset(self) -> None:
        if self.modelSelector.currentIndex() == self.YOLO_V8_MODEL_INDEX:
            if self.currentModelTrainer is None:
                self.currentModelTrainer = YoloUltralyticsTrainer()

            isValid, message = self.currentModelTrainer.validateDataset(
                self._datasetPathTextEdit.text()
            )

            if not isValid:
                self._btnStartTraining.setEnabled(False)
                QtWidgets.QMessageBox.critical(self, "Dataset is not correct", message)
                return
            else:
                self._btnStartTraining.setEnabled(True)

    def generateModelName(self) -> None:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        self._modelNameTextEdit.setText(f"project_{timestamp}_ver")

    def generateModelPath(self) -> None:
        if self._datasetPathTextEdit.text() == "":
            QtWidgets.QMessageBox.warning(
                self, "Select dataset path for generating model output path"
            )
        else:
            path = Path(os.getcwd()) / "models"
            self._modelPathTextEdit.setText(path.resolve()._str)

    def startTraining(self) -> None:
        if self.currentModelTrainer is not None:
            self.setTabsEnabled_fn(False)
            self._modelSelectorContainer.setEnabled(False)
            self._settingsContainer.setEnabled(False)

            self.currentModelTrainer.epochs = self._epochsSpinBox.value()
            self.currentModelTrainer.workers = self._workerSpinBox.value()
            self.currentModelTrainer.batch = self._batchSpinBox.value()
            self.currentModelTrainer.modelPath = self._modelPathTextEdit.text()
            self.currentModelTrainer.modelName = self._modelNameTextEdit.text()

            if self.trainerThread is None:
                self.trainerThread = QtCore.QThread()

            if not self.currentModelTrainer.connectedToThread:
                self.currentModelTrainer.moveToThread(self.trainerThread)

                self.trainerThread.started.connect(self.currentModelTrainer.run)

                self.currentModelTrainer.progress.connect(self._progressBar.setValue)
                self.currentModelTrainer.status.connect(self._statusText_slot)
                self.currentModelTrainer.error.connect(self._showError_slot)
                self.currentModelTrainer.errorExit.connect(self._errorExit_slot)

                self.currentModelTrainer.finished.connect(self._trainingEnded_slot)
                self.currentModelTrainer.connectedToThread = True

            self._statusTextEdit.clear()
            self.trainerThread.start()
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Model trainer not selected",
                "Model trainer is not selected or not supported. "
                "Training will not start",
            )

    def _trainingEnded_slot(self) -> None:
        """_summary_"""
        self.setTabsEnabled_fn(True)
        self._modelSelectorContainer.setEnabled(True)
        self._settingsContainer.setEnabled(True)

    def destroyTrainers(self) -> None:
        if self.trainerThread is None:
            return

        if self.trainerThread.isRunning():
            self.trainerThread.quit()
            self.trainerThread.wait()

        if self.currentModelTrainer is not None:
            self.currentModelTrainer.deleteLater()
            self.currentModelTrainer = None

        self.trainerThread.deleteLater()
        self.trainerThread = None

    @Slot(str)
    def _statusText_slot(self, text: str) -> None:
        self._statusTextEdit.setPlainText(
            self._statusTextEdit.toPlainText() + "\n" + text
        )
        self._statusTextEdit.moveCursor(QTextCursor.End)  # type: ignore

    def _showError_slot(self, text: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Training error", text)

    def _errorExit_slot(self, text: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Error occurred during training", text)
        self._trainingEnded_slot()

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        pass
