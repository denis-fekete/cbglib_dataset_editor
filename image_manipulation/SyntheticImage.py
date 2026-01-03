from pathlib import Path
import os
from datetime import datetime
import numpy as np

import cv2 as cv 

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QColor

from widgets import *
from utils import *
from .ImageSample import ImageSample
from .FilterPreset import FilterPreset


class SyntheticImage():
    def __init__(self, invalidate_fn=None):
        self.imageReference: ImageSample = None
        self.filter = FilterPreset()
        self.invalidate_fn = invalidate_fn
        self.updateReference()
        
    def save(self, exportImagePath: str = None, exportLabelPath: str = None) -> None:
        """
        Saves current `ImageFilter` file based on `exportImagePath` and `exportLabelPath`. 
        If parameters are not defined default values for from `self.imagePath` `and self.labelPath` 
        will be used.
        """

        if (exportImagePath is None):
            raise Exception("Image path for saving ImageSample is not valid")
        if (exportLabelPath is None):
            raise Exception("Label path for saving ImageSample is not valid")
        
        if(self.cvImage is None):
            self._loadImageAndLabel(skipLabel=False)

        filterName = f"_vf{self.filter.vFlip}_hf{self.filter.hFlip}"
        filterName += f"_bl{self.filter.blur}_br{self.filter.brightness}_con{self.filter.contrast}"
        filterName += f"_sat{self.filter.saturation}"
        filterName += f"_spn{self.filter.sapNoise}_gn{self.filter.gaussianNoise}"

        # fileName = self.imageReference.name + "_filters_" + filterName;
        fileName = self.imageReference.name + "_filters_" + self.filter.name;
        fullImagePath = exportImagePath / (fileName + self.imageReference.imageExt)
        cv.imwrite(fullImagePath, self.cvImage)

        labelExt = self.imageReference.labelExt if (self.imageReference.labelExt is not None) else ".txt"
        fullLabelPath = exportLabelPath / (fileName + labelExt)

        width = self.imageReference.width
        height = self.imageReference.height

        with open(fullLabelPath, 'w') as f:
            for labelBox in self.imageReference._labelBoxes:
                x, y, w, h = labelBox.getDimensionTuple()
                
                if(self.filter.hFlip):
                    x = width - x
                if(self.filter.vFlip):
                    y = height - y

                x, y, w, h = Pixels2Norm(x, y, w, h, 
                                        width, height)
                

                f.write(f"{labelBox.label} {x} {y} {w} {h}\n")

    def getCvImage(self) -> cv.Mat:
        if(self.cvImage is None):
            self.updateReference()

        return self.cvImage
    
    def updateReference(self):
        """Updates internal `cvImage` based on `imageReference`"""
        if(self.imageReference is not None):
            self.cvImage = self.imageReference.getCvImage()

    def getQPixmap(self) -> QPixmap:
        if(self.cvImage is None):
            self.updateReference()

        return QPixmap.fromImage(Mat2QImage(self.cvImage))
    
    def setReference(self, reference: ImageSample):
        self.imageReference = reference
        self.updateReference()
        self.applyFilter()

    def rect(self) -> QRectF:
        return QRectF(0, 0, self.imageReference.width, self.imageReference.height)

    def width(self) -> float:
        return self.imageReference.width
    
    def height(self) -> float:
        return self.imageReference.height
    
    def applyFilter(self):
        if(self.imageReference is None):
            return
        
        original = self.imageReference.getCvImage()

        # apply contrast and brightness
        img = cv.convertScaleAbs(original, alpha=self.filter.contrast / 100, beta=self.filter.brightness)

        
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # apply saturation
        h, s, v = cv.split(img)
        s = cv.multiply(s, self.filter.saturation / 100)
        s = cv.min(s, 255)
        img = cv.merge([h, s, v])
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)

        # apply blur
        if(self.filter.blur > 0):
            blurValue = self.filter.blur if (self.filter.blur % 2 == 1) else self.filter.blur + 1
            img = cv.medianBlur(img, blurValue)

        if(self.filter.sapNoise > 0):
            w, h = self.width(), self.height()
            noisePixels = int(self.filter.sapNoise * (w * h / 100))
            noiseRows = np.random.randint(0, h-1, noisePixels)
            noiseCols = np.random.randint(0, w-1, noisePixels)

            img[noiseRows, noiseCols] = 255

            noiseRows = np.random.randint(0, h-1, noisePixels)
            noiseCols = np.random.randint(0, w-1, noisePixels)

            img[noiseRows, noiseCols] = 0

        if(self.filter.gaussianNoise > 0):
            img = img.astype(np.float32)
            noiseMask = np.random.normal(0, self.filter.gaussianNoise, img.shape).astype(np.float32)
            img += noiseMask
            img = np.clip(img, 0, 255).astype(np.uint8)


        if(self.filter.hFlip and self.filter.vFlip):
            img = cv.flip(img, -1)
        else:
            if(self.filter.hFlip):
                img = cv.flip(img, 1)
            if(self.filter.vFlip):
                img = cv.flip(img, 0)

        self.cvImage = img
        
        if(self.invalidate_fn is not None):
            self.invalidate_fn()
        
    def blurSliderChanged_slot(self, value):
        self.filter.blur = value

    def saturationSliderChanged_slot(self, value):
        self.filter.saturation = value

    def brightnessSliderChanged_slot(self, value):
        self.filter.brightness = value

    def contrastSliderChanged_slot(self, value):
        self.filter.contrast = value

    def sapNoiseSliderChanged_slot(self, value):
        self.filter.sapNoise = value

    def gaussianNoiseSliderChanged_slot(self, value):
        self.filter.gaussianNoise = value

    def horizontalFlipCheckboxChanged_slot(self, checked: bool):
        self.filter.hFlip = checked
        self.applyFilter()

    def verticalFlipCheckboxChanged_slot(self, checked: bool):
        self.filter.vFlip = checked
        self.applyFilter()