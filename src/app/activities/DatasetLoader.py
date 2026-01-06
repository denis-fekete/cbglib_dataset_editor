from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Slot

import os
from pathlib import Path
import yaml
from typing import Callable

from app.widgets import *
from app.image_manipulation import *
from app.utils import *
from app.data_classes import *
from .AbstractTabWidget import AbstractTabWidget


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

        self._initImportContainer()
        self._initExportContainer()
        self._initDataYamlContainer()
        self._initExportProgressContainer()

        self.layout().addWidget(self._importContainer, 0, 0)
        self.layout().addWidget(self._exportContainer, 1, 0)
        self.layout().addWidget(self._exportProgressContainer, 2, 0)
        self.layout().addWidget(self._dataYamlContainer, 0, 1, 3, 1)

    def _initImportContainer(self) -> None:
        self._importContainer = QtWidgets.QWidget()
        self._importContainer.setLayout(QtWidgets.QGridLayout())
        importPathLabel = QtWidgets.QLabel(
            "Path to import dataset from (subdirectories will be imported as well)"
        )
        importPathLabel.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self._importPathTextEdit = QtWidgets.QLineEdit()
        self._importPathTextEdit.textChanged.connect(
            self._importPathTextEditChanged_slot
        )

        self._btnImportDialog = QtWidgets.QPushButton("Import")
        self._btnImportDialog.clicked.connect(self.btnImport_slot)

        self.datasetTreeView = ImageSampleTreeView(SharedValues().imageSamples)

        self._importContainer.layout().addWidget(importPathLabel, 0, 0, 1, 2)
        self._importContainer.layout().addWidget(self._importPathTextEdit, 1, 0)
        self._importContainer.layout().addWidget(self._btnImportDialog, 1, 1)
        self._importContainer.layout().addWidget(self.datasetTreeView, 2, 0, 1, 2)

    def _initExportContainer(self) -> None:
        self._exportContainer = QtWidgets.QWidget()
        self._exportContainer.setLayout(QtWidgets.QGridLayout())
        exportPathLabel = QtWidgets.QLabel("Path to export dataset to")
        exportPathLabel.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self._exportPathTextEdit = QtWidgets.QLineEdit()
        self._exportPathTextEdit.textChanged.connect(
            self._exportPathTextEditChanged_slot
        )

        self._btnExportDialog = QtWidgets.QPushButton("Open")
        self._btnExportDialog.clicked.connect(self.btnExportDialog_slot)

        self._btnExport = QtWidgets.QPushButton("Start Export")
        self._btnExport.clicked.connect(self.btnExport_slot)

        self._applyFiltersCheckBox = QtWidgets.QCheckBox("Apply filters")
        self._applyFiltersCheckBox.setChecked(True)

        self._generateNameCheckBox = QtWidgets.QCheckBox("Generate name from class")
        self._generateNameCheckBox.setChecked(True)

        self._trainDataPercentageSpinBox = QtWidgets.QSpinBox(prefix="Train data %:")
        self._trainDataPercentageSpinBox.setMinimum(0)
        self._trainDataPercentageSpinBox.setMaximum(100)
        self._trainDataPercentageSpinBox.setValue(100)

        self._separateByClassesCheckBox = QtWidgets.QCheckBox(
            "Separate classes into subdirectories"
        )
        self._separateByClassesCheckBox.setChecked(True)

        self._exportContainer.layout().addWidget(exportPathLabel, 0, 0, 1, 2)
        self._exportContainer.layout().addWidget(self._exportPathTextEdit, 1, 0)
        self._exportContainer.layout().addWidget(self._btnExportDialog, 1, 1)
        self._exportContainer.layout().addWidget(self._trainDataPercentageSpinBox, 2, 0)
        self._exportContainer.layout().addWidget(self._generateNameCheckBox, 2, 1)
        self._exportContainer.layout().addWidget(self._separateByClassesCheckBox, 2, 2)
        self._exportContainer.layout().addWidget(self._applyFiltersCheckBox, 2, 3)
        self._exportContainer.layout().addWidget(self._btnExport, 3, 0)

    def _initExportProgressContainer(self) -> None:
        self._exportProgressContainer = QtWidgets.QWidget()
        self._exportProgressContainer.setLayout(QtWidgets.QGridLayout())

        self._exportProgressBar = QtWidgets.QProgressBar()
        self._exportProgressBar.setMaximum(100)
        self._exportProgressBar.setMinimum(0)

        self._exportProgressContainer.layout().addWidget(
            QtWidgets.QLabel("Export progress:"), 3, 0
        )
        self._exportProgressContainer.layout().addWidget(
            self._exportProgressBar, 4, 0, 1, 2
        )
        self._exportProgressContainer.setEnabled(False)

    def _initDataYamlContainer(self) -> None:
        self._dataYamlContainer = QtWidgets.QWidget()
        self._dataYamlContainer.setMaximumWidth(300)
        self._dataYamlContainer.setLayout(QtWidgets.QGridLayout())

        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("data.yaml"), 0, 0)
        spacer = QtWidgets.QWidget()
        spacer.setMinimumHeight(10)
        self._dataYamlContainer.layout().addWidget(spacer, 1, 0)

        self._dataYamlPathLineEdit = QtWidgets.QLineEdit()
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("path:"), 2, 0)
        self._dataYamlContainer.layout().addWidget(self._dataYamlPathLineEdit, 2, 1)

        self._dataYamlTrainLineEdit = QtWidgets.QLineEdit()
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("train:"), 3, 0)
        self._dataYamlContainer.layout().addWidget(self._dataYamlTrainLineEdit, 3, 1)

        self._dataYamlValLineEdit = QtWidgets.QLineEdit()
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("val:"), 4, 0)
        self._dataYamlContainer.layout().addWidget(self._dataYamlValLineEdit, 4, 1)

        self._dataYamlTestLineEdit = QtWidgets.QLineEdit()
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("test:"), 5, 0)
        self._dataYamlContainer.layout().addWidget(self._dataYamlTestLineEdit, 5, 1)

        self.labelSelectorTreeView = LabelSelectorTreeView(SharedValues().labelsDict)
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("names:"), 6, 0)

        self._dataYamlContainer.layout().addWidget(
            self.labelSelectorTreeView, 7, 0, 1, 2
        )

    @Slot()
    def btnImport_slot(self) -> None:
        """Open OS dialog window to choose a directory from which a dataset will be imported"""
        textPath = QtWidgets.QFileDialog().getExistingDirectory(
            self, "Select a Folder", "", QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        if textPath == "":
            return
        else:
            self._importPathTextEdit.setText(textPath)
            self.dataYamlPath = None

            self.loadDataset()

    @Slot()
    def btnExportDialog_slot(self) -> None:
        """Opens OS dialog window to choose a directory to which a dataset will be exported"""
        textPath = QtWidgets.QFileDialog().getExistingDirectory(
            self, "Select a Folder", "", QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        self._exportPathTextEdit.setText(textPath)

    @Slot()
    def btnExport_slot(self) -> None:
        """Qt slot for starting export"""
        exportPath = Path(SharedValues().datasetExportPath)

        if SharedValues().datasetExportPath == "":
            newExportPath = Path(SharedValues().datasetImportPath).parent / "exported"
            os.makedirs(newExportPath, exist_ok=True)
            # SharedValues().datasetExportPath = _exportPathTextEdit.text() called automatically
            self._exportPathTextEdit.setText(str(newExportPath.resolve()))
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

    def loadDataset(self) -> None:
        """Loads `ImageDataset` from"""

        SharedValues().imageSamples.clear()
        self.imageDataset.loadImageSamples(
            SharedValues().datasetImportPath,
            SharedValues().imageSamples,
            SharedValues().labelsDict,
        )
        self.updateDataYaml()

        self.datasetTreeView.loadSamplesFull()

    def updateDataYaml(self) -> None:
        """
        Updates values of `data.yaml` based on `SharedValues().datasetImportPath` and loads all
        class indexes and labels from data.yaml
        """
        path = Path(SharedValues().datasetImportPath)

        self._dataYamlPathLineEdit.setText(path.name)
        self._dataYamlValLineEdit.setText("images/val")
        self._dataYamlTrainLineEdit.setText("images/train")
        self._dataYamlTestLineEdit.setText("# not used")

        if self.imageDataset.dataYamlPath is None:
            return

        with open(self.imageDataset.dataYamlPath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for index, name in data["names"].items():
            SharedValues().labelsDict[index] = LabelEntry(name, index, None)

        self.labelSelectorTreeView.loadLabels()

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
            applyFilters=self._applyFiltersCheckBox.isChecked(),
            separateByClasses=self._separateByClassesCheckBox.isChecked(),
            generateNameFromClass=self._generateNameCheckBox.isChecked(),
            trainDataPercentage=self._trainDataPercentageSpinBox.value(),
        )
        self.worker.moveToThread(self.workerThread)

        self.workerThread.started.connect(self.worker.run)
        self.worker.progress.connect(self.saveImageSamplesUpdate_slot)
        self.worker.finished.connect(self.saveImageSamplesDone_slot)

        self.worker.finished.connect(self.workerThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.workerThread.finished.connect(self.workerThread.deleteLater)

        self._exportProgressContainer.setEnabled(True)
        self._exportContainer.setEnabled(False)
        self._importContainer.setEnabled(False)
        self._dataYamlContainer.setEnabled(False)
        self.setParentEnabled_fn(False)

        self.workerThread.start()

    @Slot(int)
    def saveImageSamplesUpdate_slot(self, progress: int) -> None:
        self._exportProgressBar.setValue(progress)

    @Slot()
    def saveImageSamplesDone_slot(self) -> None:
        self._exportProgressContainer.setEnabled(False)
        self._exportContainer.setEnabled(True)
        self._importContainer.setEnabled(True)
        self._dataYamlContainer.setEnabled(True)
        self.setParentEnabled_fn(True)

    def _exportPathTextEditChanged_slot(self, text: str) -> None:
        SharedValues().datasetExportPath = text

    def _importPathTextEditChanged_slot(self, text: str) -> None:
        SharedValues().datasetImportPath = text

    def tabSelected(self) -> None:
        self.incorrectLabels = self.datasetTreeView.loadSamplesFull(
            restoreVerticalPosition=True
        )
        self.labelSelectorTreeView.loadLabels()
        self._btnExport.setDisabled(self.incorrectLabels)
        if self.incorrectLabels:
            self._btnExport.setText(
                "Start Export (disabled until default labels are replaced)"
            )
        else:
            self._btnExport.setText("Start Export")

    def tabClosed(self) -> None:
        pass
