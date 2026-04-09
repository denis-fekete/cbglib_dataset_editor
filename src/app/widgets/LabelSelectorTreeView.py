"""
Module: LabelSelectorTreeView.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Derived class from QTreeView that shows LabelEntry objects in QTreeView
"""

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt, Slot, Signal
from PySide6.QtWidgets import QHeaderView

from app.labeling import *


class LabelSelectorTreeView(QtWidgets.QTreeView):
    labelsChanged = Signal(QModelIndex)
    dataEdited = Signal(QModelIndex, QModelIndex, list)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self._labelsDict: dict[int, LabelEntry] | None = None
        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()  # type: ignore
        self.currQIndex: QModelIndex | None = None
        self.currIndex: int | None = None

        self.setModel(self.model)
        self.clicked.connect(self.labelsChanged)
        self.model.dataChanged.connect(self._onModelDataChanged)

    def setLabels(self, labelsDict: dict[int, LabelEntry]) -> None:
        self._labelsDict = labelsDict
        self.loadLabels()

    def loadLabels(self, showCounts: bool = False) -> None:
        """Loads labels into the model and tree view"""
        if self._labelsDict is None:
            raise Exception(
                "LabelSelectorTreeView: self._labelsDict was not set."
                " Did you forget to call setLabels()?"
            )

        self.model.clear()
        if showCounts:
            self.model.setHorizontalHeaderLabels(["#", "Name", "Count"])
        else:
            self.model.setHorizontalHeaderLabels(["#", "Name"])

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        if showCounts:
            self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        for label in self._labelsDict.values():
            index = QtGui.QStandardItem(str(label.index))
            index.setFlags(index.flags() & ~Qt.ItemFlag.ItemIsEditable)

            labelName = QtGui.QStandardItem(label.name)

            if showCounts:
                labelCount = QtGui.QStandardItem(f"{label.count}")
                labelCount.setFlags(index.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.model.appendRow([index, labelName, labelCount])
            else:
                self.model.appendRow([index, labelName])

    def selectLabel(self, index: QModelIndex) -> None:
        """Selects current index of LabelEntry based on `index`"""
        self.selectionModel().select(
            index,
            QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows,
        )
        self.currQIndex = index
        self.currIndex = index.row()

    @Slot(QModelIndex, QModelIndex, list)
    def _onModelDataChanged(self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]):
        # WORK-AROUND : on compilation time QList cannot be converted to python list
        self.dataEdited.emit(topLeft, bottomRight, roles)
