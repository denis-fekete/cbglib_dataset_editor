"""
Module: DatasetLoader.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for loading and exporting image datasets.
"""

from PySide6 import QtCore, QtWidgets
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

        self.ui.calcStatisticsButton.clicked.connect(self.calculateStatistics)

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
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Not a valid path for import dataset."
            )

        SharedValues().imageSamples.clear()
        self.onImportStart.emit()
        self.onImportEnded.emit()

        try:
            self.imageDataset.loadImageSamples(
                SharedValues().datasetImportPath,
                SharedValues().imageSamples,
                SharedValues().labelsDict,
            )

            self.updateDataYaml()

            self.ui.imageSampleTreeView.loadSamples(showFull=True)
            self.onImportEnded.emit()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", e.__str__())

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

        self.saveImageSamplesStart()

    @Slot(str)
    def exportPathChanged(self, text: str) -> None:
        SharedValues().datasetExportPath = text

    @Slot(int)
    def exportProgressUpdate(self, progress: int) -> None:
        self.ui.exportProgressBar.setValue(progress)

    @Slot()
    def exportProgressDone(self) -> None:
        self.ui.exportWidget.setEnabled(False)
        self.ui.importExportWidget.setEnabled(True)
        self.ui.detailsWidget.setEnabled(True)
        self.setParentEnabled_fn(True)

    def updateDataYaml(self) -> None:
        """
        Updates values of `data.yaml` based on `SharedValues().datasetImportPath` and loads all
        class indexes and labels from data.yaml
        """
        path = Path(SharedValues().datasetImportPath)

        self.ui.dataPathLabel.setText(path.name)

        self.ui.valLineEdit.setText("images/val")
        self.ui.trainLineEdit.setText("images/train")
        self.ui.testLineEdit.setText("# not used")

        if self.imageDataset.dataYamlPath is None:
            return

        with open(self.imageDataset.dataYamlPath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for index, name in data["names"].items():
            SharedValues().labelsDict[index] = LabelEntry(name, index)

        self.ui.classesTreeView.loadLabels()

    def saveImageSamplesStart(self) -> None:
        """Saves images to the `exportRootPath`"""
        self.workerThread = QtCore.QThread()

        if SharedValues().datasetExportPath == "":
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                'Export root path is ""',
            )
            return

        self.worker = ExportWorker(
            imageSamples=SharedValues().imageSamples,
            filterPresets=SharedValues().filterPresets,
            labelsDict=SharedValues().labelsDict,
            exportRootPath=SharedValues().datasetExportPath,
            applyFilters=self.ui.genSyntheticCheckBox.isChecked(),
            separateByClasses=self.ui.separateCheckBox.isChecked(),
            generateNameFromClass=self.ui.genNamesCheckBox.isChecked(),
            trainDataPercentage=self.ui.trainPercentSpinBox.value(),
        )
        self.worker.moveToThread(self.workerThread)

        self.workerThread.started.connect(self.worker.run)
        self.worker.progress.connect(self.exportProgressUpdate)
        self.worker.finished.connect(self.exportProgressDone)

        self.worker.finished.connect(self.workerThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.workerThread.finished.connect(self.workerThread.deleteLater)

        self.ui.exportWidget.setEnabled(True)
        self.ui.importExportWidget.setEnabled(False)
        self.ui.detailsWidget.setEnabled(False)
        self.setParentEnabled_fn(False)

        self.workerThread.start()

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.dataset
        self.ui.trainPercentSpinBox.setValue(min(settings.trainDataPercent, 100))

        self.ui.genSyntheticCheckBox.setChecked(settings.generateSynthetic)
        self.ui.genNamesCheckBox.setChecked(settings.generateNames)
        self.ui.separateCheckBox.setChecked(settings.separateToSubdirectories)
        self.ui.importLineEdit.setText(settings.importPath)

    def updateSettings(self):
        settings = SharedValues().settings.dataset
        settings.separateToSubdirectories = self.ui.separateCheckBox.isChecked()
        settings.generateNames = self.ui.genNamesCheckBox.isChecked()
        settings.generateSynthetic = self.ui.genSyntheticCheckBox.isChecked()
        settings.trainDataPercent = self.ui.trainPercentSpinBox.value()
        settings.importPath = self.ui.importLineEdit.text()

    #######################################################
    # Statistics
    #######################################################
    @Slot()
    def calculateStatistics(self):
        sVals = SharedValues()

        sVals.statistics.emptySamples = 0
        sVals.statistics.labelBoxes = 0

        for sample in SharedValues().imageSamples:
            sample._loadImageAndLabel(skipLabel=False, skipImage=True)  # type: ignore
            boxes = len(sample.labelBoxes)

            if boxes == 0:
                sVals.statistics.emptySamples += 1
            else:
                sVals.statistics.labelBoxes += boxes

        sVals.statistics.classes = len(SharedValues().labelsDict)
        sVals.statistics.imageSamples = len(SharedValues().imageSamples)

        self.ui.labeledLineEdit.setText(f"{sVals.statistics.labelBoxes}")
        self.ui.imageSamplesLineEdit.setText(f"{sVals.statistics.imageSamples}")
        self.ui.annotatedLineEdit.setText(f"{sVals.statistics.labeledSamples}")
        self.ui.emptySamplesLineEdit.setText(f"{sVals.statistics.emptySamples}")
        self.ui.totalClassesLineEdit.setText(f"{sVals.statistics.classes}")
        self.ui.labelBoxesLineEdit.setText(f"{sVals.statistics.labelBoxes}")

        pass

    #######################################################
    # Other
    #######################################################

    def tabSelected(self) -> None:
        self.incorrectLabels = self.ui.imageSampleTreeView.loadSamples(
            restoreVerticalPosition=True, showFull=True
        )
        self.ui.classesTreeView.loadLabels()
        self.ui.exportButton.setDisabled(self.incorrectLabels)
        if self.incorrectLabels:
            self.ui.exportButton.setText(
                "Export (disabled until default labels are replaced)"
            )
        else:
            self.ui.exportButton.setText("Export")

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        pass
