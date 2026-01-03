from PySide6.QtCore import QObject, Signal, Slot
from .ImageSample import ImageSample
from .FilterPreset import FilterPreset
from .SyntheticImage import SyntheticImage
from .LabelEntry import LabelEntry

import random
import os
import yaml
from pathlib import Path

class ExportWorker(QObject):
    VALIDATION_THRESHOLD_PERCENT = 30
    VALIDATION_THRESHOLD_MAX = 20

    def __init__(self, imageSamples: list[ImageSample], filterPresets : list[FilterPreset], labelsDict: dict[int, LabelEntry], exportRootPath: str):
        super().__init__()
        self.imageSamples = imageSamples
        self.filterPresets = filterPresets
        self.exportRootPath = exportRootPath
        self.labelsDict = labelsDict

    progress = Signal(int)
    finished = Signal()

    @Slot()
    def run(self):
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

        for imageSample in self.imageSamples:
            if(random.randint(0, 100) < self.VALIDATION_THRESHOLD_PERCENT and 
               len(valImageSamples) <= self.VALIDATION_THRESHOLD_MAX):
                valImageSamples.append(imageSample)
            else:
                trainImageSamples.append(imageSample)

        progressCnt = 0
        progressStep = 100 / (len(trainImageSamples) * len(self.filterPresets) + len(valImageSamples))

        sFilter = SyntheticImage()
        for imageSample in trainImageSamples:
            imageSample: ImageSample = imageSample
            imageSample.save(exportImagePath=trainImagesPath,
                             exportLabelPath=trainLabelPath)
            
            progressCnt = progressCnt + progressStep
            self.progress.emit(progressCnt)

            for preset in self.filterPresets:
                sFilter.filter = preset
                sFilter.setReference(imageSample)
                sFilter.save(trainImagesPath, trainLabelPath)

                progressCnt = progressCnt + progressStep
                self.progress.emit(progressCnt)

        for imageSample in valImageSamples:
            imageSample: ImageSample = imageSample
            imageSample.save(exportImagePath=valImagesPath,
                             exportLabelPath=valLabelPath)
            
            progressCnt = progressCnt + progressStep
            self.progress.emit(progressCnt)
    
        self.progress.emit(100)
        self.finished.emit()
