"""
Module: FilterPreset.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class defining filter values that are of the filter used for synthetic data.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FilterPreset:
    name: str = "Default"

    blur: int = 0
    sapNoise: int = 0
    gaussianNoise: int = 0

    saturation: int = 100
    contrast: int = 100
    brightness: int = 0

    hFlip: bool = False
    vFlip: bool = False

    def toString(self) -> str:
        string = f"name: {self.name}, blur: {self.blur}, sat : {self.saturation}, \
        brightness : {self.brightness}, contrast : {self.contrast}, \
        hFlip : {self.hFlip}, vFlip : {self.vFlip}, sap : {self.sapNoise}, \
        gaussian : {self.gaussianNoise}"
        return string
