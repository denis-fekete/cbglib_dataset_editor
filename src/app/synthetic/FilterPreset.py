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
    """
    :var name: name of the filter, mostly for the UI purposes.
    :var blur: amount of blur added to the image, must be odd number.
    :var sapNoise: amount of sap noise added to the image, values are 1/1000, where 1000 is full
    image covered in sap noise. This generate black and white pixels.
    :var gaussianNoise: amount of gaussian noise added to the image, values are 1/1000, where 1000 is full
    image covered in sap noise.
    :var saturation: saturation value of the filter
    :var contrast: contrast value of the filter
    :var brightness: brightness value of the filter
    :var hFlip: if set to `True`, image will be horizontally flipped
    :var vFlip: if set to `True`, image will be vertically flipped
    :var forceResolution: if set to `True`, resolution will be changed using `resolution` parameter.
    :var resolution: resolution, to which image will be rescaled for 1:1 aspect ratio without
    distortion, only one dimension (the higher one) will satisfy this resolution.
    :var applyLetterbox: if set to `True` letter-boxing will be applied, forcing image into 1:1
    aspect ratio with padded dimension
    :var paddingRed: Red value of the padding applied to the letter-boxing.
    :var paddingGreen: Green value of the padding applied to the letter-boxing.
    :var paddingBlue: Blue value of the padding applied to the letter-boxing.
    """

    name: str = "Default"

    blur: int = 0
    sapNoise: int = 0
    gaussianNoise: int = 0

    saturation: int = 100
    contrast: int = 100
    brightness: int = 0

    hFlip: bool = False
    vFlip: bool = False

    forceResolution: bool = False
    resolution: int = 0

    applyLetterbox: bool = False
    paddingRed: int = 0
    paddingGreen: int = 0
    paddingBlue: int = 0
