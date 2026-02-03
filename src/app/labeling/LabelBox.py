"""
Module: LabelBox.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class containing information about `ImageSample`, this information is mostly used for storing
    into label files in text form.
"""


class LabelBox:
    def __init__(
        self, x: float, y: float, width: float, height: float, label: int
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.label: int = label

    def getDimensionTuple(self) -> tuple[float, float, float, float]:
        """Returns x, y, width, height as a tuple"""
        return self.x, self.y, self.width, self.height
