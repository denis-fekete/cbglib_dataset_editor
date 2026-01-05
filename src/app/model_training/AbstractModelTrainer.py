from PySide6.QtCore import QObject, Signal


class AbstractModelTrainer(QObject):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
