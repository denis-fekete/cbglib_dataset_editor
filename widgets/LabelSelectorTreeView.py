from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide6.QtWidgets import QHeaderView

from image_manipulation import * 

class LabelSelectorTreeView(QtWidgets.QTreeView):
    def __init__(self, labels: dict[int, LabelEntry]):
        super().__init__()
        self.labelsDict: list[LabelEntry] = labels
        self.model: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.currentQIndex: QModelIndex = None
        self.currentIndex: int = None

        self.setModel(self.model)
        self.loadLabels()

    def loadLabels(self):
        """Loads labels into the model and tree view"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["#", "Name", "Shortcut"])

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        for label in self.labelsDict.values():
            index = QtGui.QStandardItem(str(label.index))
            index.setFlags(index.flags() & ~Qt.ItemFlag.ItemIsEditable)

            labelName = QtGui.QStandardItem(label.name)
            shortcut = QtGui.QStandardItem(label.shortcut.toString() if (label.shortcut is not None) else "")

            self.model.appendRow([index, labelName, shortcut])
            
    def selectLabel(self, index: QModelIndex):
        """Selects current index of ImageLabelBox based on `index`"""
        self.selectionModel().select(index,
                                    QItemSelectionModel.SelectionFlag.Select |  QItemSelectionModel.SelectionFlag.Rows)
        self.currentQIndex = index
        self.currentIndex = index.row()