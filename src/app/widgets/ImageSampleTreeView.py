"""
Module: ImageSampleTreeView.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
     Derived class from QTreeView that shows ImageSample objects in QTreeView.
"""

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QTimer, Signal, QItemSelection
from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from PySide6.QtGui import QStandardItem

from app.labeling import ImageSample


class ImageSampleTreeView(QtWidgets.QTreeView):
    selectedSampleChanged = Signal(QItemSelection, QItemSelection)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self._imageSamples: list[ImageSample] | None = None
        self._itemDict: dict[ImageSample, QStandardItem] = {}
        self.performingWarningAnalysis = False
        self.treeModel = QtGui.QStandardItemModel()
        self.setModel(self.treeModel)
        self.selectionModel().selectionChanged.connect(self.selectedSampleChanged)

    def setImageSamples(self, imageSamples: list[ImageSample]) -> None:
        self._imageSamples = imageSamples

    def checkImageSampleWarnings(
        self,
        imageSample: ImageSample,
        checkLabelBoxes: bool = True,
        checkImageLabelBoxes: bool = False,
    ):
        """
        Check `imageSample` for invalid labels. If invalid labels are present a red warning
        background will be set for item in QTreeView. If none is present a red warning background
        will be removed.
        """
        if self.performingWarningAnalysis:
            return
        print("checkImageSampleWarnings()")
        self.performingWarningAnalysis = True

        invalidLabels = False

        if checkLabelBoxes:
            for labelBox in imageSample.labelBoxes:
                if labelBox.label == -1:
                    invalidLabels = True
                    break

        if checkImageLabelBoxes:
            for imageLabelBox in imageSample.imageLabelBoxes:
                if imageLabelBox.label == -1:
                    invalidLabels = True
                    break

        for row in range(self.model().rowCount()):
            index = self.model().index(row, 0)
            name = index.data()

            if name == imageSample.name:
                if invalidLabels:
                    self.model().setData(
                        index,
                        QtGui.QBrush(QtGui.Qt.GlobalColor.red),
                        QtCore.Qt.ItemDataRole.BackgroundRole,
                    )
                else:
                    self.model().setData(
                        index, None, QtCore.Qt.ItemDataRole.BackgroundRole
                    )
                break

        self.performingWarningAnalysis = False

    def loadSamples(
        self, restoreVerticalPosition: bool = False, showFull: bool = False
    ) -> bool:
        """
        Loads image samples names, image path and label path into a `QTreeView`.
        Returns true if some of the samples contain incorrect labels
        """
        print(
            f"loadSamples(restoreVerticalPosition={restoreVerticalPosition}, showFull={showFull})"
        )
        if self._imageSamples is None:
            raise Exception(
                "ImageSampleTreeView: self._imageSamples was not set."
                " Did you forget to call setImageSamples()?"
            )

        if restoreVerticalPosition:
            verticalPos = self.verticalScrollBar().value()

        self.treeModel.clear()

        if showFull:
            self.treeModel.setHorizontalHeaderLabels(
                ["Name", "Image path", "Label path"]
            )
            self.header().setSectionResizeMode(
                0, QHeaderView.ResizeMode.ResizeToContents
            )
            self.header().setSectionResizeMode(
                1, QHeaderView.ResizeMode.ResizeToContents
            )
            self.header().setSectionResizeMode(
                2, QHeaderView.ResizeMode.ResizeToContents
            )
        else:
            self.treeModel.setHorizontalHeaderLabels(["Name"])
            self.header().setSectionResizeMode(
                0, QHeaderView.ResizeMode.ResizeToContents
            )

        incorrectLabels = False
        item0: QtGui.QStandardItem = QtGui.QStandardItem("")
        item1: QtGui.QStandardItem = QtGui.QStandardItem("")
        item2: QtGui.QStandardItem = QtGui.QStandardItem("")
        for imageSample in self._imageSamples:
            item0 = QtGui.QStandardItem(imageSample.name)

            if showFull:
                item1 = QtGui.QStandardItem(imageSample.imagePath)
                item2 = QtGui.QStandardItem(
                    imageSample.labelPath if (imageSample.labelPath is not None) else ""
                )
                self.treeModel.appendRow([item0, item1, item2])
            else:
                self.treeModel.appendRow([item0])

            for labelBox in imageSample.labelBoxes:
                if labelBox.label < 0:
                    item0.setBackground(QtGui.Qt.GlobalColor.red)
                    if showFull:
                        item1.setBackground(QtGui.Qt.GlobalColor.red)
                        item2.setBackground(QtGui.Qt.GlobalColor.red)

                    incorrectLabels = True

        # update after UI initialized
        if restoreVerticalPosition:
            QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(verticalPos))  # type: ignore

        self.setEditTriggers(QtWidgets.QTreeView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        return incorrectLabels
