from PySide6.QtCore import QObject, Signal, Slot

import random
import os
import yaml
from pathlib import Path

from .ImageSample import ImageSample
from .FilterPreset import FilterPreset
from .SyntheticImage import SyntheticImage
from .LabelEntry import LabelEntry


class ExportWorker(QObject):
    VALIDATION_THRESHOLD_PERCENT = 30
    VALIDATION_THRESHOLD_MAX = 20

    def __init__(
        self,
        imageSamples: list[ImageSample],
        filterPresets: list[FilterPreset],
        labelsDict: dict[int, LabelEntry],
        exportRootPath: str,
        applyFilters: bool,
    ) -> None:
        super().__init__()
        self.imageSamples = imageSamples
        self.filterPresets = filterPresets
        self.exportRootPath = exportRootPath
        self.labelsDict = labelsDict
        self.applyFilters = applyFilters

    progress = Signal(int)
    finished = Signal()

    @Slot()
    def run(self) -> None:
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

        namesDict: dict[int, str] = {}
        for label in self.labelsDict.values():
            namesDict[label.index] = label.name

        dataYaml = {
            "filePath": rootPath.name,
            "train": "images/train",
            "val": "images/val",
            # "test": "# not used",
            "names": namesDict,
        }

        with open(rootPath / "data.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(dataYaml, f, sort_keys=False)

        trainImages: list[ImageSample] = []
        valImages: list[ImageSample] = []

        for imageSample in self.imageSamples:
            if (
                random.randint(0, 100) < self.VALIDATION_THRESHOLD_PERCENT
                and len(valImages) <= self.VALIDATION_THRESHOLD_MAX
            ):
                valImages.append(imageSample)
            else:
                trainImages.append(imageSample)

        progressCnt = 0
        if self.applyFilters:
            progressStep = 100 / (
                len(trainImages) * len(self.filterPresets) + len(valImages)
            )
        else:
            progressStep = 100 / (len(trainImages) + len(valImages))

        sFilter = SyntheticImage()
        for imageSample in trainImages:
            imageSample: ImageSample = imageSample
            imageSample.save(
                exportImagePath=trainImagesPath.resolve()._str,
                exportLabelPath=trainLabelPath.resolve()._str,
            )

            progressCnt = progressCnt + progressStep
            self.progress.emit(progressCnt)

            if self.applyFilters:
                for preset in self.filterPresets:
                    sFilter.filter = preset
                    sFilter.setReference(imageSample)
                    sFilter.save(
                        trainImagesPath.resolve()._str, trainLabelPath.resolve()._str
                    )

                    progressCnt = progressCnt + progressStep
                    self.progress.emit(progressCnt)

        for imageSample in valImages:
            imageSample: ImageSample = imageSample
            imageSample.save(
                exportImagePath=valImagesPath.resolve()._str,
                exportLabelPath=valLabelPath.resolve()._str,
            )

            progressCnt = progressCnt + progressStep
            self.progress.emit(progressCnt)

        self.progress.emit(100)
        self.finished.emit()
