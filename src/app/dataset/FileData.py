"""
Module: FileData.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Data class object containing found file (image or label).
"""

from dataclasses import dataclass


@dataclass
class FileData:
    name: str
    filePath: str
    ext: str
