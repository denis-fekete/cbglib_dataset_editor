"""
Module: SyntheticDataCreator.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for creating a synthetic data filters that can be applied to the exported labeled data.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QModelIndex, Slot

from typing import Callable

from app.widgets import *
from app.labeling import *
from app.dataset import *
from app.utils import *
from app.widgets.AbstractTabWidget import AbstractTabWidget
from app.synthetic.SyntheticImage import SyntheticImage
from app.synthetic.FilterPreset import FilterPreset
from .syntheticDataWidgets.FilterSettings import FilterSettings
from .syntheticDataWidgets.FilterBrowser import FilterBrowser


class SyntheticDataCreator(AbstractTabWidget):
    def __init__(self, imageSampleGetter_fn: Callable[[], ImageSample | None]) -> None:
        super().__init__()
        self.imageSampleGetter_fn = imageSampleGetter_fn
        self.imageSample: ImageSample | None = None
        self.syntheticImage: SyntheticImage = SyntheticImage(self.loadSceneImage)
        self.syntheticImage.filter = SharedValues().filterPresets[0]

        self._initUI()

    def _initUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self.scene = ImageScene()
        self.view = ZoomGraphicsView(self.scene)

        self.filterSettings = FilterSettings()
        self.filterSettings.blurChanged.connect(self.updateSettingsTexts)
        self.filterSettings.saturationChanged.connect(
            self.syntheticImage.saturationChanged
        )
        self.filterSettings.contrastChanged.connect(self.syntheticImage.contrastChanged)
        self.filterSettings.brightnessChanged.connect(
            self.syntheticImage.brightnessChanged
        )
        self.filterSettings.hFlipChanged.connect(self.syntheticImage.hFlipChanged)
        self.filterSettings.vFlipChanged.connect(self.syntheticImage.vFlipChanged)
        self.filterSettings.sapNoiseChanged.connect(self.syntheticImage.sapNoiseChanged)
        self.filterSettings.gaussianNoiseChanged.connect(
            self.syntheticImage.gaussianChanged
        )
        self.filterSettings.updateTexts.connect(self.update)
        self.filterSettings.applyFilters.connect(self.syntheticImage.applyFilter)
        self.updateSettingsTexts()
        self.updateFilterValues()

        self.filterBrowser = FilterBrowser()
        self.filterBrowser.filterSelected.connect(self.filterSelected)
        self.filterBrowser.filterChanged.connect(self.filterChanged)
        self.filterBrowser.newFilter.connect(self.newFilter)
        self.filterBrowser.deleteFilter.connect(self.deleteFilter)

        self.layout().addWidget(self.filterSettings, 0, 0)
        self.layout().addWidget(self.filterBrowser, 1, 0)
        self.layout().addWidget(self.view, 0, 1, 2, 2)

    #######################################################
    # Filter settings
    #######################################################

    @Slot()
    def updateSettingsTexts(self) -> None:
        self.filterSettings.blurText.setText(
            "Blur: " + str(self.syntheticImage.filter.blur)
        )
        self.filterSettings.saturationText.setText(
            "Saturation: " + str(self.syntheticImage.filter.saturation)
        )
        self.filterSettings.contrastText.setText(
            "Contrast: " + str(self.syntheticImage.filter.contrast)
        )
        self.filterSettings.brightnessText.setText(
            "Brightness: " + str(self.syntheticImage.filter.brightness)
        )
        self.filterSettings.sapNoiseText.setText(
            "Salt and Pepper noise %: " + str(self.syntheticImage.filter.sapNoise)
        )
        self.filterSettings.gaussianNoiseText.setText(
            "gaussian noise %: " + str(self.syntheticImage.filter.gaussianNoise)
        )

    @Slot()
    def updateFilterValues(self) -> None:
        self.filterSettings.vFlipCheckbox.setChecked(self.syntheticImage.filter.vFlip)
        self.filterSettings.hFlipCheckbox.setChecked(self.syntheticImage.filter.hFlip)
        self.filterSettings.blurSlider.setValue(self.syntheticImage.filter.blur)
        self.filterSettings.contrastSlider.setValue(self.syntheticImage.filter.contrast)
        self.filterSettings.sapNoiseSlider.setValue(self.syntheticImage.filter.sapNoise)
        self.filterSettings.brightnessSlider.setValue(
            self.syntheticImage.filter.brightness
        )
        self.filterSettings.saturationSlider.setValue(
            self.syntheticImage.filter.saturation
        )
        self.filterSettings.gaussianNoiseSlider.setValue(
            self.syntheticImage.filter.gaussianNoise
        )

    #######################################################
    # Filter browser
    #######################################################

    @Slot()
    def newFilter(self) -> None:
        """Creates new `FilterPreset` into global dictionary of filters"""
        SharedValues().filterPresets.append(FilterPreset())
        self.filterBrowser.selector.loadLabels()

    @Slot()
    def deleteFilter(self) -> None:
        """Deletes filter from global list of filters, all keys will be moved down"""
        index = self.filterBrowser.selector.currIndex
        if index is None:
            return
        SharedValues().filterPresets.pop(index)
        self.filterBrowser.selector.loadLabels()

    def filterSelected(self, index: QModelIndex) -> None:
        """Slot called when label from `_filterSelector` was changed"""
        self.filterBrowser.selector.selectLabel(index)

        self.syntheticImage.filter = SharedValues().filterPresets[index.row()]
        if self.syntheticImage.imageReference is not None:
            self.syntheticImage.applyFilter()

    def filterChanged(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]
    ) -> None:
        """Slot called when filter was edited"""
        for row in range(topLeft.row(), bottomRight.row() + 1):
            if topLeft != bottomRight:
                raise Exception("Shouldn't happen")

            name = self.filterBrowser.selector.model.index(row, 0).data()
            SharedValues().filterPresets[row].name = name

    #######################################################
    # Other
    #######################################################

    def correctSceneAndView(self) -> None:
        """Corrects scale of `QGraphicsView` based on loaded `ImageFilter`"""
        self.view.resetTransform()

        wScale = self.view.rect().width() / self.syntheticImage.width()
        hScale = self.view.rect().height() / self.syntheticImage.height()

        scale = min(wScale, hScale)

        SCALE_CONST = (
            0.02  # constant for zooming out move to get rid of sliders on sides
        )
        self.view.scale(scale - SCALE_CONST, scale - SCALE_CONST)

    def loadSceneImage(self) -> None:
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        self.scene.clear()
        self.view.resetZoom()
        self.view.selectedItem = None

        self.scene.setPixmap(self.syntheticImage.getQPixmap())
        self.scene.setSceneRect(
            0, 0, self.syntheticImage.width(), self.syntheticImage.height()
        )

        self.correctSceneAndView()

    def tabSelected(self) -> None:
        """Loads current image selected in `DataLabeler` activity"""
        imageSample = self.imageSampleGetter_fn()
        if imageSample is None:
            return

        if self.syntheticImage.imageReference == imageSample:
            self.syntheticImage.updateReference()
        else:
            self.syntheticImage.setReference(imageSample)

        self.loadSceneImage()

    def tabClosed(self) -> None:
        pass
