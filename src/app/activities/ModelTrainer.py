"""
Module: ModelTrainer.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for training models.
"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QTextCursor

import os
from pathlib import Path
from datetime import datetime
from typing import Callable

from app.widgets import *
from app.dataset import *
from app.utils import *
from app.training import *

from app.ui.ModelTrainer_ui import Ui_DataTrainerWidget


class ModelTrainer(AbstractTabWidget):
    def __init__(self, setTabsEnabled_fn: Callable[[bool], None]) -> None:
        super().__init__()
        self.ui = Ui_DataTrainerWidget()
        self.ui.setupUi(self)  # type: ignore

        self.pathValidated: bool = False
        self.setTabsEnabled_fn = setTabsEnabled_fn
        self.trainerThread: QtCore.QThread | None = None
        self.currentModelTrainer: AbstractModelTrainer | None = None

        self._connectUI()

    def _connectUI(self) -> None:
        self.currentModelTrainer = None

        self.ui.generateNameButton.clicked.connect(self.generateModelName)
        self.ui.generateOutputDirectoryButton.clicked.connect(self.generateModelPath)
        self.ui.validateButton.clicked.connect(self.validateDataset)
        self.ui.startTrainingButton.clicked.connect(self.startTraining)
        self.ui.datasetPathLineEdit.textChanged.connect(self.datasetPathEdited)

        for i in range(0, len(DATASET_PATHS)):
            self.ui.datasetPathComboBox.addItem(DATASET_PATHS[i])

        self.ui.datasetPathComboBox.currentIndexChanged.connect(
            self.datasetComboBoxChanged
        )

        for i in range(0, len(MODELS_NAMES)):
            self.ui.modelSelectorComboBox.addItem(MODELS_NAMES[i])

    #######################################################
    # Settings
    #######################################################

    @Slot(int)
    def datasetComboBoxChanged(self, index: int) -> None:
        if index == 0:  # dataset export path
            self.ui.datasetPathLineEdit.setText(SharedValues().datasetExportPath)
        elif index == 1:
            self.ui.datasetPathLineEdit.setText(SharedValues().datasetImportPath)

        self.pathValidated = False
        self.ui.startTrainingButton.setEnabled(False)

    @Slot(str)
    def datasetPathEdited(self, text: str) -> None:
        self.pathValidated = False
        self.ui.startTrainingButton.setEnabled(False)

    @Slot()
    def validateDataset(self) -> None:
        self._getCorrectModel(self.ui.modelSelectorComboBox.currentIndex())

        if self.currentModelTrainer is None:
            return

        isValid, message = self.currentModelTrainer.validateDataset(
            self.ui.datasetPathLineEdit.text()
        )

        if not isValid:
            self.ui.startTrainingButton.setEnabled(False)
            QtWidgets.QMessageBox.critical(self, "Dataset is not correct", message)
            return
        else:
            self.ui.startTrainingButton.setEnabled(True)

    @Slot()
    def generateModelName(self) -> None:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        self.ui.modelNameLineEdit.setText(f"project_{timestamp}_ver")

    @Slot()
    def generateModelPath(self) -> None:
        if self.ui.datasetPathLineEdit.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Select 'Dataset path' for generating 'Model output root directory path'",
            )
        else:
            path = Path(os.getcwd()) / "models"
            self.ui.modelOutputPathLineEdit.setText(path.resolve()._str)

    @Slot()
    def startTraining(self) -> None:
        if self.currentModelTrainer is not None:
            self.setTabsEnabled_fn(False)
            self.ui.modelSettingsWidget.setEnabled(False)

            self.currentModelTrainer.epochs = self.ui.epochsSpinBox.value()
            self.currentModelTrainer.workers = self.ui.workersSpinBox.value()
            self.currentModelTrainer.batch = self.ui.batchSpinBox.value()
            self.currentModelTrainer.modelPath = self.ui.modelOutputPathLineEdit.text()
            self.currentModelTrainer.modelName = self.ui.modelNameLineEdit.text()

            if self.trainerThread is None:
                self.trainerThread = QtCore.QThread()

            if not self.currentModelTrainer.connectedToThread:
                self.currentModelTrainer.moveToThread(self.trainerThread)

                self.trainerThread.started.connect(self.currentModelTrainer.run)

                self.currentModelTrainer.progress.connect(
                    self.ui.trainingProgressBar.setValue
                )
                self.currentModelTrainer.status.connect(self.statusTextChanged)
                self.currentModelTrainer.error.connect(self.showError)
                self.currentModelTrainer.errorExit.connect(self.errorExit)

                self.currentModelTrainer.finished.connect(self.trainingEnded)
                self.currentModelTrainer.connectedToThread = True

            self.ui.logOutputTextEdit.clear()
            self.trainerThread.start()
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Model trainer not selected",
                "Model trainer is not selected or not supported. "
                "Training will not start",
            )

    #######################################################
    # Training
    #######################################################

    @Slot()
    def trainingEnded(self) -> None:
        """_summary_"""
        self.setTabsEnabled_fn(True)
        self.ui.modelSettingsWidget.setEnabled(True)

    @Slot()
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
    def statusTextChanged(self, text: str) -> None:
        self.ui.logOutputTextEdit.setPlainText(
            self.ui.logOutputTextEdit.toPlainText() + "\n" + text
        )
        self.ui.outputLogLabel.moveCursor(QTextCursor.End)  # type: ignore

    def showError(self, text: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Training error", text)

    def errorExit(self, text: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Error occurred during training", text)
        self.trainingEnded()

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.training
        self.ui.modelSelectorComboBox.setCurrentIndex(settings.model)

        self.ui.batchSpinBox.setValue(settings.batchSize)
        self.ui.workersSpinBox.setValue(settings.numberOfWorkers)
        self.ui.epochsSpinBox.setValue(settings.numberOfEpochs)

        self.ui.modelOutputPathLineEdit.setText(settings.modelOutputPath)
        self.ui.modelNameLineEdit.setText(settings.modelName)

    def updateSettings(self):
        settings = SharedValues().settings.training
        settings.model = self.ui.modelSelectorComboBox.currentIndex()

        settings.batchSize = self.ui.batchSpinBox.value()
        settings.numberOfWorkers = self.ui.workersSpinBox.value()
        settings.numberOfEpochs = self.ui.epochsSpinBox.value()

        settings.modelOutputPath = self.ui.modelOutputPathLineEdit.text()
        settings.modelName = self.ui.modelNameLineEdit.text()

    #######################################################
    # Other
    #######################################################

    def _getCorrectModel(self, index: int):
        if index == YOLO_V8_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV8n()
        elif index == YOLO_V8_M_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV8m()
        elif index == YOLO_V11_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV11n()
        elif index == YOLO_V11_M_MODEL_INDEX:
            self.currentModelTrainer = None
        elif index == YOLO_V26_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV26n()
        elif index == FASTER_RCNN_MODEL_INDEX:
            self.currentModelTrainer = None

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        pass
