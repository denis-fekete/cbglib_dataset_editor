"""
Module: DatasetLoader.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for loading and exporting image datasets.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Signal

import os
from pathlib import Path
import yaml
from typing import Callable

from app.widgets import *
from app.dataset import *
from app.labeling import *
from app.settings import *
from app.utils.SharedValues import SharedValues

from app.ui.DatasetManager_ui import Ui_DatasetManager


class DatasetManager(AbstractTabWidget):
    onImportStart = Signal()
    onImportEnded = Signal()

    def __init__(
        self,
        screenScaleText_fn: Callable[[], float],
        setTabsEnabled_fn: Callable[[bool], None],
    ):
        super().__init__()
        self.ui = Ui_DatasetManager()
        self.ui.setupUi(self)  # type: ignore

        self.screenScaleText_fn = screenScaleText_fn
        self.setParentEnabled_fn = setTabsEnabled_fn
        self.dataYamlPath: str | None = None
        self.incorrectLabels: bool = True

        self.imageDataset = ImageDataset(self.screenScaleText_fn)
        self.imageDataset.importFinished.connect(self.importFinished)
        self.imageDataset.exportFinished.connect(self.exportFinished)
        self.imageDataset.progressUpdate.connect(self.progressUpdate)
        self.imageDataset.error.connect(self.importError)

        self.statisticsCalculated = False

        self._connectUI()

    def _connectUI(self) -> None:
        self.ui.classesTreeView.setLabels(SharedValues().labelsDict)
        self.ui.imageSampleTreeView.setImageSamples(SharedValues().imageSamples)

        self.ui.importButton.clicked.connect(self.importDataset)
        self.ui.importOpenButton.clicked.connect(self.openImportDialog)
        self.ui.importLineEdit.textChanged.connect(self.importPathChanged)

        self.ui.exportButton.clicked.connect(self.exportDataset)
        self.ui.exportOpenButton.clicked.connect(self.openExportDialog)
        self.ui.exportLineEdit.textChanged.connect(self.exportPathChanged)

        # lambda to prevent Qt sending checked argument which is misinterpreted as skipBoxesAndLabels
        self.ui.calcStatisticsButton.clicked.connect(lambda: self.calculateStatistics())

    #######################################################
    # Importing dataset
    #######################################################

    @Slot()
    def openImportDialog(self) -> None:
        """Open OS dialog window to choose a directory from which a dataset will be imported"""
        textPath = QtWidgets.QFileDialog().getExistingDirectory(
            self, "Select a Folder", "", QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        if textPath == "":
            return
        else:
            self.ui.importLineEdit.setText(textPath)
            self.dataYamlPath = None

            self.importDataset()

    @Slot(str)
    def importPathChanged(self, text: str) -> None:
        SharedValues().datasetImportPath = text

    @Slot()
    def importDataset(self) -> None:
        """Loads `ImageDataset` from `self.importToolbar.importPathTextEdit`"""
        path = Path(self.ui.importLineEdit.text())

        if self.ui.importLineEdit.text() == "" or not path.is_dir():
            QtWidgets.QMessageBox.warning(self, "Warning", "Not a valid path for import dataset.")
            return

        self.statisticsCalculated = False  # reset statistic flag

        SharedValues().imageSamples.clear()
        self.onImportStart.emit()

        self.ui.exportProgressBar.setEnabled(True)
        self.ui.importExportWidget.setEnabled(False)
        self.ui.detailsWidget.setEnabled(False)
        self.setParentEnabled_fn(False)
        try:
            self.progressReset()
            self.imageDataset.importDataset()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", e.__str__())
            self.exportFinished()

    @Slot(str)
    def importError(self, msg: str):
        QtWidgets.QMessageBox.critical(self, "Import error", msg)
        self.importFinished()

    @Slot()
    def importFinished(self):
        self.updateDataYaml()
        self.onImportEnded.emit()
        self.updateImportStatistics()
        self.exportFinished()
        self.progressUpdate(100)
        self.ui.imageSampleTreeView.loadSamples(showFull=True)

    #######################################################
    # Exporting dataset
    #######################################################

    @Slot()
    def openExportDialog(self) -> None:
        """Opens OS dialog window to choose a directory to which a dataset will be exported"""
        textPath = QtWidgets.QFileDialog().getExistingDirectory(
            self, "Select a Folder", "", QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        self.ui.exportLineEdit.setText(textPath)

    @Slot()
    def exportDataset(self) -> None:
        """Start the export of dataset"""
        exportPath = Path(SharedValues().datasetExportPath)

        if SharedValues().datasetExportPath == "":
            newExportPath = Path(SharedValues().datasetImportPath).parent / "exported"
            os.makedirs(newExportPath, exist_ok=True)
            # SharedValues().datasetExportPath =  self.ui.exportLineEdit.text() called automatically
            self.ui.exportLineEdit.setText(str(newExportPath.resolve()))
            SharedValues().datasetExportPath = self.ui.exportLineEdit.text()
        else:
            if exportPath.exists():
                if not exportPath.is_dir():
                    QtWidgets.QMessageBox.critical(
                        self,
                        "Error",
                        "Export root path exists but it is not a directory!",
                    )
                    return
            else:
                exportPath.mkdir(exist_ok=True)

        if (
            not self.ui.exportOriginalCheckBox.isChecked()
            and not self.ui.genSyntheticTrainCheckBox.isChecked()
            and not self.ui.genSyntheticValCheckBox.isChecked()
        ):
            QtWidgets.QMessageBox.warning(
                self,
                "Wrong export configuration",
                "Exporting original image, synthetic training, and synthetic validation data are disabled, there is nothing to export!",
            )
            return

        if len(SharedValues().imageSamples) <= 0:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "Dataset is empty",
            )
            return

        self.ui.exportProgressBar.setEnabled(True)
        self.ui.importExportWidget.setEnabled(False)
        self.ui.detailsWidget.setEnabled(False)
        self.setParentEnabled_fn(False)

        self.progressReset()

        self.imageDataset.exportDataset(
            trainDataPercentage=self.ui.trainPercentSpinBox.value(),
            numOfWorkers=self.ui.workerThreadsSpinBox.value(),
            genSyntheticTrain=self.ui.genSyntheticTrainCheckBox.isChecked(),
            genSyntheticVal=self.ui.genSyntheticValCheckBox.isChecked(),
            separateByClasses=self.ui.separateCheckBox.isChecked(),
            generateNameFromClass=self.ui.genNamesCheckBox.isChecked(),
            exportOriginal=self.ui.exportOriginalCheckBox.isChecked(),
        )

    @Slot(str)
    def exportPathChanged(self, text: str) -> None:
        SharedValues().datasetExportPath = text

    @Slot(float)
    def progressUpdate(self, value: int) -> None:
        self.ui.exportProgressBar.setValue(value)

    @Slot()
    def progressReset(self) -> None:
        self.ui.exportProgressBar.setValue(0)

    def updateDataYaml(self) -> None:
        """
        Updates values of `data.yaml` based on `SharedValues().datasetImportPath` and loads all
        class indexes and labels from data.yaml
        """
        path = Path(SharedValues().datasetImportPath)

        self.ui.dataPathLineEdit.setText(path.name)

        self.ui.valLineEdit.setText("images/val")
        self.ui.trainLineEdit.setText("images/train")
        self.ui.testLineEdit.setText("# not used")

        if self.imageDataset.dataYamlPath is None:
            return

        with open(self.imageDataset.dataYamlPath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for index, name in data["names"].items():
            SharedValues().labelsDict[index] = LabelEntry(name, index)

        self.ui.classesTreeView.loadLabels(showCounts=self.statisticsCalculated)

    @Slot()
    def exportFinished(self) -> None:
        self.ui.exportProgressBar.setEnabled(False)
        self.ui.importExportWidget.setEnabled(True)
        self.ui.detailsWidget.setEnabled(True)
        self.setParentEnabled_fn(True)

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.dataset
        self.ui.trainPercentSpinBox.setValue(min(settings.trainDataPercent, 100))

        self.ui.genSyntheticTrainCheckBox.setChecked(settings.generateSyntheticTrain)
        self.ui.genSyntheticValCheckBox.setChecked(settings.generateSyntheticVal)
        self.ui.genNamesCheckBox.setChecked(settings.generateNames)
        self.ui.separateCheckBox.setChecked(settings.separateToSubdirectories)
        self.ui.importLineEdit.setText(settings.importPath)
        self.ui.workerThreadsSpinBox.setValue(settings.workers)
        self.ui.exportOriginalCheckBox.setChecked(settings.exportOriginal)

    def updateSettings(self):
        settings = SharedValues().settings.dataset
        settings.separateToSubdirectories = self.ui.separateCheckBox.isChecked()
        settings.generateNames = self.ui.genNamesCheckBox.isChecked()
        settings.generateSyntheticTrain = self.ui.genSyntheticTrainCheckBox.isChecked()
        settings.generateSyntheticVal = self.ui.genSyntheticValCheckBox.isChecked()
        settings.trainDataPercent = self.ui.trainPercentSpinBox.value()
        settings.importPath = self.ui.importLineEdit.text()

        settings.workers = self.ui.workerThreadsSpinBox.value()
        settings.exportOriginal = self.ui.exportOriginalCheckBox.isChecked()

    #######################################################
    # Statistics
    #######################################################
    @Slot()
    def calculateStatistics(self):
        sVals = SharedValues()

        sVals.statistics.emptySamples = 0
        sVals.statistics.labelBoxes = 0

        self.imageDataset.calculateStatistics()

        sVals.statistics.classes = len(SharedValues().labelsDict)
        sVals.statistics.imageSamples = len(SharedValues().imageSamples)
        self.ui.emptySamplesLineEdit.setText(f"{sVals.statistics.emptySamples}")
        self.ui.labelBoxesLineEdit.setText(f"{sVals.statistics.labelBoxes}")

        self.statisticsCalculated = True
        self.ui.classesTreeView.loadLabels(showCounts=True)

        self.updateImportStatistics()

    @Slot()
    def updateImportStatistics(self):
        sVals = SharedValues()
        self.ui.labelFilesLineEdit.setText(f"{sVals.statistics.labelsFiles}")
        self.ui.imageSamplesLineEdit.setText(f"{sVals.statistics.imageSamples}")
        self.ui.annotatedLineEdit.setText(f"{sVals.statistics.labeledSamples}")
        self.ui.totalClassesLineEdit.setText(f"{sVals.statistics.classes}")

        self.ui.trainSamplesLineEdit.setText(f"{sVals.statistics.trainSamples}")
        self.ui.valSamplesLineEdit.setText(f"{sVals.statistics.valSamples}")
        self.ui.testSamplesLineEdit.setText(f"{sVals.statistics.testSamples}")

    #######################################################
    # Other
    #######################################################

    def tabSelected(self) -> None:
        self.incorrectLabels = self.ui.imageSampleTreeView.loadSamples(
            restoreVerticalPosition=True, showFull=True
        )
        self.ui.classesTreeView.loadLabels(showCounts=self.statisticsCalculated)
        self.ui.exportButton.setDisabled(self.incorrectLabels)
        if self.incorrectLabels:
            self.ui.exportButton.setText("Export (disabled until default labels are replaced)")
        else:
            self.ui.exportButton.setText("Export")

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        pass
