"""
Module: Detection.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Data class describing detected object using computer vision
"""

from dataclasses import dataclass


@dataclass
class Detection:
    """
    Data class object defining found Detection

    :var xCenter: x position of detection/bounding box, centered = middle of detection
    :vartype xCenter: float
    :var yCenter: y position of detection/bounding box, centered = middle of detection
    :vartype yCenter: float
    :var width: width of detection
    :vartype width: float
    :var height: height of detection
    :vartype height: float
    :var classIndex: integer value of class this detection has highest confidence score
    :vartype classIndex: int
    :var score: confidence score for detection
    :vartype score: float
    """

    xCenter: float
    yCenter: float
    width: float
    height: float
    classIndex: int
    score: float
