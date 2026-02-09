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
from .modelTrainerWidgets.Settings import Settings
from .modelTrainerWidgets.ModelSelector import ModelSelector
from .modelTrainerWidgets.ModelOutput import ModelOutput
from .modelTrainerWidgets.values import *


class ModelTrainer(AbstractTabWidget):
    def __init__(self, setTabsEnabled_fn: Callable[[bool], None]) -> None:
        super().__init__()
        self.pathValidated: bool = False
        self.setTabsEnabled_fn = setTabsEnabled_fn
        self.trainerThread: QtCore.QThread | None = None
        self.currentModelTrainer: YoloUltralyticsTrainer | None = None
        self._initUI()

    def _initUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self.currentModelTrainer = None

        self.modelSelector = ModelSelector()
        self.modelSelector.modelChanged.connect(self.modelChanged)

        self.settings = Settings()
        self.settings.generateModelPath.connect(self.generateModelPath)
        self.settings.generateModelName.connect(self.generateModelName)
        self.settings.datasetPathEdited.connect(self.datasetPathEdited)
        self.settings.datasetPathChanged.connect(self.datasetPathChanged)
        self.settings.validateDataset.connect(self.validateDataset)
        self.settings.startTraining.connect(self.startTraining)

        self.modelOutput = ModelOutput()

        self.layout().addWidget(self.modelSelector, 0, 0)
        self.layout().addWidget(self.settings, 1, 0)
        self.layout().addWidget(self.modelOutput, 2, 0)

    #######################################################
    # Settings
    #######################################################

    @Slot(int)
    def datasetPathChanged(self, index: int) -> None:
        if index == 0:  # dataset export path
            self.settings.datasetPathTextEdit.setText(SharedValues().datasetExportPath)
        elif index == 1:
            self.settings.datasetPathTextEdit.setText(SharedValues().datasetImportPath)

        self.pathValidated = False
        self.settings.startTrainingBtn.setEnabled(False)

    @Slot(str)
    def datasetPathEdited(self, text: str) -> None:
        self.pathValidated = False
        self.settings.startTrainingBtn.setEnabled(False)

    @Slot()
    def validateDataset(self) -> None:
        if self.modelSelector.selector.currentIndex() == YOLO_V8_MODEL_INDEX:
            if self.currentModelTrainer is None:
                self.currentModelTrainer = YoloUltralyticsTrainer()

            isValid, message = self.currentModelTrainer.validateDataset(
                self.settings.datasetPathTextEdit.text()
            )

            if not isValid:
                self.settings.startTrainingBtn.setEnabled(False)
                QtWidgets.QMessageBox.critical(self, "Dataset is not correct", message)
                return
            else:
                self.settings.startTrainingBtn.setEnabled(True)

    @Slot()
    def generateModelName(self) -> None:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        self.settings.modelNameTextEdit.setText(f"project_{timestamp}_ver")

    @Slot()
    def generateModelPath(self) -> None:
        if self.settings.datasetPathTextEdit.text() == "":
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Select dataset path for generating model output path"
            )
        else:
            path = Path(os.getcwd()) / "models"
            self.settings.modelPathTextEdit.setText(path.resolve()._str)

    @Slot()
    def startTraining(self) -> None:
        if self.currentModelTrainer is not None:
            self.setTabsEnabled_fn(False)
            self.modelSelector.setEnabled(False)
            self.settings.setEnabled(False)

            self.currentModelTrainer.epochs = self.settings.epochsSpinBox.value()
            self.currentModelTrainer.workers = self.settings.workerSpinBox.value()
            self.currentModelTrainer.batch = self.settings.batchSpinBox.value()
            self.currentModelTrainer.modelPath = self.settings.modelPathTextEdit.text()
            self.currentModelTrainer.modelName = self.settings.modelNameTextEdit.text()

            if self.trainerThread is None:
                self.trainerThread = QtCore.QThread()

            if not self.currentModelTrainer.connectedToThread:
                self.currentModelTrainer.moveToThread(self.trainerThread)

                self.trainerThread.started.connect(self.currentModelTrainer.run)

                self.currentModelTrainer.progress.connect(
                    self.modelOutput.progressBar.setValue
                )
                self.currentModelTrainer.status.connect(self.statusTextChanged)
                self.currentModelTrainer.error.connect(self.showError)
                self.currentModelTrainer.errorExit.connect(self.errorExit)

                self.currentModelTrainer.finished.connect(self.trainingEnded)
                self.currentModelTrainer.connectedToThread = True

            self.modelOutput.statusTextEdit.clear()
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
        self.modelSelector.setEnabled(True)
        self.settings.setEnabled(True)

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
        self.modelOutput.statusTextEdit.setPlainText(
            self.modelOutput.statusTextEdit.toPlainText() + "\n" + text
        )
        self._statusTextEdit.moveCursor(QTextCursor.End)  # type: ignore

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
        self.modelSelector.selector.setCurrentIndex(settings.model)

        self.settings.batchSpinBox.setValue(settings.batchSize)
        self.settings.workerSpinBox.setValue(settings.numberOfWorkers)
        self.settings.epochsSpinBox.setValue(settings.numberOfEpochs)

        self.settings.modelPathTextEdit.setText(settings.modelOutputPath)
        self.settings.modelNameTextEdit.setText(settings.modelName)

    def updateSettings(self):
        settings = SharedValues().settings.training
        settings.model = self.modelSelector.selector.currentIndex()

        settings.batchSize = self.settings.batchSpinBox.value()
        settings.numberOfWorkers = self.settings.workerSpinBox.value()
        settings.numberOfEpochs = self.settings.epochsSpinBox.value()

        settings.modelOutputPath = self.settings.modelPathTextEdit.text()
        settings.modelName = self.settings.modelNameTextEdit.text()

    #######################################################
    # Other
    #######################################################

    @Slot(int)
    def modelChanged(self, index: int) -> None:
        self.settings.settingsLabel.setText(f"Settings for {MODELS[index]}:")

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        pass
