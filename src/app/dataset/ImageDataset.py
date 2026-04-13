"""
Module: ImageDataset.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class for importing images and its associated label files as an correct ImageSamples that will
    be in application later on for exporting, labeling and creating synthetic data.
"""

import os
from pathlib import Path
from typing import Callable
import random
import yaml
import math

from PySide6 import QtCore
from PySide6.QtCore import QThread, Slot, Signal

from app.utils import SharedValues
from .ExportWorker import ExportWorker
from .ImportWorker import ImportWorker
from app.labeling import LabelEntry


class ImageDataset(QtCore.QObject):
    exportFinished = Signal()
    progressUpdate = Signal(float)
    importFinished = Signal()
    error = Signal(str)

    def __init__(self, screenScaleText_fn: Callable[[], float]) -> None:
        super().__init__()
        self.screenScaleText_fn: Callable[[], float] = screenScaleText_fn
        self.dataYamlPath: str | None = None

        self.eWorkers: list[ExportWorker] = []
        self.eWorkerThreads: list[QThread] = []
        self.progress = 0.0
        self.progressStep = 0.0

    def importDataset(
        self,
    ) -> None:
        """Clears `imageSamples` and loads new from `SharedValues().datasetImportPath`"""

        self.iWorker = ImportWorker(
            SharedValues().datasetImportPath,
            SharedValues().imageSamples,
            SharedValues().labelsDict,
            self.screenScaleText_fn,
        )

        self.iWorkerThread = QThread()
        self.iWorker.moveToThread(self.iWorkerThread)

        self.iWorkerThread.started.connect(self.iWorker.run)
        self.iWorker.progress.connect(self.progressUpdate)
        self.iWorker.finished.connect(self.importFinished)
        self.iWorker.dataYamlPathFound.connect(self.setDataYamlPath)
        self.iWorker.error.connect(self.error)

        self.iWorker.finished.connect(self.iWorkerThread.quit)
        self.iWorker.finished.connect(self.iWorker.deleteLater)
        self.iWorker.error.connect(self.iWorker.deleteLater)
        self.iWorker.error.connect(self.iWorkerThread.quit)
        self.iWorkerThread.finished.connect(self.iWorkerThread.deleteLater)

        self.iWorkerThread.start()

    def exportDataset(
        self,
        trainDataPercentage: int,
        numOfWorkers: int,
        genSyntheticTrain: bool,
        genSyntheticVal: bool,
        separateByClasses: bool,
        generateNameFromClass: bool,
        exportOriginal: bool,
    ) -> None:
        """Exports dataset into Ultralytics YOLO format with data.yaml"""

        self.exportYaml()
        self._separateIntoTraining(trainDataPercentage)

        self.numOfWorkers = numOfWorkers
        self.finishedWorkers = 0

        # calculate progress step for each image stored
        self.progressStep = 100.0 / len(SharedValues().imageSamples)

        # calculate work per worker
        samplesPerWorker = math.floor(len(SharedValues().imageSamples) / numOfWorkers)
        additionalSamples = len(SharedValues().imageSamples) % numOfWorkers

        self.progress = 0.0
        self.eWorkers = []  # reset threads and export workers
        self.eWorkerThreads = []

        indexStart = 0
        indexEnd = samplesPerWorker + additionalSamples  # add additional work to first
        for i in range(0, numOfWorkers):
            self.eWorkerThreads.append(QThread())
            worker = ExportWorker(
                imageSamples=SharedValues().imageSamples[indexStart:indexEnd],
                filterPresets=SharedValues().filterPresets,
                trainImagesPath=self.trainImagesPath,
                trainLabelsPath=self.trainLabelsPath,
                valImagesPath=self.valImagesPath,
                valLabelsPath=self.valLabelsPath,
                genSyntheticTrain=genSyntheticTrain,
                genSyntheticVal=genSyntheticVal,
                separateByClasses=separateByClasses,
                generateNameFromClass=generateNameFromClass,
                exportOriginal=exportOriginal,
            )
            self.eWorkers.append(worker)

            indexStart = indexEnd
            indexEnd = indexStart + samplesPerWorker

            self.eWorkers[i].moveToThread(self.eWorkerThreads[i])

            self.eWorkerThreads[i].started.connect(self.eWorkers[i].run)
            self.eWorkers[i].progress.connect(self.progressSampleFinished)
            self.eWorkers[i].finished.connect(self.workerFinished)

            self.eWorkers[i].finished.connect(self.eWorkerThreads[i].quit)
            self.eWorkers[i].finished.connect(self.eWorkers[i].deleteLater)
            self.eWorkerThreads[i].finished.connect(self.eWorkerThreads[i].deleteLater)

            self.eWorkerThreads[i].start()

    def exportYaml(self) -> None:
        """Exports data.yaml file from current values in SharedValues()"""
        rootPath = Path(SharedValues().datasetExportPath)
        imagesPath = rootPath / "images"
        self.trainImagesPath = imagesPath / "train"
        self.valImagesPath = imagesPath / "val"

        labelsPath = rootPath / "labels"
        self.trainLabelsPath = labelsPath / "train"
        self.valLabelsPath = labelsPath / "val"

        os.makedirs(imagesPath, exist_ok=True)
        os.makedirs(self.trainImagesPath, exist_ok=True)
        os.makedirs(self.valImagesPath, exist_ok=True)
        os.makedirs(labelsPath, exist_ok=True)
        os.makedirs(self.trainLabelsPath, exist_ok=True)
        os.makedirs(self.valLabelsPath, exist_ok=True)

        namesDict: dict[int, str] = {}
        for label in SharedValues().labelsDict.values():
            if label.index != -1:  # skip mixed
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

    def _separateIntoTraining(self, trainDataPercentage: int):
        """"""
        SharedValues().labelsDict[-1] = LabelEntry("mixed", -1)
        # update LabelsDict with ImageSamples by class
        for imageSample in SharedValues().imageSamples:
            sampleClass = imageSample.getClass()
            if sampleClass > -2:  # ignore no label images
                SharedValues().labelsDict[sampleClass].samples.append(imageSample)

        percent = trainDataPercentage / 100.0
        for entry in SharedValues().labelsDict.values():
            total = len(entry.samples)
            forTraining = math.ceil(total * percent)

            while len(entry.samples) > forTraining:
                randomSample = random.randint(0, len(entry.samples) - 1)
                trainingSample = entry.samples.pop(randomSample)
                trainingSample.isForValidation = True

            entry.samples.clear()

        SharedValues().labelsDict.pop(-1)  # delete mixed

    def calculateStatistics(self):
        """Calculate statistics of the `ImageDataset` and update `SharedValues().statistics`"""
        # reset labelDict count values
        for value in SharedValues().labelsDict.values():
            value.count = 0

        for sample in SharedValues().imageSamples:
            sample._loadImageAndLabel(skipLabel=False, skipImage=True)  # type: ignore
            boxes = len(sample.labelBoxes)

            if boxes == 0:
                SharedValues().statistics.emptySamples += 1
            else:
                SharedValues().statistics.labelBoxes += boxes

            for labelBox in sample.labelBoxes:
                SharedValues().labelsDict[labelBox.label].count += 1

    @Slot()
    def progressSampleFinished(self):
        self.progress += self.progressStep
        self.progressUpdate.emit(self.progress)

    @Slot()
    def setDataYamlPath(self, path: str):
        self.dataYamlPath = path

    @Slot()
    def workerFinished(self):
        self.finishedWorkers += 1

        if self.finishedWorkers == self.numOfWorkers:
            self.exportFinished.emit()
            self.progressUpdate.emit(100)
