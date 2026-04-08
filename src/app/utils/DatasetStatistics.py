"""
Module: SharedValues.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Global variables as a single instance 'static' function getter that is used in application.
"""

from dataclasses import dataclass


@dataclass
class DatasetStatistics:
    labelsFiles: int = 0
    imageSamples: int = 0
    labeledSamples: int = 0
    emptySamples: int = 0
    classes: int = 0
    labelBoxes: int = 0
    trainSamples: int = 0
    valSamples: int = 0
    testSamples: int = 0
