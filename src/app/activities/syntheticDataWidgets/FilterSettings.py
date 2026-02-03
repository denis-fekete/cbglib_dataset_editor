"""
Module: ModelSelector.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains elements for changing synthetic data filter values, for SyntheticDataCreator.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QSizePolicy

from app.widgets import *


class FilterSettings(QtWidgets.QWidget):
    blurChanged = Signal(int)
    saturationChanged = Signal(int)
    contrastChanged = Signal(int)
    brightnessChanged = Signal(int)
    hFlipChanged = Signal(bool)
    vFlipChanged = Signal(bool)
    sapNoiseChanged = Signal(int)
    gaussianNoiseChanged = Signal(int)

    updateTexts = Signal()
    applyFilters = Signal()

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.blurSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.blurSlider.setMinimum(0)
        self.blurSlider.setMaximum(100)
        self.blurSlider.setSingleStep(2)
        self.blurSlider.valueChanged.connect(self.blurChanged)
        self.blurSlider.valueChanged.connect(self.updateTexts)
        self.blurSlider.sliderReleased.connect(self.applyFilters)

        self.saturationSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.saturationSlider.setMinimum(50)
        self.saturationSlider.setMaximum(150)
        self.saturationSlider.valueChanged.connect(self.saturationChanged)
        self.saturationSlider.valueChanged.connect(self.updateTexts)
        self.saturationSlider.sliderReleased.connect(self.applyFilters)

        self.contrastSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.contrastSlider.setMinimum(50)
        self.contrastSlider.setMaximum(150)
        self.contrastSlider.valueChanged.connect(self.contrastChanged)
        self.contrastSlider.valueChanged.connect(self.updateTexts)
        self.contrastSlider.sliderReleased.connect(self.applyFilters)

        self.brightnessSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.brightnessSlider.setMinimum(-50)
        self.brightnessSlider.setMaximum(50)
        self.brightnessSlider.valueChanged.connect(self.brightnessChanged)
        self.brightnessSlider.valueChanged.connect(self.updateTexts)
        self.brightnessSlider.sliderReleased.connect(self.applyFilters)

        self.hFlipCheckbox = QtWidgets.QCheckBox("Horizontal flip")
        self.hFlipCheckbox.toggled.connect(self.hFlipChanged)

        self.vFlipCheckbox = QtWidgets.QCheckBox("Vertical flip")
        self.vFlipCheckbox.toggled.connect(self.vFlipChanged)

        self.sapNoiseSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.sapNoiseSlider.setMinimum(0)
        self.sapNoiseSlider.setMaximum(100)
        self.sapNoiseSlider.valueChanged.connect(self.sapNoiseChanged)
        self.sapNoiseSlider.valueChanged.connect(self.updateTexts)
        self.sapNoiseSlider.sliderReleased.connect(self.applyFilters)

        self.gaussianNoiseSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.gaussianNoiseSlider.setMinimum(0)
        self.gaussianNoiseSlider.setMaximum(100)
        self.gaussianNoiseSlider.valueChanged.connect(self.gaussianNoiseChanged)
        self.gaussianNoiseSlider.valueChanged.connect(self.updateTexts)
        self.gaussianNoiseSlider.sliderReleased.connect(self.applyFilters)

        self.blurText = QtWidgets.QLabel()
        self.saturationText = QtWidgets.QLabel()
        self.brightnessText = QtWidgets.QLabel()
        self.contrastText = QtWidgets.QLabel()
        self.sapNoiseText = QtWidgets.QLabel()
        self.gaussianNoiseText = QtWidgets.QLabel()

        blurContainer = Container(QtWidgets.QVBoxLayout())
        blurContainer.addWidgets([self.blurText, self.blurSlider])
        saturationContainer = Container(QtWidgets.QVBoxLayout())
        saturationContainer.addWidgets([self.saturationText, self.saturationSlider])
        contrastContainer = Container(QtWidgets.QVBoxLayout())
        contrastContainer.addWidgets([self.contrastText, self.contrastSlider])
        brightnessContainer = Container(QtWidgets.QVBoxLayout())
        brightnessContainer.addWidgets([self.brightnessText, self.brightnessSlider])
        sapNoiseContainer = Container(QtWidgets.QVBoxLayout())
        sapNoiseContainer.addWidgets([self.sapNoiseText, self.sapNoiseSlider])
        gaussianNoiseContainer = Container(QtWidgets.QVBoxLayout())
        gaussianNoiseContainer.addWidgets(
            [self.gaussianNoiseText, self.gaussianNoiseSlider]
        )

        self.layout().addWidget(blurContainer)
        self.layout().addWidget(saturationContainer)
        self.layout().addWidget(contrastContainer)
        self.layout().addWidget(brightnessContainer)
        self.layout().addWidget(sapNoiseContainer)
        self.layout().addWidget(gaussianNoiseContainer)
        self.layout().addWidget(self.hFlipCheckbox)
        self.layout().addWidget(self.vFlipCheckbox)
