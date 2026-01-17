from PySide6.QtCore import QRectF, Slot
from PySide6.QtGui import QPixmap

import numpy as np

import cv2 as cv
from cv2.typing import MatLike
from typing import Callable
from pathlib import Path

from app.widgets import *
from app.utils import *
from .ImageSample import ImageSample
from .FilterPreset import FilterPreset


class SyntheticImage:
    def __init__(self, invalidate_fn: Callable[[], None] | None = None) -> None:
        self.imageReference: ImageSample | None = None
        self.filter: FilterPreset = FilterPreset()
        self.invalidate_fn: Callable[[], None] | None = invalidate_fn
        self.cvImage: cv.Mat | None = None

        self.updateReference()

    def save(
        self,
        exportImagePath: str,
        exportLabelPath: str,
        separateByClasses: bool = False,
        hasher: None | cv.img_hash.AverageHash = None,
    ) -> None:
        """
        Saves current `FilterPreset` as an Image based on `exportImagePath` and `exportLabelPath`.
        """

        className = self.imageReference.getClassName()

        filterName = f"_vf{self.filter.vFlip}_hf{self.filter.hFlip}"
        filterName += f"_bl{self.filter.blur}_br{self.filter.brightness}_con{self.filter.contrast}"
        filterName += f"_sat{self.filter.saturation}"
        filterName += f"_spn{self.filter.sapNoise}_gn{self.filter.gaussianNoise}"
        filterName = "_$f$_" + filterName

        fullImagePath = Path(exportImagePath)

        if separateByClasses:
            fullImagePath /= className

        fullImagePath.mkdir(exist_ok=True)

        if hasher is not None:
            fullImagePath /= (
                self.imageReference.generateNameFromImage(className, hasher)
                + filterName
                + self.imageReference.imageExt
            )
        else:
            fullImagePath /= (
                self.imageReference.name + filterName + self.imageReference.imageExt
            )

        cv.imwrite(fullImagePath.resolve()._str, self.cvImage)

        labelExt = (
            self.imageReference.labelExt
            if (self.imageReference.labelExt is not None)
            else ".txt"
        )
        fullLabelPath = Path(exportLabelPath)

        if separateByClasses:
            fullLabelPath /= className

        if hasher is not None:
            fullLabelPath /= (
                self.imageReference.generateNameFromImage(className, hasher)
                + filterName
                + labelExt
            )
        else:
            fullLabelPath /= self.imageReference.name + filterName + labelExt

        width = self.imageReference.width
        height = self.imageReference.height

        with open(fullLabelPath, "w") as f:
            for labelBox in self.imageReference.labelBoxes:
                x, y, w, h = labelBox.getDimensionTuple()

                if self.filter.hFlip:
                    x = width - x
                if self.filter.vFlip:
                    y = height - y

                x, y, w, h = Pixels2Norm(x, y, w, h, width, height)

                f.write(f"{labelBox.label} {x} {y} {w} {h}\n")

    def getCvImage(self) -> cv.Mat | None:
        if self.cvImage is None:
            self.updateReference()

        return self.cvImage

    def updateReference(self) -> None:
        """Updates internal `cvImage` based on `imageReference`"""
        if self.imageReference is not None:
            self.cvImage = self.imageReference.getCvImage()

    def getQPixmap(self) -> QPixmap:
        if self.cvImage is None:
            self.updateReference()

        return QPixmap.fromImage(Mat2QImage(self.cvImage))

    def setReference(self, reference: ImageSample):
        """Sets reference `ImageSample` and reapplies filter"""
        self.imageReference = reference
        self.applyFilter()

    def rect(self) -> QRectF:
        return QRectF(0, 0, self.imageReference.width, self.imageReference.height)

    def width(self) -> float:
        return self.imageReference.width

    def height(self) -> float:
        return self.imageReference.height

    def applyFilter(self) -> None:
        """
        Applies `FilterPreset` onto the `ImageSample` from `self.imageReference`. Upon applying
        filters sets `self.cvImage` and calls `self.invalidate_fn` invalidating QGraphicsScene
        showing `SyntheticImage`
        """
        if self.imageReference is None:
            return

        original: cv.Mat | None = self.imageReference.getCvImage()

        if original is None:
            return

        # apply contrast and brightness
        img: MatLike = cv.convertScaleAbs(
            original, alpha=self.filter.contrast / 100, beta=self.filter.brightness
        )

        img: MatLike = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # apply saturation
        h, s, v = cv.split(img)

        s = cv.multiply(s, self.filter.saturation / 100.0)  # type: ignore
        s = cv.min(s, 255)  # type: ignore

        img = cv.merge([h, s, v])  # type: ignore
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)

        # apply blur
        if self.filter.blur > 0:
            blurValue = (
                self.filter.blur
                if (self.filter.blur % 2 == 1)
                else self.filter.blur + 1
            )
            img = cv.medianBlur(img, blurValue)

        # start here
        if self.filter.sapNoise > 0:
            width, height = self.width(), self.height()
            noisePixels = int(self.filter.sapNoise * (width * height / 100))
            noiseRows = np.random.randint(0, int(height) - 1, noisePixels)
            noiseCols = np.random.randint(0, int(width) - 1, noisePixels)

            img[noiseRows, noiseCols] = 255

            noiseRows = np.random.randint(0, int(height) - 1, noisePixels)
            noiseCols = np.random.randint(0, int(width) - 1, noisePixels)

            img[noiseRows, noiseCols] = 0

        if self.filter.gaussianNoise > 0:
            img = img.astype(np.float32)
            noiseMask = np.random.normal(  # type: ignore
                0, self.filter.gaussianNoise, img.shape
            ).astype(
                np.float32
            )  # type: ignore
            img += noiseMask  # type: ignore
            img = np.clip(img, 0, 255).astype(np.uint8)  # type: ignore

        if self.filter.hFlip and self.filter.vFlip:
            img = cv.flip(img, -1)
        else:
            if self.filter.hFlip:
                img = cv.flip(img, 1)
            if self.filter.vFlip:
                img = cv.flip(img, 0)

        self.cvImage = img  # type: ignore

        if self.invalidate_fn is not None:
            self.invalidate_fn()

    @Slot(int)
    def blurSliderChanged_slot(self, value: int) -> None:
        self.filter.blur = value

    @Slot(int)
    def saturationSliderChanged_slot(self, value: int) -> None:
        self.filter.saturation = value

    @Slot(int)
    def brightnessSliderChanged_slot(self, value: int) -> None:
        self.filter.brightness = value

    @Slot(int)
    def contrastSliderChanged_slot(self, value: int) -> None:
        self.filter.contrast = value

    @Slot(int)
    def sapNoiseSliderChanged_slot(self, value: int) -> None:
        self.filter.sapNoise = value

    @Slot(int)
    def gaussianNoiseSliderChanged_slot(self, value: int) -> None:
        self.filter.gaussianNoise = value

    @Slot(bool)
    def horizontalFlipCheckboxChanged_slot(self, checked: bool) -> None:
        self.filter.hFlip = checked
        self.applyFilter()

    @Slot(bool)
    def verticalFlipCheckboxChanged_slot(self, checked: bool) -> None:
        self.filter.vFlip = checked
        self.applyFilter()
