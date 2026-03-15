"""
Module: DatasetInfoToolbar.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    GUI QWidget that contains information about dataset loaded from `data.yaml`, for DatasetLoader.py.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal


from app.widgets import *
from app.utils import SharedValues


class DatasetInfoToolbar(QtWidgets.QWidget):
    calculateStatistics = Signal()

    def __init__(self):
        super().__init__()
        self.setMaximumWidth(300)
        self.setLayout(QtWidgets.QGridLayout())

        spacer = QtWidgets.QWidget()
        spacer.setMinimumHeight(10)

        spacer2 = QtWidgets.QWidget()
        spacer2.setMinimumHeight(10)

        self.statisticsBtn = QtWidgets.QPushButton("Calculate statistics")
        self.statisticsBtn.clicked.connect(self.calculateStatistics)

        self.dataPath = QtWidgets.QLineEdit()
        self.trainPath = QtWidgets.QLineEdit()
        self.valPath = QtWidgets.QLineEdit()
        self.testPath = QtWidgets.QLineEdit()

        self._labelsFilesLineEdit = QtWidgets.QLineEdit()
        self._imageSamplesLineEdit = QtWidgets.QLineEdit()
        self._labeledSamplesLineEdit = QtWidgets.QLineEdit()
        self._emptySamplesLineEdit = QtWidgets.QLineEdit()
        self._classesLineEdit = QtWidgets.QLineEdit()
        self._labelBoxesLineEdit = QtWidgets.QLineEdit()

        self.dataPath = QtWidgets.QLineEdit()
        self.trainPath = QtWidgets.QLineEdit()
        self.valPath = QtWidgets.QLineEdit()
        self.testPath = QtWidgets.QLineEdit()
        self.treeView = LabelSelectorTreeView(SharedValues().labelsDict)

        top = 0
        self.layout().addWidget(QtWidgets.QLabel("Statistics:"), top + 0, 0)
        self.layout().addWidget(QtWidgets.QLabel("Label files:"), top + 1, 0)
        self.layout().addWidget(self._labelsFilesLineEdit, top + 1, 1)
        self.layout().addWidget(QtWidgets.QLabel("Image samples:"), top + 2, 0)
        self.layout().addWidget(self._imageSamplesLineEdit, top + 2, 1)
        self.layout().addWidget(
            QtWidgets.QLabel("Annotated image samples:"), top + 3, 0
        )
        self.layout().addWidget(self._labeledSamplesLineEdit, top + 3, 1)
        self.layout().addWidget(QtWidgets.QLabel("Empty image samples:"), top + 4, 0)
        self.layout().addWidget(self._emptySamplesLineEdit, top + 4, 1)
        self.layout().addWidget(QtWidgets.QLabel("Classes:"), top + 5, 0)
        self.layout().addWidget(self._classesLineEdit, top + 5, 1)
        self.layout().addWidget(QtWidgets.QLabel("Image Label Boxes:"), top + 6, 0)
        self.layout().addWidget(self._labelBoxesLineEdit, top + 6, 1)
        self.layout().addWidget(self.statisticsBtn, top + 7, 0, 1, 2)
        self.layout().addWidget(spacer2, top + 8, 0)

        btm = 7

        self.layout().addWidget(QtWidgets.QLabel("data.yaml"), btm + 1, 0)
        self.layout().addWidget(spacer, btm + 2, 0)
        self.layout().addWidget(QtWidgets.QLabel("path:"), btm + 3, 0)
        self.layout().addWidget(self.dataPath, btm + 3, 1)
        self.layout().addWidget(QtWidgets.QLabel("train:"), btm + 4, 0)
        self.layout().addWidget(self.trainPath, btm + 4, 1)
        self.layout().addWidget(QtWidgets.QLabel("val:"), btm + 5, 0)
        self.layout().addWidget(self.valPath, btm + 5, 1)
        self.layout().addWidget(QtWidgets.QLabel("test:"), btm + 6, 0)
        self.layout().addWidget(self.testPath, btm + 6, 1)
        self.layout().addWidget(QtWidgets.QLabel("names:"), btm + 7, 0)
        self.layout().addWidget(self.treeView, btm + 8, 0, 1, 2)

    def updateStatistics(self):
        self._labelsFilesLineEdit.setText(f"{SharedValues().statistics.labelsFiles}")
        self._imageSamplesLineEdit.setText(f"{SharedValues().statistics.imageSamples}")
        self._labeledSamplesLineEdit.setText(
            f"{SharedValues().statistics.labeledSamples}"
        )
        self._emptySamplesLineEdit.setText(f"{SharedValues().statistics.emptySamples}")
        self._classesLineEdit.setText(f"{SharedValues().statistics.classes}")
        self._labelBoxesLineEdit.setText(f"{SharedValues().statistics.labelBoxes}")
