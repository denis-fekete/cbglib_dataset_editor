from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ColorPicker(QtWidgets.QPushButton):
    def __init__(self, defaultColor: QColor, callback_fn=None):
        super().__init__()

        self.clicked.connect(self.onClicked_slot)
        self.color = defaultColor
        self.callback_fn = callback_fn
        self._updateBackgroundColor()

    def onClicked_slot(self):
        color = QtWidgets.QColorDialog.getColor(self.color)

        if(color.isValid()):
            self.color = color

        self._updateBackgroundColor()

        if(self.callback_fn is not None):
            self.callback_fn()

    def _updateBackgroundColor(self):
        self.setStyleSheet(f"background-color: {self.color.name()}")

