from PySide6.QtWidgets import QWidget


class AbstractTabWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        pass
