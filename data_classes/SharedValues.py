from PySide6.QtGui import QScreen

from image_manipulation import ImageSample, LabelEntry, FilterPreset

class SharedValues:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self.datasetExportPath: str = ""
        self.datasetImportPath: str = ""
        self.imageSamples: list[ImageSample] = []
        self.filterPresets: list[FilterPreset] = []
        self.labelsDict: dict[int, LabelEntry] = {}
        self.screen: QScreen | None = None

        self._initialized = True