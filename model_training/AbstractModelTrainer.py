from PySide6.QtCore import QObject, Signal, Slot

class AbstractModelTrainer(QObject):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self):
        super().__init__()