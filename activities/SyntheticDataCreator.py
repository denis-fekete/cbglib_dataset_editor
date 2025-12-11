from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QSizePolicy

import os
from pathlib import Path

from widgets import *
from utils import *
from image_manipulation import *

class SyntheticDataCreator(QtWidgets.QWidget):
    def __init__(self, imageSampleGetter_fn: ImageSample, filterPresets : list[SyntheticImage]):
        super().__init__()  
        self.imageSampleGetter_fn = imageSampleGetter_fn
        self.imageSample : ImageSample = None
        self.filterPresets : list[SyntheticImage] = filterPresets
        self.syntheticImage : SyntheticImage = SyntheticImage(self.loadSceneImage)
        self.syntheticImage.filter = self.filterPresets[0]

        self._initUI()

    def _initUI(self):
        self.setLayout(QtWidgets.QGridLayout())

        self._initTopBarContainer()
        self._initImagePreviewContainer()
        self._initPresetSelectorContainer()
        self._initImageSettingsContainer()

        self.layout().addWidget(self._topBarContainer, 0, 0, 1, 3)
        self.layout().addWidget(self._imageSettingsContainer, 1, 0)
        self.layout().addWidget(self._presetSelectorContainer, 2, 0)
        self.layout().addWidget(self._view, 1, 1, 2, 2)

    def _initTopBarContainer(self):
        self._topBarContainer = QtWidgets.QWidget()
        self._topBarContainer.setLayout(QtWidgets.QHBoxLayout())
        self._topBarContainer.layout().setSpacing(0)
        self._topBarContainer.layout().setContentsMargins(0, 0, 0, 0)
        self._topBarContainer.setMaximumHeight(30)

        
        self._title = QtWidgets.QLabel("")
        saveButton = QtWidgets.QPushButton("Save")
        saveButton.clicked.connect(self.saveSyntheticImage_slot)
        
        self._topBarContainer.layout().addWidget(self._title)
        self._topBarContainer.layout().addWidget(saveButton)

    def _initPresetSelectorContainer(self):
        self._presetSelectorContainer = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        self._presetSelectorContainer.setLayout(layout)
        self._presetSelectorContainer.setMaximumWidth(300)
        self._presetSelectorContainer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self._filterSelector = FilterPresetTreeView(self.filterPresets)
        self._filterSelector.clicked.connect(self.filterSelected_slot)
        self._filterSelector.model.dataChanged.connect(self.filterChanged_slot)

        self._btnNewLabel = QtWidgets.QPushButton("New")
        self._btnNewLabel.clicked.connect(self.newFilter_slot)

        self._btnDeleteLabel = QtWidgets.QPushButton("Delete")
        self._btnDeleteLabel.clicked.connect(self.deleteFilter_slot)

        self._presetSelectorContainer.layout().addWidget(QtWidgets.QLabel("Filters:"), 0, 0)
        self._presetSelectorContainer.layout().addWidget(self._btnNewLabel, 1, 0)
        self._presetSelectorContainer.layout().addWidget(self._btnDeleteLabel, 1, 1)
        self._presetSelectorContainer.layout().addWidget(self._filterSelector, 2, 0, 1, 2)

    def _initImageSettingsContainer(self):
        self._imageSettingsContainer = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self._imageSettingsContainer.setLayout(layout)
        self._imageSettingsContainer.setMaximumWidth(300)
        self._imageSettingsContainer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.blurSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.blurSlider.setMinimum(0)
        self.blurSlider.setMaximum(100)
        self.blurSlider.setSingleStep(2)
        self.blurSlider.valueChanged.connect(self.syntheticImage.blurSliderChanged_slot)
        self.blurSlider.valueChanged.connect(self.updateSettingsTexts)
        self.blurSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self.saturationSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.saturationSlider.setMinimum(50)
        self.saturationSlider.setMaximum(150)
        self.saturationSlider.valueChanged.connect(self.syntheticImage.saturationSliderChanged_slot)
        self.saturationSlider.valueChanged.connect(self.updateSettingsTexts)
        self.saturationSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self.contrastSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.contrastSlider.setMinimum(50)
        self.contrastSlider.setMaximum(150)
        self.contrastSlider.valueChanged.connect(self.syntheticImage.contrastSliderChanged_slot)
        self.contrastSlider.valueChanged.connect(self.updateSettingsTexts)
        self.contrastSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self.brightnessSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.brightnessSlider.setMinimum(-50)
        self.brightnessSlider.setMaximum(50)
        self.brightnessSlider.valueChanged.connect(self.syntheticImage.brightnessSliderChanged_slot)
        self.brightnessSlider.valueChanged.connect(self.updateSettingsTexts)
        self.brightnessSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self.hFlipCheckbox = QtWidgets.QCheckBox("Horizontal flip");
        self.hFlipCheckbox.toggled.connect(self.syntheticImage.horizontalFlipCheckboxChanged_slot)

        self.vFlipCheckbox = QtWidgets.QCheckBox("Vertical flip");
        self.vFlipCheckbox.toggled.connect(self.syntheticImage.verticalFlipCheckboxChanged_slot)

        self.sapNoiseSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.sapNoiseSlider.setMinimum(0)
        self.sapNoiseSlider.setMaximum(100)
        self.sapNoiseSlider.valueChanged.connect(self.syntheticImage.sapNoiseSliderChanged_slot)
        self.sapNoiseSlider.valueChanged.connect(self.updateSettingsTexts)
        self.sapNoiseSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self.gaussianNoiseSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.gaussianNoiseSlider.setMinimum(0)
        self.gaussianNoiseSlider.setMaximum(100)
        self.gaussianNoiseSlider.valueChanged.connect(self.syntheticImage.gaussianNoiseSliderChanged_slot)
        self.gaussianNoiseSlider.valueChanged.connect(self.updateSettingsTexts)
        self.gaussianNoiseSlider.sliderReleased.connect(self.syntheticImage.applyFilter)

        self._settingsBlurText = QtWidgets.QLabel()
        self._settingsSaturationText = QtWidgets.QLabel()
        self._settingsBrightnessText = QtWidgets.QLabel()
        self._settingsContrastText = QtWidgets.QLabel()
        self._settingsSAPNoiseText = QtWidgets.QLabel()
        self._settingsGaussianNoiseText = QtWidgets.QLabel()    
    
        blurContainer = Container(QtWidgets.QVBoxLayout())
        blurContainer.addWidgets([self._settingsBlurText, self.blurSlider])
        saturationContainer = Container(QtWidgets.QVBoxLayout())
        saturationContainer.addWidgets([self._settingsSaturationText, self.saturationSlider])
        contrastContainer = Container(QtWidgets.QVBoxLayout())
        contrastContainer.addWidgets([self._settingsContrastText, self.contrastSlider])
        brightnessContainer = Container(QtWidgets.QVBoxLayout())
        brightnessContainer.addWidgets([self._settingsBrightnessText, self.brightnessSlider])
        sapNoiseContainer = Container(QtWidgets.QVBoxLayout())
        sapNoiseContainer.addWidgets([self._settingsSAPNoiseText, self.sapNoiseSlider])
        gaussianNoiseContainer = Container(QtWidgets.QVBoxLayout())
        gaussianNoiseContainer.addWidgets([self._settingsGaussianNoiseText, self.gaussianNoiseSlider])

        self._imageSettingsContainer.layout().addWidget(blurContainer)
        self._imageSettingsContainer.layout().addWidget(saturationContainer)
        self._imageSettingsContainer.layout().addWidget(contrastContainer)
        self._imageSettingsContainer.layout().addWidget(brightnessContainer)
        self._imageSettingsContainer.layout().addWidget(sapNoiseContainer)
        self._imageSettingsContainer.layout().addWidget(gaussianNoiseContainer)
        self._imageSettingsContainer.layout().addWidget(self.hFlipCheckbox)
        self._imageSettingsContainer.layout().addWidget(self.vFlipCheckbox)

        self.updateSettingsTexts()

    def _initImagePreviewContainer(self):
        self._scene = ImageScene()
        self._view = ZoomGraphicsView(self._scene)

    def _correctSceneAndView(self):
        """Corrects scale of `QGraphicsView` based on loaded `ImageFilter`"""
        self._view.resetTransform()

        wScale = self._view.rect().width() / self.syntheticImage.width()
        hScale = self._view.rect().height() / self.syntheticImage.height()

        scale = min(wScale, hScale)

        SCALE_CONST = 0.02 # constant for zooming out move to get rid of sliders on sides
        self._view.scale(scale - SCALE_CONST, scale - SCALE_CONST)

    def tab_selected(self):
        """Loads current image selected in `DataLabeler` activity"""
        imageSample = self.imageSampleGetter_fn()
        if(imageSample is None):
            return
        
        if(self.syntheticImage.imageReference == imageSample):
            self.syntheticImage.updateReference()
        else:
            self.syntheticImage.setReference(imageSample)

        self.loadSceneImage()

    def updateSettingsTexts(self):
        self._settingsBlurText.setText("Blur: " + str(self.syntheticImage.filter.blur))
        self._settingsSaturationText.setText("Saturation: " + str(self.syntheticImage.filter.saturation))
        self._settingsContrastText.setText("Contrast: " + str(self.syntheticImage.filter.contrast))
        self._settingsBrightnessText.setText("Brightness: " + str(self.syntheticImage.filter.brightness))
        self._settingsSAPNoiseText.setText("Salt and Pepper noise %: " + str(self.syntheticImage.filter.sapNoise))
        self._settingsGaussianNoiseText.setText("gaussian noise %: " + str(self.syntheticImage.filter.gaussianNoise))
        
    def loadSceneImage(self):
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        self._scene.clear()
        self._view.resetZoom()
        self._view.selectedItem = None

        self._scene.setPixmap(self.syntheticImage.getQPixmap())
        self._scene.setSceneRect(0, 0, self.syntheticImage.width(), self.syntheticImage.height())
        
        self._title.setText(self.syntheticImage.imageReference.name)
        
        self._correctSceneAndView()

    def updateFilterValues(self):
        self.vFlipCheckbox.setChecked(self.syntheticImage.filter.vFlip)
        self.hFlipCheckbox.setChecked(self.syntheticImage.filter.hFlip)
        self.blurSlider.setValue( self.syntheticImage.filter.blur)
        self.contrastSlider.setValue(self.syntheticImage.filter.contrast)
        self.sapNoiseSlider.setValue( self.syntheticImage.filter.sapNoise)
        self.brightnessSlider.setValue( self.syntheticImage.filter.brightness)
        self.saturationSlider.setValue( self.syntheticImage.filter.saturation)
        self.gaussianNoiseSlider.setValue( self.syntheticImage.filter.gaussianNoise)

    def saveSyntheticImage_slot(self):
        for sFilter in self.filterPresets:
            sFilter.setReference(self.imageSampleGetter_fn())
            sFilter.save(Path(os.getcwd()), Path(os.getcwd()))

    def newFilter_slot(self):
        """Creates new `FilterPreset` into global dictionary of filters"""
        index = len(self.filterPresets)
        self.filterPresets.append(FilterPreset())
        self._filterSelector.loadLabels()

    def deleteFilter_slot(self):
        """Deletes filter from global list of filters, all keys will be moved down"""
        index = self._filterSelector.currentIndex
        self.filterPresets.pop(index)
        self._filterSelector.loadLabels()

    def filterSelected_slot(self, index: QModelIndex):
        """Slot called when label from `_filterSelector` was changed"""
        self._filterSelector.selectLabel(index)
        
        print(f"Selected :{index.row()}")
        self.syntheticImage.filter = self.filterPresets[index.row()]
        if(self.syntheticImage.imageReference is not None):
            self.syntheticImage.applyFilter()
            self.updateSettingsTexts()
            print(f"Applying filter: {self.syntheticImage.filter.toString()}")
       
    def filterChanged_slot(self, topLeft, bottomRight, roles):
        """Slot called when filter was edited"""
        for row in range(topLeft.row(), bottomRight.row() + 1):
            if(topLeft != bottomRight):
                raise Exception("Shouldn't happen")
            
            name = self._filterSelector.model.index(row, 0).data()
            print(f"labelChanged_slot(): name: {name}, row: {row}")
            self.filterPresets[row].name = name

        print("Filters:")
        for sFilter in self.filterPresets:
            print(f"\t{sFilter.name}")

    def tab_closed(self):
        pass