"""
Module: ExportWorker.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class derived from QObject that is used for multi-threaded exporting of images and labels.
"""

from PySide6.QtCore import QObject, Signal, Slot

import cv2 as cv
from pathlib import Path

from app.labeling.ImageSample import ImageSample
from app.synthetic.FilterPreset import FilterPreset
from app.synthetic.SyntheticImage import SyntheticImage


class ExportWorker(QObject):
    def __init__(
        self,
        imageSamples: list[ImageSample],
        filterPresets: list[FilterPreset],
        trainImagesPath: Path,
        trainLabelsPath: Path,
        valImagesPath: Path,
        valLabelsPath: Path,
        generateSynthetic: bool,
        separateByClasses: bool,
        generateNameFromClass: bool,
        exportOriginal: bool,
    ) -> None:
        super().__init__()
        self.imageSamples = imageSamples
        self.filterPresets = filterPresets
        self.trainImagesPath = trainImagesPath
        self.trainLabelsPath = trainLabelsPath
        self.valImagesPath = valImagesPath
        self.valLabelsPath = valLabelsPath
        self.applyFilters = generateSynthetic
        self.separateByClasses = separateByClasses
        self.generateNameFromClass = generateNameFromClass
        self.exportOriginal = exportOriginal

        self.sFilter: SyntheticImage | None = None

    progress = Signal()
    finished = Signal()

    @Slot()
    def run(self) -> None:
        # create hasher
        if self.generateNameFromClass:
            self.hasher = cv.img_hash.AverageHash().create()
        else:
            self.hasher = None

        # export train data with synthetic data
        self.sFilter = SyntheticImage()
        for imageSample in self.imageSamples:
            if imageSample.isForTraining:
                self._exportSample(
                    imageSample,
                    self.trainImagesPath,
                    self.trainLabelsPath,
                    self.applyFilters,
                )
            else:
                self._exportSample(imageSample, self.valImagesPath, self.valLabelsPath, False)

        self.finished.emit()

    def _exportSample(
        self,
        imageSample: ImageSample,
        imagePath: Path,
        labelPath: Path,
        applyFilters: bool,
    ) -> None:
        """Export single ImageSample"""
        if self.exportOriginal:
            imageSample.save(
                exportImagePath=str(imagePath.resolve()),
                exportLabelPath=str(labelPath.resolve()),
                separateByClasses=self.separateByClasses,
                hasher=self.hasher,
            )

        if applyFilters:
            for preset in self.filterPresets:
                self.sFilter.filter = preset
                self.sFilter.setReference(imageSample)
                self.sFilter.save(
                    str(imagePath.resolve()),
                    str(labelPath.resolve()),
                    self.separateByClasses,
                    hasher=self.hasher,
                )

        self.progress.emit()

        # unload image sample from memory
        imageSample.cvImage = None
