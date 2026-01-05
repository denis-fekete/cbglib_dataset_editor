from PySide6 import QtWidgets


class Container(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout) -> None:
        super().__init__()

        self.setLayout(layout)

    def addWidgets(self, widgetList: list[QtWidgets.QWidget]) -> None:
        for widget in widgetList:
            self.layout().addWidget(widget)
