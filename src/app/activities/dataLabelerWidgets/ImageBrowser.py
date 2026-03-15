"""
Module: ImageSampleBrowser.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    QWidget that contains GUI elements for browsing opened ImageSamples in project, for
    DataLabeler.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtCore import QItemSelection

from app.utils import SharedValues
from app.widgets import ImageSampleTreeView


class ImageBrowser(QtWidgets.QWidget):
    nextImage = Signal()
    previousImage = Signal()
    imageSampleChanged = Signal(QItemSelection, QItemSelection)

    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setSpacing(0)
        self.setMaximumWidth(200)

        self.treeView = ImageSampleTreeView(SharedValues().imageSamples)
        self.treeView.loadSamples()
        self.treeView.selectionModel().selectionChanged.connect(self.imageSampleChanged)

        btnNextImageSample = QtWidgets.QPushButton("Next")
        btnNextImageSample.clicked.connect(self.nextImage)

        btnPreviousImageSample = QtWidgets.QPushButton("Previous")
        btnPreviousImageSample.clicked.connect(self.previousImage)

        labelPrevious = QtWidgets.QLabel(" ( Q ) ")
        labelPrevious.setContentsMargins(10, 0, 0, 0)
        labelNext = QtWidgets.QLabel(" ( E ) ")
        labelNext.setContentsMargins(10, 0, 0, 0)

        self.layout().addWidget(QtWidgets.QLabel("Image samples:"), 0, 0)
        self.layout().addWidget(self.treeView, 1, 0, 1, 2)
        self.layout().addWidget(btnPreviousImageSample, 2, 0)
        self.layout().addWidget(btnNextImageSample, 2, 1)
        self.layout().addWidget(labelPrevious, 3, 0)
        self.layout().addWidget(labelNext, 3, 1)
