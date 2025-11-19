class LabelBox():
    def __init__(self, x, y, width, height, label):
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.label: float = label

    def getDimensionTuple(self) -> tuple[float, float, float, float]:
        """Returns x, y, width, height as a tuple"""
        return self.x, self.y, self.width, self.height