from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from PySide6.QtGui import QStandardItem

from app.image_manipulation import *


class ImageSampleTreeView(QtWidgets.QTreeView):
    def __init__(self, imageSamples: list[ImageSample]) -> None:
        super().__init__()
        self.imageSamples: list[ImageSample] = imageSamples
        self._itemDict: dict[ImageSample, QStandardItem] = {}

        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()  # type: ignore

        self.setModel(self.model)
        self.loadSamples()
        self.setEditTriggers(QtWidgets.QTreeView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def loadSamples(self, restoreVerticalPosition: bool = False) -> bool:
        """
        Loads image samples names into a `QTreeView`. Returns true if some of the samples contain
        incorrect labels. If `restoreVerticalPosition` is set to true a vertical position of scrollbars
        will be restored on load.
        """
        if restoreVerticalPosition:
            verticalPos = self.verticalScrollBar().value()

        self.blockSignals(True)
        self.selectionModel().blockSignals(True)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Name"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        incorrectLabels = False
        for imageSample in self.imageSamples:
            item = QtGui.QStandardItem(imageSample.name)
            self.model.appendRow(item)

            self._itemDict[imageSample] = item

            for labelBox in imageSample.labelBoxes:
                if labelBox.label < 0:
                    item.setBackground(QtGui.Qt.GlobalColor.red)
                    incorrectLabels = True

        # update after UI initialized
        if restoreVerticalPosition:
            QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(verticalPos))  # type: ignore

        self.selectionModel().blockSignals(False)
        self.blockSignals(False)
        return incorrectLabels

    def checkImageSampleWarnings(
        self,
        imageSample: ImageSample,
        checkLabelBoxes: bool = True,
        checkImageLabelBoxes: bool = False,
    ):
        """
        Check `imageSample` for invalid labels. If none is present a red warning background will be
        removed. If invalid labels are present a red warning background will be set for item in
        QTreeView
        """
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

        item = self._itemDict[imageSample]
        if invalidLabels:
            item.setBackground(QtGui.Qt.GlobalColor.red)
        else:
            item.setBackground(QtGui.QBrush())

    def loadSamplesFull(self, restoreVerticalPosition: bool = False) -> bool:
        """
        Loads image samples names, image path and label path into a `QTreeView`.
        Returns true if some of the samples contain incorrect labels
        """
        if restoreVerticalPosition:
            verticalPos = self.verticalScrollBar().value()

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Name", "Image path", "Label path"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        incorrectLabels = False
        for imageSample in self.imageSamples:
            item0 = QtGui.QStandardItem(imageSample.name)
            item1 = QtGui.QStandardItem(imageSample.imagePath)
            item2 = QtGui.QStandardItem(
                imageSample.labelPath if (imageSample.labelPath is not None) else ""
            )
            self.model.appendRow([item0, item1, item2])

            for labelBox in imageSample.labelBoxes:
                if labelBox.label < 0:
                    item0.setBackground(QtGui.Qt.GlobalColor.red)
                    item1.setBackground(QtGui.Qt.GlobalColor.red)
                    item2.setBackground(QtGui.Qt.GlobalColor.red)
                    incorrectLabels = True

        # update after UI initialized
        if restoreVerticalPosition:
            QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(verticalPos))  # type: ignore

        return incorrectLabels
