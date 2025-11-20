from PySide6.QtGui import QKeySequence

class LabelEntry():
    def __init__(self, name: str, index: int, shortcut: QKeySequence = None):
        self.name: str = name
        self.index: int = index
        self.shortcut: QKeySequence = shortcut