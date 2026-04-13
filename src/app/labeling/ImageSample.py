"""
Module: ImageSample.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class representing images that contain image bitmaps and its labels. Also works like a bridge
    between `LabelBox` objects (data being saved into label files) and graphical `ImageLabelBox`
    objects.
"""

from __future__ import annotations
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .LabelEntry import LabelEntry

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QColor

from pathlib import Path
from datetime import datetime
import cv2 as cv

from .converters import Norm2Pixels, Pixels2Norm, Mat2QImage
from .LabelBox import LabelBox
from .LabelEntry import LabelEntry
from .ImageLabelBox import ImageLabelBox
from .Box import Box


class ImageSample:
    def __init__(
        self,
        rootPath: str,
        name: str,
        imagePath: str,
        labelPath: str | None,
        imageExt: str,
        labelExt: str | None,
        labelsDict: dict[int, LabelEntry],
        screenScaleText_fn: Callable[[], float],
    ) -> None:
        """
        :param rootPath: Full path to the root directory containing image and label of this ImageSample
        :type rootPath: str
        :param name: Name of image file
        :type name: str
        :param imagePath: Relative path to the image file from `rootPath`
        :type imagePath: str
        :param labelPath: Relative path to the label file from `rootPath`
        :type labelPath: str | None
        :param imageExt: Extension of image file
        :type imageExt: str
        :param labelExt: Extension of label file
        :type labelExt: str | None
        :param labelsDict: Dictionary containing class index as a key and class name as a value
        :type labelsDict: dict[int, LabelEntry]
        :param screenScaleText_fn: Callback function for scaling text based on window size and
        `ImageLabelBox` size
        :type screenScaleText_fn: Callable[[], float]
        """
        self.rootPath: str = rootPath
        self.name: str = name
        self.imagePath: str = imagePath
        self.labelPath: str | None = labelPath
        self.imageExt: str = imageExt
        self.labelExt: str | None = labelExt
        self._screenScaleText_fn = screenScaleText_fn
        self.labelsDict: dict[int, LabelEntry] = labelsDict

        self.labelBoxes: list[LabelBox] = []
        self.imageLabelBoxes: list[ImageLabelBox] = []
        self.cvImage: cv.Mat | None = None
        self.width: float = 0
        self.height: float = 0
        self._lastModified: datetime | None = None
        self._loaded = False
        self._loadedLabels = False
        self.isForValidation = False

    def _loadImageAndLabel(self, skipLabel: bool = False, skipImage: bool = False) -> None:
        """
        Opens image and its label file from `imagePath` and `labelPath`. Dimensions of image are
        stored in internal list of `LabelBoxes` `_labelBoxes`. Checks for existence of both files.
        If image does not exist an exception is raised. For non existing label file no exception is raised.
        """

        if not skipImage:
            imgPath = Path(self.rootPath) / self.imagePath / (self.name + self.imageExt)
            if imgPath.is_file():
                self.cvImage = cv.imread(imgPath.resolve()._str)  # type: ignore
                self.height, self.width = self.cvImage.shape[:2]  # type: ignore
            else:
                raise Exception(f"Error: Image file does not exist: {imgPath}")

        if not skipLabel and self.labelPath is not None and self.labelExt is not None:
            lblPath = Path(self.rootPath) / self.labelPath / (self.name + self.labelExt)
            if lblPath.is_file():
                lastModified = datetime.fromtimestamp(lblPath.stat().st_mtime)

                if self._lastModified is not None and lastModified < self._lastModified:
                    return

                try:
                    with open(lblPath, "r") as f:
                        lines = f.readlines()

                    self.labelBoxes.clear()

                    for line in lines:
                        parsed = [float(x) for x in line.split(" ")]
                        label = int(parsed[0])
                        x = parsed[1]
                        y = parsed[2]
                        w = parsed[3]
                        h = parsed[4]

                        x, y, w, h = Norm2Pixels(x, y, w, h, self.width, self.height)
                        self.labelBoxes.append(LabelBox(x, y, w, h, label))
                except:
                    raise Exception(f"Error: Label image exists but cannot be read: {lblPath}")
                self._loadedLabels = True

    def load(self, selectedColor: QColor, defaultColor: QColor) -> None:
        """
        Loads internal list of `LabelBox` objects into the list of `ImageLabelBox` objects.
        """
        if self._loaded:
            return

        self._loadImageAndLabel(skipLabel=False)

        if len(self.imageLabelBoxes) == 0:
            for label in self.labelBoxes:

                newLabel = ImageLabelBox(
                    Box(label.x, label.y, label.width, label.height),
                    label.label,
                    (self.labelsDict[label.label].name if (label.label >= 0) else "default"),
                    self._screenScaleText_fn,
                    self.rect(),
                    selectedColor=selectedColor,
                    defaultColor=defaultColor,
                )
                self.imageLabelBoxes.append(newLabel)

        self._loaded = True

    def unload(self, save: bool = False) -> None:
        """
        Unloads list of graphical items (`ImageLabelBox`), if `save` is set to `True` the changes
        will be stored in internal `_labelBoxes` and can later be stored into label file for this image.
        """
        if not self._loaded:
            return

        if save:
            self.labelBoxes.clear()

            for imageLabelBox in self.imageLabelBoxes:
                rect = imageLabelBox.rect()
                self.labelBoxes.append(
                    LabelBox(
                        rect.x(),
                        rect.y(),
                        rect.width(),
                        rect.height(),
                        imageLabelBox.label,
                    )
                )
            self._lastModified = datetime.now()

        self.imageLabelBoxes.clear()
        self._loadedLabels = False
        self.cvImage = None
        self._loaded = False

    def generatePathToFile(
        self,
        rootPath: str,
        separateByClass: bool,
        isImage: bool,
        hasher: None | cv.img_hash.AverageHash = None,
    ) -> Path:
        """Generates file and its full path from the rootPath"""
        if self.cvImage is None:  # load image and its labels
            self._loadImageAndLabel(skipLabel=False)

        className = self.getClassName()

        if hasher is not None:
            fileName = self.generateNameFromImage(className, hasher)
        else:
            fileName = self.name

        filePath = Path(rootPath)

        if separateByClass:
            filePath /= className

        filePath.mkdir(exist_ok=True)  # check if directory exists, if not create it

        if isImage:
            filePath /= fileName + self.imageExt
        else:
            if self.labelExt is None:
                self.labelExt = ".txt"
            filePath /= fileName + self.labelExt

        if filePath.exists():
            filePath = filePath.with_name(f"{filePath.stem}_1{filePath.suffix}")

        return filePath

    def save(
        self,
        exportImagePath: str,
        exportLabelPath: str,
        separateByClasses: bool = False,
        hasher: None | cv.img_hash.AverageHash = None,
    ) -> None:
        """
        Saves current `ImageSample` labels into label file based on `exportImagePath` and `exportLabelPath`.
        If parameters are not defined default values for from `self.imagePath` `and self.labelPath`
        will be used.
        """

        imagePath = self.generatePathToFile(
            exportImagePath, separateByClasses, isImage=True, hasher=hasher
        )

        if self.cvImage is not None:
            cv.imwrite(str(imagePath.resolve()), self.cvImage)
        else:
            print(f"Error: Failed to save image, self.cvImage was None. Try to continue exporting.")
            return

        if len(self.labelBoxes) > 0:  # labelBoxes loaded from first generatePathToFile()
            labelPath = self.generatePathToFile(
                exportLabelPath, separateByClasses, isImage=False, hasher=hasher
            )

            with open(labelPath, "w") as f:
                for labelBox in self.labelBoxes:
                    x, y, w, h = labelBox.getDimensionTuple()
                    x, y, w, h = Pixels2Norm(x, y, w, h, self.width, self.height)
                    f.write(f"{labelBox.label} {x} {y} {w} {h}\n")

    def reloadImageLabels(self) -> None:
        """Reloads all labels `ImageLabelBoxes` in current ImageSample"""
        for imageLabelBox in self.imageLabelBoxes:
            imageLabelBox.setLabel(
                imageLabelBox.label,
                (
                    self.labelsDict[imageLabelBox.label].name
                    if (imageLabelBox.label >= 0)
                    else "default"
                ),
            )

    def add(self, imageLabelBox: ImageLabelBox) -> None:
        self.imageLabelBoxes.append(imageLabelBox)

    def remove(self, imageLabelBox: ImageLabelBox) -> None:
        self.imageLabelBoxes.remove(imageLabelBox)

    def getCvImage(self) -> cv.Mat | None:
        if self.cvImage is None:
            self._loadImageAndLabel(skipLabel=True)

        return self.cvImage

    def rect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def setCvImage(self, image: cv.Mat) -> None:
        self.cvImage = image

    def getQPixmap(self) -> QPixmap:
        if self.cvImage is None:
            self._loadImageAndLabel(skipLabel=True)

        return QPixmap.fromImage(Mat2QImage(self.cvImage))

    def getFullImagePath(self) -> str:
        return (Path(self.rootPath) / self.imagePath).resolve()._str  # type: ignore

    def getFullLabelPath(self) -> str:
        if self.labelPath is not None:
            return (Path(self.rootPath) / self.labelPath).resolve()._str  # type: ignore
        else:
            return ""

    def generateNameFromImage(self, className: None | str, hasher: cv.img_hash.AverageHash) -> str:
        if className is None:
            className = self.getClassName()

        if self.cvImage is None:  # if image was not loaded, load it
            self._loadImageAndLabel(skipLabel=False)

        if self.cvImage is not None:
            hsh = hasher.compute(self.cvImage)
            hshHex = hsh.flatten().tobytes().hex()

            return f"{className}_{str(hshHex)}"
        else:
            print("ERROR: Image could not be loaded in generateNameFromImage()")
            return className

    def getClassName(self) -> str:
        """Returns class the dominant class in image sample in string format"""
        currentClass = self.getClass()

        if currentClass == -1:
            return "mixed"
        elif currentClass == -2:
            return "no_label"
        else:
            return self.labelsDict[currentClass].name

    def getClass(self) -> int:
        """
        Returns class the dominant class in image sample. Return `-2` on no label, or `-1` for mixed,
        or class index if there on
        """
        if not self._loadedLabels:
            self._loadImageAndLabel(skipLabel=False, skipImage=True)

        if len(self.labelBoxes) == 1:
            return self.labelBoxes[0].label
        elif len(self.labelBoxes) > 1:
            firstClass = self.labelBoxes[0].label
            for labelBox in self.labelBoxes:
                if firstClass != labelBox.label:
                    return -1
            return firstClass
        else:
            return -2
