"""
Module: SyntheticImage.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class that works with OpenCV image and applies filters to it.
"""

from PySide6.QtCore import QRectF, Slot
from PySide6.QtGui import QPixmap

import numpy as np

import cv2 as cv
from cv2.typing import MatLike
from typing import Callable

from app.widgets import *
from app.labeling import *
from .FilterPreset import FilterPreset


class SyntheticImage:
    def __init__(self, invalidate_fn: Callable[[], None] | None = None) -> None:
        self.imageReference: ImageSample | None = None
        self.filter: FilterPreset | None = None
        self.invalidate_fn: Callable[[], None] | None = invalidate_fn
        self.cvImage: cv.Mat | None = None

        self.scale = 1.0
        self.padX: int = 0
        self.padY: int = 0
        self.updateReference()

    def generateFilterName(self, hasher: None | cv.img_hash.AverageHash = None) -> str:
        if self.filter.name == "default" or self.filter.name == "":
            fileName = f"_vf{self.filter.vFlip}_hf{self.filter.hFlip}"
            fileName += (
                f"_bl{self.filter.blur}_br{self.filter.brightness}_con{self.filter.contrast}"
            )
            fileName += f"_sat{self.filter.saturation}"
            fileName += f"_spn{self.filter.sapNoise}_gn{self.filter.gaussianNoise}"
            fileName = ".$f$_" + fileName
        else:
            fileName = ".$f$_" + self.filter.name

        return fileName

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

        if self.imageReference is None:
            return

        imagePath = self.imageReference.generatePathToFile(
            exportImagePath, separateByClasses, isImage=True, hasher=hasher, forceLabelLoad=True
        )

        filterName = self.generateFilterName(hasher)
        imagePath = imagePath.with_name(f"{imagePath.stem}{filterName}{imagePath.suffix}")

        if imagePath.exists():
            imagePath = imagePath.with_name(f"{imagePath.stem}_1{imagePath.suffix}")

        if self.cvImage is None:
            self.applyFilter()

        cv.imwrite(str(imagePath.resolve()), self.cvImage)  # type: ignore

        # labelBoxes loaded from first generatePathToFile()
        if len(self.imageReference.labelBoxes) > 0:
            labelPath = self.imageReference.generatePathToFile(
                exportLabelPath, separateByClasses, isImage=False, hasher=hasher
            )
            labelPath = labelPath.with_name(f"{labelPath.stem}{filterName}{labelPath.suffix}")

            if labelPath.exists():
                labelPath = labelPath.with_name(f"{labelPath.stem}_1{labelPath.suffix}")

            with open(labelPath, "w") as f:
                for labelBox in self.imageReference.labelBoxes:
                    x, y, w, h = labelBox.getDimensionTuple()
                    if self.filter.hFlip:
                        x = self.imageReference.width - x
                    if self.filter.vFlip:
                        y = self.imageReference.height - y

                    x, y, w, h = Pixels2Norm(
                        x * self.scale + self.padX,
                        y * self.scale + self.padY,
                        w * self.scale,
                        h * self.scale,
                        self.width(),
                        self.height(),
                    )

                    f.write(f"{labelBox.label} {x} {y} {w} {h}\n")

    def unload(self) -> None:
        self.cvImage = None

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
        if self.filter.forceResolution:
            return QRectF(0, 0, self.filter.resolution, self.filter.resolution)
        else:
            return QRectF(0, 0, self.imageReference.width, self.imageReference.height)

    def width(self) -> float:
        if self.filter.forceResolution and self.cvImage is not None:
            return self.cvImage.shape[1]
        else:
            return self.imageReference.width

    def height(self) -> float:
        if self.filter.forceResolution and self.cvImage is not None:
            return self.cvImage.shape[0]
        else:
            return self.imageReference.height

    def resizeImage(self, img: cv.Mat) -> MatLike:
        """
        Changes the resolution of image based on the filter.resolution. This will not force both
        resolutions and result in deformation of image, instead a image will be scaled by the bigger
        dimension. If filter.applyLetterbox is set, aspect ratio of 1:1 will be force and image will
        be padded with filters.paddingRed/Blue/Green values or with static noise
        """
        srcH = img.shape[0]
        srcW = img.shape[1]

        self.scale = self.filter.resolution / max(srcH, srcW)
        newW, newH = int(srcW * self.scale), int(srcH * self.scale)
        resized = cv.resize(img, (newW, newH))

        return resized

    def letterbox(self, img: MatLike) -> MatLike:
        """Applied letter-boxing to input image"""
        h = img.shape[0]
        w = img.shape[1]

        self.padX = (self.filter.resolution - w) // 2
        self.padY = (self.filter.resolution - h) // 2

        padded = cv.copyMakeBorder(
            img,
            self.padY,
            self.filter.resolution - h - self.padY,
            self.padX,
            self.filter.resolution - w - self.padX,
            cv.BORDER_CONSTANT,
            value=(
                self.filter.paddingRed,
                self.filter.paddingGreen,
                self.filter.paddingBlue,
            ),
        )
        return padded

    def photometricFilters(self, img: cv.Mat | MatLike) -> MatLike:
        # apply contrast and brightness
        img = cv.convertScaleAbs(img, alpha=self.filter.contrast / 100, beta=self.filter.brightness)

        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # apply saturation
        h, s, v = cv.split(img)

        s = cv.multiply(s, self.filter.saturation / 100.0)  # type: ignore
        s = cv.min(s, 255)  # type: ignore

        img = cv.merge([h, s, v])  # type: ignore
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)

        return img

    def generateSapNoise(self, img: cv.Mat | MatLike) -> MatLike:
        width, height = self.width(), self.height()
        noisePixels = int((self.filter.sapNoise / 10.0) * (width * height / 100))
        noiseRows = np.random.randint(0, int(height) - 1, noisePixels)
        noiseCols = np.random.randint(0, int(width) - 1, noisePixels)

        img[noiseRows, noiseCols] = 255

        noiseRows = np.random.randint(0, int(height) - 1, noisePixels)
        noiseCols = np.random.randint(0, int(width) - 1, noisePixels)

        img[noiseRows, noiseCols] = 0
        return img

    def generateGaussianNoise(self, img: cv.Mat | MatLike) -> MatLike:
        img = img.astype(np.float32)
        noiseMask = np.random.normal(  # type: ignore
            0, self.filter.gaussianNoise / 10.0, img.shape
        ).astype(
            np.float32
        )  # type: ignore
        img += noiseMask  # type: ignore
        img = np.clip(img, 0, 255).astype(np.uint8)  # type: ignore
        return img

    def applyFilter(self) -> None:
        """
        Applies `FilterPreset` onto the `ImageSample` from `self.imageReference`. Upon applying
        filters sets `self.cvImage` and calls `self.invalidate_fn` invalidating QGraphicsScene
        showing `SyntheticImage`
        """
        if self.imageReference is None or self.filter is None:
            return

        img: cv.Mat | None | MatLike = self.imageReference.getCvImage()

        if img is None:
            return

        if self.filter.forceResolution:
            img = self.resizeImage(img)
            # update self.cvImage as it is used for dimensions later
            self.cvImage = img  # type: ignore
        else:
            self.scale = 1.0
            self.padX = 0
            self.padY = 0

        img = self.photometricFilters(img)

        # apply blur
        if self.filter.blur > 0:
            blurValue = self.filter.blur if (self.filter.blur % 2 == 1) else self.filter.blur + 1
            img = cv.GaussianBlur(img, (blurValue, blurValue), 0)

        if self.filter.sapNoise > 0:
            img = self.generateSapNoise(img)

        if self.filter.gaussianNoise > 0:
            img = self.generateGaussianNoise(img)

        if self.filter.hFlip and self.filter.vFlip:
            img = cv.flip(img, -1)
        else:
            if self.filter.hFlip:
                img = cv.flip(img, 1)
            if self.filter.vFlip:
                img = cv.flip(img, 0)

        if self.filter.applyLetterbox:
            img = self.letterbox(img)

        self.cvImage = img  # type: ignore

        if self.invalidate_fn is not None:
            self.invalidate_fn()

    @Slot(int)
    def blurChanged(self, value: int) -> None:
        self.filter.blur = value

    @Slot(int)
    def saturationChanged(self, value: int) -> None:
        self.filter.saturation = value

    @Slot(int)
    def brightnessChanged(self, value: int) -> None:
        self.filter.brightness = value

    @Slot(int)
    def contrastChanged(self, value: int) -> None:
        self.filter.contrast = value

    @Slot(int)
    def sapNoiseChanged(self, value: int) -> None:
        self.filter.sapNoise = value

    @Slot(int)
    def gaussianChanged(self, value: int) -> None:
        self.filter.gaussianNoise = value

    @Slot(bool)
    def hFlipChanged(self, checked: bool) -> None:
        self.filter.hFlip = checked
        self.applyFilter()

    @Slot(bool)
    def vFlipChanged(self, checked: bool) -> None:
        self.filter.vFlip = checked
        self.applyFilter()
