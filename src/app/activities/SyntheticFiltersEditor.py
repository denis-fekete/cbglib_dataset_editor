"""
Module: SyntheticDataCreator.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for creating a synthetic data filters that can be applied to the exported labeled data.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QModelIndex, Slot
from PySide6.QtGui import QShortcut, QKeySequence

from typing import Callable

from app.widgets import *
from app.labeling import *
from app.dataset import *
from app.utils import *
from app.widgets.AbstractTabWidget import AbstractTabWidget
from app.synthetic.SyntheticImage import SyntheticImage
from app.synthetic.FilterPreset import FilterPreset

from app.ui.SyntheticFiltersEditor_ui import Ui_SyntheticFiltersEditor


class SyntheticFiltersEditor(AbstractTabWidget):
    def __init__(self, imageSampleGetter_fn: Callable[[], ImageSample | None]) -> None:
        super().__init__()
        self.ui = Ui_SyntheticFiltersEditor()
        self.ui.setupUi(self)  # type: ignore

        self.imageSampleGetter_fn = imageSampleGetter_fn
        self.imageSample: ImageSample | None = None

        self.syntheticImage: SyntheticImage = SyntheticImage(self.loadSceneImage)
        self.currentFilterPreset = 0
        self._connectUI()

    def _connectUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self._scene = ImageScene()
        self.ui.graphicsView.setScene(self._scene)

        self.ui.applyFiltersButton.clicked.connect(self.updateSyntheticImage)
        self._applyFiltersShortcut = QShortcut(QKeySequence("Tab"), self)
        self._applyFiltersShortcut.activated.connect(self.updateSyntheticImage)

        self.ui.filterPresetTreeView.filterChanged.connect(self.filterChanged)
        self.ui.filterPresetTreeView.filterSelected.connect(self.filterSelected)
        self.ui.newFilterButton.clicked.connect(self.newFilter)
        self.ui.deleteFilterButton.clicked.connect(self.deleteFilter)

        self.ui.blurSlider.valueChanged.connect(self.blurSliderChanged)
        self.ui.blurSpinBox.valueChanged.connect(self.blurSpinboxChanged)

        self.ui.saturationSlider.valueChanged.connect(self.ui.saturationSpinBox.setValue)
        self.ui.saturationSpinBox.valueChanged.connect(self.ui.saturationSlider.setValue)

        self.ui.contrastSlider.valueChanged.connect(self.ui.contrastSpinBox.setValue)
        self.ui.contrastSpinBox.valueChanged.connect(self.ui.contrastSlider.setValue)

        self.ui.brightnessSlider.valueChanged.connect(self.ui.brightnessSpinBox.setValue)
        self.ui.brightnessSpinBox.valueChanged.connect(self.ui.brightnessSlider.setValue)

        self.ui.sapSlider.valueChanged.connect(self.ui.sapSpinBox.setValue)
        self.ui.sapSpinBox.valueChanged.connect(self.ui.sapSlider.setValue)

        self.ui.gaussianSlider.valueChanged.connect(self.ui.gaussianSpinBox.setValue)
        self.ui.gaussianSpinBox.valueChanged.connect(self.ui.gaussianSlider.setValue)

    #######################################################
    # Filter settings
    #######################################################

    @Slot()
    def blurSliderChanged(self, value: int) -> None:
        # blur kernel requires odd numbers
        if value % 2 == 0:
            blurValue = value + 1
            self.ui.blurSpinBox.setValue(blurValue)
        else:
            blurValue = value

        self.ui.blurSpinBox.setValue(blurValue)

    @Slot()
    def blurSpinboxChanged(self, value: int) -> None:
        # blur kernel requires odd numbers
        if value % 2 == 0:
            blurValue = value + 1
            self.ui.blurSpinBox.setValue(blurValue)
        else:
            blurValue = value
        self.ui.blurSlider.setValue(blurValue)

    @Slot()
    def updateSyntheticImage(self) -> None:
        self.updateFilterFromUI()
        self.syntheticImage.applyFilter()

    @Slot()
    def updateFilterFromUI(self) -> None:
        """
        Updates the current `SyntheticImage` with the values from the UI components.
        """
        if self.syntheticImage.filter is None:
            return

        self.syntheticImage.filter.blur = self.ui.blurSpinBox.value()

        self.syntheticImage.filter.saturation = self.ui.saturationSpinBox.value()
        self.syntheticImage.filter.contrast = self.ui.contrastSpinBox.value()
        self.syntheticImage.filter.brightness = self.ui.brightnessSpinBox.value()

        self.syntheticImage.filter.sapNoise = self.ui.sapSpinBox.value()
        self.syntheticImage.filter.gaussianNoise = self.ui.gaussianSpinBox.value()

        self.syntheticImage.filter.vFlip = self.ui.verticalCheckBox.isChecked()
        self.syntheticImage.filter.hFlip = self.ui.horizontalCheckBox.isChecked()

        self.syntheticImage.filter.forceResolution = self.ui.forceResolutionCheckBox.isChecked()
        self.syntheticImage.filter.resolution = self.ui.resolutionSpinBox.value()

        self.syntheticImage.filter.applyLetterbox = self.ui.applyLetterBoxingCheckBox.isChecked()
        self.syntheticImage.filter.paddingRed = self.ui.paddingColorPicker.color.red()
        self.syntheticImage.filter.paddingGreen = self.ui.paddingColorPicker.color.green()
        self.syntheticImage.filter.paddingBlue = self.ui.paddingColorPicker.color.blue()

    @Slot()
    def updateUIFromFilter(self) -> None:
        """
        Updates the values of the UI components from the current `SyntheticImage`.
        """
        if self.syntheticImage.filter is None:
            return

        self.ui.blurSpinBox.setValue(self.syntheticImage.filter.blur)

        self.ui.saturationSpinBox.setValue(self.syntheticImage.filter.saturation)
        self.ui.contrastSpinBox.setValue(self.syntheticImage.filter.contrast)
        self.ui.brightnessSpinBox.setValue(self.syntheticImage.filter.brightness)

        self.ui.sapSpinBox.setValue(self.syntheticImage.filter.sapNoise)
        self.ui.gaussianSpinBox.setValue(self.syntheticImage.filter.gaussianNoise)

        self.ui.verticalCheckBox.setChecked(self.syntheticImage.filter.vFlip)
        self.ui.horizontalCheckBox.setChecked(self.syntheticImage.filter.hFlip)

        self.ui.forceResolutionCheckBox.setChecked(self.syntheticImage.filter.forceResolution)
        self.ui.resolutionSpinBox.setValue(self.syntheticImage.filter.resolution)

        self.ui.applyLetterBoxingCheckBox.setChecked(self.syntheticImage.filter.applyLetterbox)
        self.ui.paddingColorPicker.color.setRed(self.syntheticImage.filter.paddingRed)
        self.ui.paddingColorPicker.color.setGreen(self.syntheticImage.filter.paddingGreen)
        self.ui.paddingColorPicker.color.setBlue(self.syntheticImage.filter.paddingBlue)

    #######################################################
    # Filter browser
    #######################################################

    @Slot()
    def newFilter(self) -> None:
        """Creates new `FilterPreset` into global dictionary of filters"""
        SharedValues().filterPresets.append(FilterPreset())
        self.ui.filterPresetTreeView.loadFilters()

    @Slot()
    def deleteFilter(self) -> None:
        """Deletes filter from global list of filters, all keys will be moved down"""
        index = self.ui.filterPresetTreeView.currIndex
        if index is None:
            return
        SharedValues().filterPresets.pop(index)
        self.ui.filterPresetTreeView.loadFilters()

    def filterSelected(self, index: QModelIndex) -> None:
        """Slot called when label from `_filterSelector` was changed"""
        self.ui.filterPresetTreeView.selectLabel(index)

        # update old
        if self.syntheticImage.filter is not None:
            SharedValues().filterPresets[self.currentFilterPreset] = self.syntheticImage.filter

        self.currentFilterPreset = index.row()
        self.syntheticImage.filter = SharedValues().filterPresets[self.currentFilterPreset]
        self.updateUIFromFilter()

        if self.syntheticImage.imageReference is not None:
            self.syntheticImage.applyFilter()

    def filterChanged(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]
    ) -> None:
        """Slot called when filter was edited"""
        for row in range(topLeft.row(), bottomRight.row() + 1):
            if topLeft != bottomRight:
                raise Exception("Shouldn't happen")

            name = self.ui.filterPresetTreeView.model.index(row, 0).data()
            SharedValues().filterPresets[row].name = name

    #######################################################
    # Other
    #######################################################

    def correctSceneAndView(self) -> None:
        """Corrects scale of `QGraphicsView` based on loaded `ImageFilter`"""
        self.ui.graphicsView.resetTransform()

        wScale = self.ui.graphicsView.rect().width() / self.syntheticImage.width()
        hScale = self.ui.graphicsView.rect().height() / self.syntheticImage.height()

        scale = min(wScale, hScale)

        SCALE_CONST = 0.02  # constant for zooming out move to get rid of sliders on sides
        self.ui.graphicsView.scale(scale - SCALE_CONST, scale - SCALE_CONST)

    def loadSceneImage(self) -> None:
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        self._scene.clear()
        self.ui.graphicsView.resetZoom()
        self.ui.graphicsView.selectedItem = None

        self._scene.setPixmap(self.syntheticImage.getQPixmap())
        self._scene.setSceneRect(0, 0, self.syntheticImage.width(), self.syntheticImage.height())

        self.correctSceneAndView()

    def tabSelected(self) -> None:
        self.ui.filterPresetTreeView.loadFilters()

        imageSample = self.imageSampleGetter_fn()
        if imageSample is None:
            self.ui.filterSettingsWidget.setEnabled(False)
            self.ui.filterBrowserWidget.setEnabled(False)
            return

        self.ui.filterSettingsWidget.setEnabled(True)
        self.ui.filterBrowserWidget.setEnabled(True)

        if self.syntheticImage.filter is None and len(SharedValues().filterPresets) > 0:
            self.syntheticImage.filter = SharedValues().filterPresets[0]
        self.syntheticImage.setReference(imageSample)
        self.updateUIFromFilter()

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        self.syntheticImage.unload()
        self.updateFilterFromUI()

        if self.syntheticImage.filter is not None:
            SharedValues().filterPresets[self.currentFilterPreset] = self.syntheticImage.filter
