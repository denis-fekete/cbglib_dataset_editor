"""
Module: Box.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Data class object used for storing Bounding box of ImageSamples, detected objects etc... This
    file is more of an syntactic sugar and  could be replaced by a Tuple, Dict or QRectF.
"""

from dataclasses import dataclass


@dataclass
class Box:
    """
    X and Y coordinate positions are centered, meaning left corner would be calculated like this:
    Top left corner = x - width / 2, y - width / 2
    """

    x: float
    y: float
    width: float
    height: float
