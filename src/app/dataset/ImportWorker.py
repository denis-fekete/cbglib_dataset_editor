"""
Module: ExportWorker.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class derived from QObject that is used for multi-threaded exporting of images and labels.
"""

import os
from pathlib import Path
from typing import Callable
import yaml  # type: ignore

from PySide6.QtCore import Slot, Signal, QObject

from app.labeling.ImageSample import ImageSample, LabelEntry
from .FileData import FileData
from app.utils import SharedValues
from app.utils.DatasetStatistics import DatasetStatistics

from app.labeling.ImageSample import ImageSample, LabelEntry


class ImportWorker(QObject):
    progress = Signal(float)
    finished = Signal()
    dataYamlPathFound = Signal(str)

    def __init__(
        self,
        rootPath: str,
        outputList: list[ImageSample],
        labelsDict: dict[int, LabelEntry],
        screenScaleText_fn: Callable[[], float],
    ) -> None:
        super().__init__()
        self.rootPath = rootPath
        self.outputList = outputList
        self.labelsDict = labelsDict
        self.screenScaleText_fn = screenScaleText_fn
        self.progressCnt = 0.0
        self.progressStep = 0.0

    @Slot()
    def run(self) -> None:
        """Clears `imageSamples` and loads new from `SharedValues().datasetImportPath`"""

        # reset statistics
        SharedValues().statistics = DatasetStatistics()
        self.dataYamlPath = None

        fileDataList: list[FileData] = self._loadFilesIntoList(self.rootPath)
        self.progressCnt = 25
        self.progress.emit(self.progressCnt)
        self.progressStep = (100.0 - self.progressCnt) / len(fileDataList)

        for item in fileDataList:
            self.progressCnt += self.progressStep
            self.progress.emit(self.progressCnt)

            if item.ext == ".jpg":
                SharedValues().statistics.imageSamples += 1

                matchedLabels: list[FileData] = []
                for other in fileDataList:
                    if other.ext == ".txt" and other.name == item.name:
                        matchedLabels.append(other)
                        SharedValues().statistics.labeledSamples += 1

                if len(matchedLabels) > 1:
                    raise Exception(
                        f"Multiple label (.txt) files found for one image (.jpg file): {matchedLabels}"
                    )

                label = matchedLabels[0] if len(matchedLabels) > 0 else None
                labelPath = label.filePath if (label is not None) else None
                labelExt = label.ext if (label is not None) else None

                self.outputList.append(
                    ImageSample(
                        rootPath=self.rootPath,
                        name=item.name,
                        imagePath=item.filePath,
                        imageExt=item.ext,
                        labelPath=labelPath,
                        labelExt=labelExt,
                        labelsDict=self.labelsDict,
                        screenScaleText_fn=self.screenScaleText_fn,
                    )
                )

                sampleParts = Path(item.filePath).parts
                if "images" in sampleParts:
                    if "train" in sampleParts:
                        SharedValues().statistics.trainSamples += 1
                    elif "val" in sampleParts:
                        SharedValues().statistics.valSamples += 1
                    elif "test" in sampleParts:
                        SharedValues().statistics.testSamples += 1

            elif item.ext == ".yaml" and item.name == "data":
                if self.dataYamlPath == None:
                    path = Path(self.rootPath)
                    path = path / item.filePath / (item.name + item.ext)

                    self.dataYamlPath = str(path.resolve()._str)
                    self.dataYamlPathFound.emit(self.dataYamlPath)
                else:
                    raise Exception(
                        "Error: Found multiple data.yaml files. Only one or none (will get created automatically) should be in dataset!"
                    )
            elif item.ext == ".txt":
                SharedValues().statistics.labelsFiles += 1

        self.finished.emit()

    def _loadFilesIntoList(self, rootPath: str) -> list[FileData]:
        """Returns list of dictionaries containing name, path and extension"""
        rawFiles: list[str] = self._loadFilesRaw(rootPath)

        fileDataList: list[FileData] = []
        for file in rawFiles:
            fullPath: Path = Path(rootPath) / file
            filePath = str(Path(file).parent)
            fileName = fullPath.stem
            ext = fullPath.suffix

            fileDataList.append(FileData(name=fileName, filePath=filePath, ext=ext))

        return fileDataList

    def _loadFilesRaw(self, directoryPath: str) -> list[str]:
        """
        Reads all files from directory path, sub directories will be called recursively and name
        of subdirectory will be added to the name. Example:\n
        root
          |- subdirectoryA
          |---fileA
          |- fileB
        Will result in: 'fileB', 'subdirectoryA/fileA'
        """
        files: list[str] = []
        path = Path(directoryPath)
        for item in os.listdir(directoryPath):
            if os.path.isfile(path / item):
                files.append(item)

            elif os.path.isdir(path / item):
                tmpFiles = self._loadFilesRaw(str(path / item))
                for dirItem in tmpFiles:
                    files.append(item + r"/" + dirItem)
            else:
                raise Exception("Unknown file/directory format")
        return files
