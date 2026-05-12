"""
Module: DatasetStatistics.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Collected and calculated statistic about dataset.
"""

from dataclasses import dataclass


@dataclass
class DatasetStatistics:
    """
    :param labelFiles: number of loaded `.txt` files.
    :param imageSamples: number of loaded image files.
    :param labeledSamples: number of `ImageSamples` with at least one label.
    :param emptySamples: number of loaded `ImageSamples`, with no labels.
    :param classes: number of loaded class from the `data.yaml` configuration file.
    :param labelBoxes: total number of loaded `LabelBox` objects, each representing single bounding box.
    :param trainSamples: number of samples used for training (in train directory)
    :param valSamples: number of samples used for validation (in val directory)
    :param valSamples: number of samples used for testing (in test directory)
    """

    labelsFiles: int = 0
    imageSamples: int = 0
    labeledSamples: int = 0
    emptySamples: int = 0
    classes: int = 0
    labelBoxes: int = 0
    trainSamples: int = 0
    valSamples: int = 0
    testSamples: int = 0
