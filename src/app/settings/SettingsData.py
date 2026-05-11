"""
Module: SettingsData.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Data class object containing saved settings values.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from app.synthetic import FilterPreset


@dataclass_json
@dataclass
class DatasetSettings:
    generateNames: bool
    separateToSubdirectories: bool
    generateSyntheticTrain: bool
    generateSyntheticVal: bool
    trainDataPercent: int
    importPath: str
    workers: int
    exportOriginal: bool


@dataclass_json
@dataclass
class LabelingSettings:
    selectedColorRed: int
    selectedColorGreen: int
    selectedColorBlue: int
    defaultColorRed: int
    defaultColorGreen: int
    defaultColorBlue: int
    modelPath: str
    autoDetectUsingYolo26: bool
    autoDetectThreshold: int


@dataclass_json
@dataclass
class TrainingSettings:
    model: int
    numberOfWorkers: int
    numberOfEpochs: int
    batchSize: int
    patience: int
    modelOutputPath: str
    onnxExport: bool


@dataclass_json
@dataclass
class SyntheticSettings:
    filters: list[FilterPreset]


@dataclass_json
@dataclass
class AppSettings:
    dataset: DatasetSettings
    labeling: LabelingSettings
    training: TrainingSettings
    syntheticSettings: SyntheticSettings
