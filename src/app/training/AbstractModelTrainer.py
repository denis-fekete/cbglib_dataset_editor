"""
Module: AbstractModelTrainer.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Abstract class for model trainers that is supposed to supply shared interface between trainers.
"""

from PySide6.QtCore import QObject, Signal
from abc import ABCMeta, abstractmethod


class ABCQObjectMeta(ABCMeta, type(QObject)):
    pass


class AbstractModelTrainer(QObject, metaclass=ABCQObjectMeta):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    errorExit = Signal(str)
    finished = Signal()

    connectedToThread: bool = False
    epochs: int | None
    workers: int | None
    batch: int | None
    modelPath: str | None
    modelName: str | None

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run(self) -> None:
        """Run the training loop. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def validateDataset(self, datasetPath: str) -> tuple[bool, str]:
        """Method returns `tuple[true, '']` on successfully validated dataset or `tuple[false, errorMessage]` on fail"""
        pass

    @abstractmethod
    def exportONNX(self):
        """Exports trained model into ONNX format"""
        pass
