import sys
import os
from pathlib import Path
import random

import yaml

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QSizePolicy

from widgets import *
from image_manipulation import *

class DatasetLoader(QtWidgets.QWidget):
    def __init__(self, imageSamples, labelsDict: dict[int, LabelEntry], filterPresets : list[SyntheticImage], handle_fn):
        super().__init__()

        self.imageSamples: list[ImageSample] = imageSamples
        self.handle_fn = handle_fn
        self.labelsDict: dict[int, LabelEntry] = labelsDict
        self.filterPresets : list[SyntheticImage] = filterPresets
        self.dataYamlPath: str = None
        self.incorrectLabels: bool = True

        self._initUI()

    def _initUI(self):
        self.setLayout(QtWidgets.QGridLayout())
        
        self._initImportContainer()
        self._initExportContainer()
        self._initDataYamlContainer()

        self.layout().addWidget(self._importContainer, 0, 0)
        self.layout().addWidget(self._exportContainer, 1, 0)
        self.layout().addWidget(self._dataYamlContainer, 0, 1)

        self.importRootPath: str = None
        self.exportRootPath: str = None
        # TODO: debug only!
        self.importRootPath = r'C:\Users\denfe\Projects\pythonDevEnv\src\data\yolo_v8'
        self.exportRootPath = r'C:\Users\denfe\Projects\pythonDevEnv\src\data\exported'
        self._textImportRootPath.setText(self.importRootPath)
        self._textExportRootPath.setText(self.exportRootPath)
        
        self.loadImageSamples()

    def _initImportContainer(self):
        self._importContainer = QtWidgets.QWidget()
        self._importContainer.setLayout(QtWidgets.QGridLayout())
        labelImportRootPath = QtWidgets.QLabel("Path to import dataset from (subdirectories will be imported as well)")
        labelImportRootPath.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._textImportRootPath = QtWidgets.QLineEdit()

        self._btnImportDialog = QtWidgets.QPushButton("Import")
        self._btnImportDialog.clicked.connect(self.btnImport_slot)

        self.datasetTreeView = ImageSampleTreeView(self.imageSamples)

        self._importContainer.layout().addWidget(labelImportRootPath, 0, 0, 1, 2)
        self._importContainer.layout().addWidget(self._textImportRootPath, 1, 0)
        self._importContainer.layout().addWidget(self._btnImportDialog, 1, 1)
        self._importContainer.layout().addWidget(self.datasetTreeView, 2, 0, 1, 2)

    def _initExportContainer(self):
        self._exportContainer = QtWidgets.QWidget()
        self._exportContainer.setLayout(QtWidgets.QGridLayout())
        labelExportRootPath = QtWidgets.QLabel("Path to export dataset to")
        labelExportRootPath.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._textExportRootPath = QtWidgets.QLineEdit()

        self._btnExportDialog = QtWidgets.QPushButton("Open")
        self._btnExportDialog.clicked.connect(self.btnExportDialog_slot)

        self._btnExport = QtWidgets.QPushButton("Start Export")
        self._btnExport.clicked.connect(self.btnExport_slot)

        self._exportContainer.layout().addWidget(labelExportRootPath, 0, 0, 1, 2)
        self._exportContainer.layout().addWidget(self._textExportRootPath, 1, 0)
        self._exportContainer.layout().addWidget(self._btnExportDialog, 1, 1)
        self._exportContainer.layout().addWidget(self._btnExport, 2, 0,)

    def _initDataYamlContainer(self):
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

        self.labelSelectorTreeView = LabelSelectorTreeView(self.labelsDict)
        self._dataYamlContainer.layout().addWidget(QtWidgets.QLabel("names:"), 6, 0)

        self._dataYamlContainer.layout().addWidget(self.labelSelectorTreeView, 7, 0, 1, 2)

    def btnImport_slot(self):
        """Open OS dialog window to choose a directory from which a dataset will be imported"""
        self.importRootPath = QtWidgets.QFileDialog().getExistingDirectory(
            self,
            "Select a Folder",
            "",
            QtWidgets.QFileDialog.Option.ShowDirsOnly
        )

        self.imageSamples.clear()
        self.dataYamlPath: str = None
        
        self.loadImageSamples()

    def btnExportDialog_slot(self):
        """Opens OS dialog window to choose a directory to which a dataset will be exported"""
        self.exportRootPath = QtWidgets.QFileDialog().getExistingDirectory(
            self,
            "Select a Folder",
            "",
            QtWidgets.QFileDialog.Option.ShowDirsOnly
        )

    def btnExport_slot(self):
        """Starts export process"""
        if(os.path.exists(self.exportRootPath)):
            if(not os.path.isdir(self.exportRootPath)):
                raise Exception("Error: Export root path exists and it is not directory")
        else:
            os.makedirs(self.exportRootPath)
        
        self.saveImageSamples()

    def loadImageSamples(self):
        """Clears `imageSamples` and loads new from `importRootPath`"""
        self.imageSamples.clear()
        
        fileDict = self.loadFilesDictionary()
        for item in fileDict:
            if(item["ext"] == ".jpg"):
                labels = []
                for _item in fileDict:
                    if(_item["ext"] == ".txt" and _item["name"] == item["name"]):
                        labels.append(_item)

                if(len(labels) > 1):
                    raise Exception(f"Multiple label (.txt) files found for one image (.jpg file): {labels}")
                
                label = labels[0] if len(labels) > 0 else None
                labelPath = label["filePath"] if (label is not None) else None
                labelExt = label["ext"] if (label is not None) else None

                self.imageSamples.append(ImageSample(
                    rootPath = self.importRootPath, 
                    name = item["name"], 
                    imagePath = item["filePath"], 
                    imageExt = item["ext"],
                    labelPath = labelPath,
                    labelExt = labelExt,
                    labelsDict = self.labelsDict, 
                    handle_fn = self.handle_fn))
                
                    
            elif(item["ext"] == ".yaml" and item["name"] == "data"):
                if(self.dataYamlPath is None):
                    self.dataYamlPath = Path(self.importRootPath) / item["filePath"] / (item["name"] + item["ext"])
                else:
                    raise Exception("Error: Found multiple data.yaml files. Only one or none (will get created automatically) should be in dataset!")
                
        self.loadDataYaml()
        self.datasetTreeView.loadSamplesFull()

    def loadDataYaml(self):
        """Loads dataset info such as label names and indexes from data.yaml """
        path = Path(self.importRootPath)
        self._dataYamlPathLineEdit.setText(path.name)
        self._dataYamlValLineEdit.setText("images/val")
        self._dataYamlTrainLineEdit.setText("images/train")
        self._dataYamlTestLineEdit.setText("# not used")
        
        if(self.dataYamlPath is None):
            return
        
        with open(self.dataYamlPath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for index, name in data["names"].items():
            self.labelsDict[index] = LabelEntry(name, index, None)

        self.labelSelectorTreeView.loadLabels()

    def loadFilesRaw(self, directoryPath):
        """
        Reads all file from directory path, sub directories will be called recursively and name 
        of subdirectory will be added to the name. Example:\n
        root
          |- subdirectoryA
          |---fileA
          |- fileB
        Will result in: 'fileB', 'subdirectoryA/fileA'
        """
        files = []
        path = Path(directoryPath)
        for item in os.listdir(directoryPath):
            if(os.path.isfile(path / item)):
                files.append(item)
                
            elif(os.path.isdir(path / item)):
                tmpFiles = self.loadFilesRaw(path / item)
                for dirItem in tmpFiles:
                    files.append(item + r'/' + dirItem)
            else:
                raise Exception("Unknown file/directory format")
        return files
    
    def loadFilesDictionary(self):
        """Returns list of dictionaries containing name, path and extension"""
        rawFiles = self.loadFilesRaw(self.importRootPath)

        fileDict = []
        for file in rawFiles:
            fullPath: Path = Path(self.importRootPath) / file
            filePath = str(Path(file).parent)
            fileName = fullPath.stem
            ext = fullPath.suffix

            fileDict.append({"name": fileName, "filePath": filePath, "ext": ext})

        return fileDict

    def saveImageSamples(self):
        """Saves images to the `exportRootPath`"""
        rootPath = Path(self.exportRootPath)
        imagesPath = rootPath / "images"
        trainImagesPath = imagesPath / "train"
        valImagesPath = imagesPath / "val"

        labelsPath = rootPath / "labels"
        trainLabelPath = labelsPath / "train"
        valLabelPath = labelsPath / "val"

        os.makedirs(imagesPath, exist_ok=True)
        os.makedirs(trainImagesPath, exist_ok=True)
        os.makedirs(valImagesPath, exist_ok=True)
        os.makedirs(labelsPath, exist_ok=True)
        os.makedirs(trainLabelPath, exist_ok=True)
        os.makedirs(valLabelPath, exist_ok=True)

        namesDict = {}
        for label in self.labelsDict.values():
            namesDict[label.index] = label.name

        dataYaml = {
            "filePath": rootPath.name,
            "train": "images/train",
            "val": "images/val",
            # "test": "# not used",
            "names" : namesDict
        }

        with open(rootPath / "data.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(dataYaml, f, sort_keys=False)

        trainImageSamples = []
        valImageSamples = []
        VALIDATION_THRESHOLD_PERCENT = 30
        VALIDATION_THRESHOLD_MAX = 20

        for imageSample in self.imageSamples:
            
            if(random.randint(0, 100) < VALIDATION_THRESHOLD_PERCENT and 
               len(valImageSamples) <= VALIDATION_THRESHOLD_MAX):
                valImageSamples.append(imageSample)
            else:
                trainImageSamples.append(imageSample)

        sFilter = SyntheticImage()
        for imageSample in trainImageSamples:
            imageSample: ImageSample = imageSample
            imageSample.save(exportImagePath=trainImagesPath,
                             exportLabelPath=trainLabelPath)
            for preset in self.filterPresets:
                sFilter.setReference(imageSample)
                sFilter.filter = preset
                sFilter.save(trainImagesPath, trainLabelPath)
            

        for imageSample in valImageSamples:
            imageSample: ImageSample = imageSample
            imageSample.save(exportImagePath=valImagesPath,
                             exportLabelPath=valLabelPath)
            for preset in self.filterPresets:
                sFilter.setReference(imageSample)
                sFilter.filter = preset
                sFilter.save(trainImagesPath, trainLabelPath)

    def tab_selected(self):
        self.incorrectLabels = self.datasetTreeView.loadSamplesFull(restoreVerticalPosition=True)
        self.labelSelectorTreeView.loadLabels()
        self._btnExport.setDisabled(self.incorrectLabels)
        if(self.incorrectLabels):
            self._btnExport.setText("Start Export (disabled until default labels are replaced)")
        else:
            self._btnExport.setText("Start Export")

    def tab_closed(self):
        pass