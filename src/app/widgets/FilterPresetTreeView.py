"""
Module: FilterPresetTreeView.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class derived QTreeView that shows `FilterPresent` objects.
"""

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QItemSelectionModel, QModelIndex, Signal, Slot
from PySide6.QtWidgets import QHeaderView

from app.synthetic import *
from app.utils.SharedValues import *


class FilterPresetTreeView(QtWidgets.QTreeView):
    filterSelected = Signal(QModelIndex)
    filterChanged = Signal(QModelIndex, QModelIndex, list)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()  # type: ignore
        self.currQIndex: QModelIndex | None = None
        self.currIndex: int | None = None
        self._filterPresets: list[FilterPreset] | None = None
        self.setModel(self.model)

        self.clicked.connect(self.filterSelected)
        self.model.dataChanged.connect(self._onModelDataChanged)

        self.loadFilters()

    def setFilters(self, filterPresets: list[FilterPreset]):
        self._filterPresets = filterPresets

    def loadFilters(self) -> None:
        """Loads labels into the model and tree view"""
        if self._filterPresets:
            raise Exception(
                "FilterPresetTreeView: self._filterPresets was not set."
                " Did you forget to call setFilters()?"
            )

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Filter name"])

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for sFilter in SharedValues().filterPresets:
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

    @Slot(QModelIndex, QModelIndex, list)
    def _onModelDataChanged(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]
    ):
        # WORK-AROUND : on compilation time QList cannot be converted to python list
        self.filterChanged.emit(topLeft, bottomRight, roles)
