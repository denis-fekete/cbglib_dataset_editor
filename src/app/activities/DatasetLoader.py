"""
Module: DatasetLoader.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for loading and exporting image datasets.
"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot

import os
from pathlib import Path
import yaml
from typing import Callable

from app.widgets import *
from app.dataset import *
from app.labeling import *
from app.settings import *
from app.utils.SharedValues import SharedValues
from .datasetLoaderWidgets.ExportToolbar import ExportToolbar
from .datasetLoaderWidgets.ImportToolbar import ImportToolbar
from .datasetLoaderWidgets.DatasetInfoToolbar import DatasetInfoToolbar


class DatasetLoader(AbstractTabWidget):
    def __init__(
        self,
        screenScaleText_fn: Callable[[], float],
        setTabsEnabled_fn: Callable[[bool], None],
    ):
        super().__init__()

        self.screenScaleText_fn = screenScaleText_fn
        self.setParentEnabled_fn = setTabsEnabled_fn
        self.dataYamlPath: str | None = None
        self.incorrectLabels: bool = True
        self.imageDataset = ImageDataset(self.screenScaleText_fn)

        self._initUI()

    def _initUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self.importToolbar = ImportToolbar()
        self.importToolbar.importDialog.connect(self.openImportDialog)
        self.importToolbar.importClicked.connect(self.importDataset)
        self.importToolbar.importPathChanged.connect(self.importPathChanged)

        self.exportToolbar = ExportToolbar()
        self.exportToolbar.exportClicked.connect(self.exportDataset)
        self.exportToolbar.exportDialog.connect(self.openExportDialog)
        self.exportToolbar.exportPathChanged.connect(self.exportPathChanged)

        self.datasetInfoToolbar = DatasetInfoToolbar()

        self.layout().addWidget(self.importToolbar, 0, 0)
        self.layout().addWidget(self.exportToolbar, 1, 0)
        self.layout().addWidget(self.datasetInfoToolbar, 0, 1, 3, 1)

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
            self.importToolbar.importPathTextEdit.setText(textPath)
            self.dataYamlPath = None

            self.importDataset()

    @Slot(str)
    def importPathChanged(self, text: str) -> None:
        SharedValues().datasetImportPath = text

    @Slot()
    def importDataset(self) -> None:
        """Loads `ImageDataset` from `self.importToolbar.importPathTextEdit`"""
        path = Path(self.importToolbar.importPathTextEdit.text())
        if self.importToolbar.importPathTextEdit.text() == "" or not path.is_dir():
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Not a valid path for import dataset."
            )

        SharedValues().imageSamples.clear()
        self.imageDataset.loadImageSamples(
            SharedValues().datasetImportPath,
            SharedValues().imageSamples,
            SharedValues().labelsDict,
        )
        self.updateDataYaml()

        self.importToolbar.treeView.loadSamplesFull()

    #######################################################
    # Exporting dataset
    #######################################################

    @Slot()
    def openExportDialog(self) -> None:
        """Opens OS dialog window to choose a directory to which a dataset will be exported"""
        textPath = QtWidgets.QFileDialog().getExistingDirectory(
            self, "Select a Folder", "", QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        self.exportToolbar.exportPathTextEdit.setText(textPath)

    @Slot()
    def exportDataset(self) -> None:
        """Qt slot for starting export"""
        exportPath = Path(SharedValues().datasetExportPath)
        self.exportToolbar.progressBar.setEnabled(True)

        if SharedValues().datasetExportPath == "":
            newExportPath = Path(SharedValues().datasetImportPath).parent / "exported"
            os.makedirs(newExportPath, exist_ok=True)
            # SharedValues().datasetExportPath = _exportPathTextEdit.text() called automatically
            self.exportToolbar.exportPathTextEdit.setText(str(newExportPath.resolve()))
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
        self.exportToolbar.progressBar.setValue(progress)

    @Slot()
    def exportProgressDone(self) -> None:
        self.exportToolbar.progressBar.setEnabled(False)
        self.exportToolbar.setEnabled(True)
        self.importToolbar.setEnabled(True)
        self.datasetInfoToolbar.setEnabled(True)
        self.setParentEnabled_fn(True)

    def updateDataYaml(self) -> None:
        """
        Updates values of `data.yaml` based on `SharedValues().datasetImportPath` and loads all
        class indexes and labels from data.yaml
        """
        path = Path(SharedValues().datasetImportPath)

        self.datasetInfoToolbar.dataPath.setText(path.name)
        self.datasetInfoToolbar.valPath.setText("images/val")
        self.datasetInfoToolbar.trainPath.setText("images/train")
        self.datasetInfoToolbar.testPath.setText("# not used")

        if self.imageDataset.dataYamlPath is None:
            return

        with open(self.imageDataset.dataYamlPath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for index, name in data["names"].items():
            SharedValues().labelsDict[index] = LabelEntry(name, index)

        self.datasetInfoToolbar.treeView.loadLabels()

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
            applyFilters=self.exportToolbar.applyFiltersCheckBox.isChecked(),
            separateByClasses=self.exportToolbar.separateByClassesCheckBox.isChecked(),
            generateNameFromClass=self.exportToolbar.generateNameCheckBox.isChecked(),
            trainDataPercentage=self.exportToolbar.trainDataPercentageSpinBox.value(),
        )
        self.worker.moveToThread(self.workerThread)

        self.workerThread.started.connect(self.worker.run)
        self.worker.progress.connect(self.exportProgressUpdate)
        self.worker.finished.connect(self.exportProgressDone)

        self.worker.finished.connect(self.workerThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.workerThread.finished.connect(self.workerThread.deleteLater)

        self.exportToolbar.progressBar.setEnabled(True)
        self.exportToolbar.setEnabled(False)
        self.importToolbar.setEnabled(False)
        self.datasetInfoToolbar.setEnabled(False)
        self.setParentEnabled_fn(False)

        self.workerThread.start()

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.dataset
        self.exportToolbar.trainDataPercentageSpinBox.setValue(
            min(settings.trainDataPercent, 100)
        )

        self.exportToolbar.applyFiltersCheckBox.setChecked(settings.generateSynthetic)
        self.exportToolbar.generateNameCheckBox.setChecked(settings.generateNames)
        self.exportToolbar.separateByClassesCheckBox.setChecked(
            settings.separateToSubdirectories
        )
        self.importToolbar.importPathTextEdit.setText(settings.importPath)

    def updateSettings(self):
        settings = SharedValues().settings.dataset
        settings.separateToSubdirectories = (
            self.exportToolbar.separateByClassesCheckBox.isChecked()
        )
        settings.generateNames = self.exportToolbar.generateNameCheckBox.isChecked()
        settings.generateSynthetic = self.exportToolbar.applyFiltersCheckBox.isChecked()
        settings.trainDataPercent = (
            self.exportToolbar.trainDataPercentageSpinBox.value()
        )
        settings.importPath = self.importToolbar.importPathTextEdit.text()

    #######################################################
    # Other
    #######################################################

    def tabSelected(self) -> None:
        self.incorrectLabels = self.importToolbar.treeView.loadSamplesFull(
            restoreVerticalPosition=True
        )
        self.datasetInfoToolbar.treeView.loadLabels()
        self.exportToolbar.btnExport.setDisabled(self.incorrectLabels)
        if self.incorrectLabels:
            self.exportToolbar.btnExport.setText(
                "Start Export (disabled until default labels are replaced)"
            )
        else:
            self.exportToolbar.btnExport.setText("Start Export")

    def tabClosed(self) -> None:
        pass
