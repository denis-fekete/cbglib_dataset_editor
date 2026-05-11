"""
Module: ModelTrainer.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for training models.
"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
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
    safeToExit = Signal()

    def __init__(self, setTabsEnabled_fn: Callable[[bool], None]) -> None:
        super().__init__()
        self.ui = Ui_DataTrainerWidget()
        self.ui.setupUi(self)  # type: ignore

        self.pathValidated: bool = False
        self.setTabsEnabled_fn = setTabsEnabled_fn
        self.trainerThread: QtCore.QThread | None = None
        self.currentModelTrainer: AbstractModelTrainer | None = None

        self.datasetValidated = False
        self.modelSelectorIndex = 0
        self.closeOnFinishFlag = False

        self._connectUI()

    def _connectUI(self) -> None:
        self.currentModelTrainer = None

        self.ui.generateNameButton.clicked.connect(self.generateModelName)
        self.ui.generateOutputDirectoryButton.clicked.connect(self.generateModelPath)
        self.ui.validateButton.clicked.connect(self.validateDataset)
        self.ui.startTrainingButton.clicked.connect(self.startTraining)
        self.ui.datasetPathLineEdit.textChanged.connect(self.datasetPathEdited)
        self.ui.exitTrainingButton.clicked.connect(self.stopTraining)

        for i in range(0, len(DATASET_PATHS)):
            self.ui.datasetPathComboBox.addItem(DATASET_PATHS[i])

        self.ui.customModelOpenButton.clicked.connect(self.openCustomModelPathDialog)

        for key in MODELS_NAMES.keys():
            self.ui.modelSelectorComboBox.addItem(MODELS_NAMES[key])

        self.ui.modelSelectorComboBox.currentIndexChanged.connect(self.modelSelectorComboBoxChanged)
        self.ui.datasetPathComboBox.currentIndexChanged.connect(self.datasetComboBoxChanged)

    #######################################################
    # Training Settings
    #######################################################

    @Slot(int)
    def modelSelectorComboBoxChanged(self, index: int) -> None:
        if index == CUSTOM_MODEL:
            self.ui.customModelWidget.setVisible(True)
        else:
            self.ui.customModelWidget.setVisible(False)

        if self.modelSelectorIndex != index:
            self.ui.startTrainingButton.setEnabled(False)
            self.datasetValidated = False

        self.modelSelectorIndex = index

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

        self.datasetValidated, message = self.currentModelTrainer.validateDataset(
            self.ui.datasetPathLineEdit.text()
        )

        if not self.datasetValidated:
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

    #######################################################
    # Training
    #######################################################

    @Slot()
    def startTraining(self) -> None:
        if self.currentModelTrainer is not None:
            self.uiTrainingStarted()

            self.currentModelTrainer.epochs = self.ui.epochsSpinBox.value()
            self.currentModelTrainer.workers = self.ui.workersSpinBox.value()
            self.currentModelTrainer.batch = self.ui.batchSpinBox.value()
            self.currentModelTrainer.patience = self.ui.patienceSpinBox.value()
            self.currentModelTrainer.modelPath = self.ui.modelOutputPathLineEdit.text()
            self.currentModelTrainer.modelName = self.ui.modelNameLineEdit.text()

            if self.trainerThread is None:
                self.trainerThread = QtCore.QThread()

            if not self.currentModelTrainer.connectedToThread:
                self.currentModelTrainer.moveToThread(self.trainerThread)

                self.trainerThread.started.connect(self.currentModelTrainer.run)

                self.currentModelTrainer.progress.connect(self.ui.trainingProgressBar.setValue)
                self.currentModelTrainer.status.connect(self.statusTextChanged)
                self.currentModelTrainer.errorExit.connect(self.errorExit)

                self.currentModelTrainer.finished.connect(self.trainingEnded)
                self.currentModelTrainer.connectedToThread = True

            self.ui.logOutputTextEdit.clear()
            self.trainerThread.start()
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Model trainer not selected",
                "Model trainer is not selected or not supported. " "Training will not start",
            )

    @Slot()
    def trainingEnded(self) -> None:
        """Slot called one the training ended"""
        if self.ui.onnxExportCheckBox.isChecked():
            self.currentModelTrainer.exportONNX()

            if self.closeOnFinishFlag:
                self.safeToExit.emit()  # wait until export
        else:
            if self.closeOnFinishFlag:
                self.safeToExit.emit()

        self.uiTrainingEnded()
        self.closeModelTrainer()

    @Slot()
    def stopTraining(self):
        if self.currentModelTrainer is not None:
            self.currentModelTrainer.stop()

    @Slot()
    def closeModelTrainer(self) -> bool:
        if self.trainerThread is None:
            return True

        if self.trainerThread.isRunning():
            if self.currentModelTrainer.isTraining:
                self.closeOnFinishFlag = True
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setWindowTitle("Training in Progress")
                msgBox.setText(
                    "Training in progress.\n"
                    "Do you want to exit after the current epoch finishes?"
                )
                gracefulExitButton = msgBox.addButton(
                    "Save exit", QtWidgets.QMessageBox.ButtonRole.AcceptRole
                )
                forceExitButton = msgBox.addButton(
                    "Force exit", QtWidgets.QMessageBox.ButtonRole.RejectRole
                )
                msgBox.setDefaultButton(forceExitButton)

                msgBox.exec()

                if msgBox.clickedButton() == gracefulExitButton:
                    self.currentModelTrainer.stop()
                    return False

        if self.currentModelTrainer is not None:
            self.currentModelTrainer.deleteLater()
            self.currentModelTrainer = None

        self.trainerThread.quit()
        self.trainerThread.deleteLater()
        self.trainerThread = None

        return True

    @Slot(str)
    def statusTextChanged(self, text: str) -> None:
        self.ui.logOutputTextEdit.setPlainText(
            self.ui.logOutputTextEdit.toPlainText() + "\n" + text
        )
        self.ui.logOutputTextEdit.moveCursor(QTextCursor.End)  # pyright: ignore

    @Slot(str)
    def errorExit(self, text: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Error occurred during training", text)

        if self.closeOnFinishFlag:
            self.safeToExit.emit()

        self.uiTrainingEnded()
        self.closeModelTrainer()

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.training
        self.ui.modelSelectorComboBox.setCurrentIndex(settings.model)
        if settings.model == 0:
            self.ui.customModelWidget.setVisible(True)
        else:
            self.ui.customModelWidget.setVisible(False)

        self.ui.batchSpinBox.setValue(settings.batchSize)
        self.ui.workersSpinBox.setValue(settings.numberOfWorkers)
        self.ui.epochsSpinBox.setValue(settings.numberOfEpochs)
        self.ui.patienceSpinBox.setValue(settings.patience)

        self.ui.modelOutputPathLineEdit.setText(settings.modelOutputPath)
        self.ui.onnxExportCheckBox.setChecked(settings.onnxExport)

    def updateSettings(self):
        settings = SharedValues().settings.training
        settings.model = self.ui.modelSelectorComboBox.currentIndex()

        settings.batchSize = self.ui.batchSpinBox.value()
        settings.numberOfWorkers = self.ui.workersSpinBox.value()
        settings.numberOfEpochs = self.ui.epochsSpinBox.value()
        settings.patience = self.ui.patienceSpinBox.value()

        settings.modelOutputPath = self.ui.modelOutputPathLineEdit.text()
        settings.onnxExport = self.ui.onnxExportCheckBox.isChecked()

    #######################################################
    # Other
    #######################################################

    @Slot()
    def openCustomModelPathDialog(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a model", "", "Pytorch Tensor (*.pt)"
        )
        self.ui.customModelPathLineEdit.setText(fileName)

    def uiTrainingEnded(self):
        """Enables UI elements after the training has ended"""
        self.setTabsEnabled_fn(True)
        self.ui.validateButton.setEnabled(True)
        self.ui.startTrainingButton.setEnabled(True)
        self.ui.modelSettingsWidget.setEnabled(True)

        self.ui.exitTrainingButton.setEnabled(False)
        self.ui.trainingProgressBar.setEnabled(False)

    def uiTrainingStarted(self):
        """Disables UI elements after the training has stated"""
        self.setTabsEnabled_fn(False)
        self.ui.validateButton.setEnabled(False)
        self.ui.startTrainingButton.setEnabled(False)
        self.ui.modelSettingsWidget.setEnabled(False)

        self.ui.exitTrainingButton.setEnabled(True)
        self.ui.trainingProgressBar.setEnabled(True)

    def _getCorrectModel(self, index: int):
        if index == CUSTOM_MODEL:
            try:
                self.currentModelTrainer = CustomYoloUltralyticsTrainer(
                    self.ui.customModelPathLineEdit.text()
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error: Loading custom model", e.__str__())
                self.currentModelTrainer = None
        elif index == YOLO_V8_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV8n()
        elif index == YOLO_V8_S_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV8s()
        elif index == YOLO_V8_M_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV8m()
        elif index == YOLO_V11_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV11n()
        elif index == YOLO_V11_S_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV11s()
        elif index == YOLO_V11_M_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV11m()
        elif index == YOLO_V26_N_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV26n()
        elif index == YOLO_V26_S_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV26s()
        elif index == YOLO_V26_M_MODEL_INDEX:
            self.currentModelTrainer = YoloUltralyticsTrainerV26m()

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        pass
