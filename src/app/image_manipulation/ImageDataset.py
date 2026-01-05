import os
from pathlib import Path
from typing import Callable

from .ImageSample import ImageSample, LabelEntry
from app.data_classes import FileData


class ImageDataset:
    def __init__(self, screenScaleText_fn: Callable[[], float]) -> None:
        self.screenScaleText_fn: Callable[[], float] = screenScaleText_fn
        self.dataYamlPath: str | None = None

    def loadImageSamples(
        self,
        rootPath: str,
        outputList: list[ImageSample],
        labelsDict: dict[int, LabelEntry],
    ) -> None:
        """Clears `imageSamples` and loads new from `SharedValues().datasetImportPath`"""
        self.dataYamlPath = None

        fileDataList: list[FileData] = self._loadFilesIntoList(rootPath)

        for item in fileDataList:
            if item.ext == ".jpg":
                matchedLabels: list[FileData] = []
                for other in fileDataList:
                    if other.ext == ".txt" and other.name == item.name:
                        matchedLabels.append(other)

                if len(matchedLabels) > 1:
                    raise Exception(
                        f"Multiple label (.txt) files found for one image (.jpg file): {matchedLabels}"
                    )

                label = matchedLabels[0] if len(matchedLabels) > 0 else None
                labelPath = label.filePath if (label is not None) else None
                labelExt = label.ext if (label is not None) else None

                outputList.append(
                    ImageSample(
                        rootPath=rootPath,
                        name=item.name,
                        imagePath=item.filePath,
                        imageExt=item.ext,
                        labelPath=labelPath,
                        labelExt=labelExt,
                        labelsDict=labelsDict,
                        screenScaleText_fn=self.screenScaleText_fn,
                    )
                )

            elif item.ext == ".yaml" and item.name == "data":
                if self.dataYamlPath == None:
                    path = Path(rootPath)
                    path = path / item.filePath / (item.name + item.ext)

                    self.dataYamlPath = str(path.resolve()._str)
                else:
                    raise Exception(
                        "Error: Found multiple data.yaml files. Only one or none (will get created automatically) should be in dataset!"
                    )

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
