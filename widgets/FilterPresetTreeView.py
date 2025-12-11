from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide6.QtWidgets import QHeaderView

from image_manipulation import * 

class FilterPresetTreeView(QtWidgets.QTreeView):
    def __init__(self, filterPresets: list[FilterPreset]):
        super().__init__()
        self.filterPresets: list[FilterPreset] = filterPresets
        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.currentQIndex: QModelIndex = None
        self.currentIndex: int = None

        self.setModel(self.model)
        self.loadLabels()

    def loadLabels(self):
        """Loads labels into the model and tree view"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Filter name"])

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        for sFilter in self.filterPresets:
            filterName = QtGui.QStandardItem(sFilter.name)
            self.model.appendRow([filterName])
            
    def selectLabel(self, index: QModelIndex):
        """Selects current index of ImageLabelBox based on `index`"""
        self.selectionModel().select(index,
                                    QItemSelectionModel.SelectionFlag.Select |  QItemSelectionModel.SelectionFlag.Rows)
        self.currentQIndex = index
        self.currentIndex = index.row()