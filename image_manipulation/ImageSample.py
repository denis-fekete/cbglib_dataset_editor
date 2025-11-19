from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QGraphicsScene

import cv2 as cv 
from pathlib import Path
import os
from datetime import datetime

from widgets import ImageLabelBox
from utils.convertors import *
from .LabelBox import LabelBox
from widgets.LabelSelectorTreeView import LabelEntry

class ImageSample():
    def __init__(self, rootPath: str, name: str, imagePath: str, labelPath: str, imageExt: str, labelExt: str, labelsDict: list[int, LabelEntry],handle_fn):
        self.rootPath: str = rootPath 
        self.name: str = name
        self.imagePath: str = imagePath
        self.labelPath: str = labelPath
        self.imageExt: str = imageExt
        self.labelExt: str = labelExt
        self._handle_fn = handle_fn
        self.labelsDict: dict[int, LabelEntry] = labelsDict

        self._labelBoxes: list[LabelBox] = []
        self.imageLabelBoxes: list[ImageLabelBox] = []
        self.cvImage: cv.Mat = None
        self.width: float = None
        self.height: float = None
        self._lastModified: datetime = None

    def _loadImageAndLabel(self, skipLabel: bool = False) -> None:
        """
        Opens image and its label file from `imagePath` and `labelPath`. Dimensions of image are 
        stored in internal list of `LabelBoxes` `_labelBoxes`. Checks for existence of both files. 
        If image does not exist an exception is raised. For non existing label file no exception is raised.
        """

        imgPath = Path(self.rootPath) / self.imagePath / (self.name + self.imageExt)
        if(imgPath.is_file()):
            self.cvImage = cv.imread(imgPath)
            self.height , self.width = self.cvImage.shape[:2]
        else:
            raise Exception(f"Error: Image file does not exist: {imgPath}")

        if(skipLabel or self.labelPath is None or self.labelExt is None):
            return
        
        lblPath = Path(self.rootPath) / self.labelPath  / (self.name + self.labelExt)
        if(lblPath.is_file()):
            lastModified = datetime.fromtimestamp(lblPath.stat().st_mtime)

            if(self._lastModified is not None and lastModified < self._lastModified):
                return
            
            try:
                with open(lblPath, 'r') as f:
                    lines = f.readlines()

                self._labelBoxes.clear()

                for line in lines:
                    parsed = [float(x) for x in line.split(" ")]
                    label = int(parsed[0])
                    x = parsed[1]
                    y = parsed[2]
                    w = parsed[3]
                    h = parsed[4]

                    x, y, w, h = Norm2Pixels(x, y, w, h, self.width, self.height)
                    self._labelBoxes.append(LabelBox(x, y, w, h, label))
            except:
                raise Exception(f"Error: Label image exists but cannot be read: {lblPath}")

    def load(self, selectedColor: QColor = None, defaultColor: QColor = None) -> None:
        """
        Loads internal list of `LabelBox` objects into the list of `ImageLabelBox` objects.
        """
        self._loadImageAndLabel(skipLabel=False)

        print(f"Loading ImageSample: {self.name}:")
        if(len(self.imageLabelBoxes) == 0):
            for label in self._labelBoxes:
                
                newLabel = ImageLabelBox(
                    QRectF(label.x, label.y, label.width, label.height), 
                    label.label, 
                    self.labelsDict[label.label].name if (label.label >= 0) else "default", 
                    self._handle_fn,
                    self.rect(),
                    selectedColor=selectedColor,
                    defaultColor=defaultColor)
                self.imageLabelBoxes.append(newLabel)
                print(f"\tsaved label:{label.label}, x:{label.x}, y:{label.y}, w:{label.width}, h:{label.height}")

    def unload(self, save: bool = False) -> None:
        """
        Unloads list of graphical items (`ImageLabelBox`), if `save` is set to `True` the changes 
        will be stored in internal `_labelBoxes` and can later be stored into label file for this image.
        """
        if(save):
            self._labelBoxes.clear()

            print(f"Unloading ImageSample: {self.name}:")
            for imageLabelBox in self.imageLabelBoxes:
                rect = imageLabelBox.rect()
                self._labelBoxes.append(LabelBox(rect.x(), rect.y(), rect.width(), rect.height(), imageLabelBox.label))
                print(f"\tsaved label:{imageLabelBox.label}, x:{rect.x()}, y:{rect.y()}, w:{rect.width()}, h:{rect.height()}")
            self._lastModified = datetime.now()

        self.imageLabelBoxes.clear()
        self.cvImage = None

    def save(self, exportImagePath: str = None, exportLabelPath: str = None) -> None:
        """
        Saves current `ImageSample` labels into label file based on `rootPath` and `labelPath`.
        """
        imagePath = exportImagePath if (exportImagePath is not None) else self.imagePath
        labelPath = exportLabelPath if (exportLabelPath is not None) else self.labelPath

        if (imagePath is None):
            raise Exception("Image path for saving ImageSample is not valid")
        if (labelPath is None):
            raise Exception("Label path for saving ImageSample is not valid")
        
        if(self.cvImage is None):
            self._loadImageAndLabel(skipLabel=False)

        fullImagePath = imagePath / (self.name + self.imageExt)
        cv.imwrite(fullImagePath, self.cvImage)

        labelExt = self.labelExt if (self.labelExt is not None) else ".txt"
        fullLabelPath = labelPath / (self.name + labelExt)

        with open(fullLabelPath, 'w') as f:
            for labelBox in self._labelBoxes:
                x, y, w, h = labelBox.getDimensionTuple()
                x, y, w, h = Pixels2Norm(x, y, w, h, 
                                        self.width, self.height)
                f.write(f"{labelBox.label} {x} {y} {w} {h}\n")

    def reloadImageLabels(self):
        """Reloads all labels `ImageLabelBoxes` in current ImageSample"""
        for imageLabelBox in self.imageLabelBoxes:
            imageLabelBox.setLabel(imageLabelBox.label, 
                                   self.labelsDict[imageLabelBox.label].name if (imageLabelBox.label >= 0) else "default")
        
    def add(self, imageLabelBox: ImageLabelBox) -> None:
        self.imageLabelBoxes.append(imageLabelBox)

    def remove(self, imageLabelBox: ImageLabelBox) -> None:
        self.imageLabelBoxes.remove(imageLabelBox)

    def getCvImage(self) -> cv.Mat:
        if(self.cvImage is None):
            self._loadImageAndLabel(skipLabel=True)

        return self.cvImage
    
    def rect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def setCvImage(self, image: cv.Mat):
        self.cvImage = image
    
    def getQPixmap(self) -> QPixmap:
        if(self.cvImage is None):
            self._loadImageAndLabel(skipLabel=True)

        return QPixmap.fromImage(Mat2QImage(self.cvImage))
    
    def getFullImagePath(self) -> str:
        return str(Path(self.rootPath) / self.imagePath)
    
    def getFullLabelPath(self) -> str:
        return str(Path(self.rootPath) / self.labelPath)