from dataclasses import dataclass


@dataclass
class Detection:
    xCenter: float
    yCenter: float
    width: float
    height: float
    classIndex: int
    score: float
