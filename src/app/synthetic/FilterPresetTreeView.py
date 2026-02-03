"""
Module: FilterPresetTreeView.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class derived QTreeView that shows `FilterPresent` objects.
"""

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QItemSelectionModel, QModelIndex
from PySide6.QtWidgets import QHeaderView

from app.synthetic import *


class FilterPresetTreeView(QtWidgets.QTreeView):
    def __init__(self, filterPresets: list[FilterPreset]) -> None:
        super().__init__()
        self.filterPresets: list[FilterPreset] = filterPresets
        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()  # type: ignore
        self.currQIndex: QModelIndex | None = None
        self.currIndex: int | None = None

        self.setModel(self.model)
        self.loadLabels()

    def loadLabels(self) -> None:
        """Loads labels into the model and tree view"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Filter name"])

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        for sFilter in self.filterPresets:
            filterName = QtGui.QStandardItem(sFilter.name)
            self.model.appendRow([filterName])

    def selectLabel(self, index: QModelIndex) -> None:
        """Selects current index of ImageLabelBox based on `index`"""
        self.selectionModel().select(
            index,
            QItemSelectionModel.SelectionFlag.Select
            | QItemSelectionModel.SelectionFlag.Rows,
        )
        self.currQIndex = index
        self.currIndex = index.row()
