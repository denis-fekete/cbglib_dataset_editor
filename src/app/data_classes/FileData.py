from dataclasses import dataclass


@dataclass
class FileData:
    name: str
    filePath: str
    ext: str
