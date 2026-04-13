"""
Module: LabelEntry.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Object used for storing labels detected from .yaml file or that were created in application
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ImageSample import ImageSample


class LabelEntry:
    def __init__(self, name: str, index: int) -> None:
        self.name: str = name
        self.index: int = index
        self.count: int = 0
        self.samples: list[ImageSample] = []
