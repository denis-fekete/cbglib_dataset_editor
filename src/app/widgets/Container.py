from PySide6 import QtWidgets
from PySide6.QtCore import QMargins


class Container(QtWidgets.QWidget):
    def __init__(
        self,
        layout: QtWidgets.QLayout,
        maxHeight: int | None = None,
        maxWidth: int | None = None,
        margins: QMargins | None = None,
    ) -> None:
        super().__init__()

        self.setLayout(layout)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        if maxHeight is not None:
            self.setMaximumHeight(maxHeight)
        if maxWidth is not None:
            self.setMaximumWidth(maxWidth)
        if margins is not None:
            self.setContentsMargins(margins)

    def addWidgets(self, widgetList: list[QtWidgets.QWidget]) -> None:
        for widget in widgetList:
            self.layout().addWidget(widget)
