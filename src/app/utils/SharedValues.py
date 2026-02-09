"""
Module: SharedValues.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Global variables as a single instance 'static' function getter that is used in application.
"""

from PySide6.QtGui import QScreen

from app.labeling.ImageSample import ImageSample
from app.labeling.LabelEntry import LabelEntry
from app.synthetic.FilterPreset import FilterPreset
from app.settings import *


class SharedValues:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return

        self.datasetExportPath: str = ""
        self.datasetImportPath: str = ""
        self.imageSamples: list[ImageSample] = []
        self.filterPresets: list[FilterPreset] = []
        self.labelsDict: dict[int, LabelEntry] = {}
        self.screen: QScreen
        self.settings: AppSettings

        self._initialized = True
