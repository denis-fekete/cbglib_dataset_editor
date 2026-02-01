from dataclasses import dataclass


@dataclass
class LetterboxInfo:
    scale: float
    paddingLeft: int
    paddingTop: int
