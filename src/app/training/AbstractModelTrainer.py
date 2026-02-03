"""
Module: AbstractModelTrainer.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Abstract class for model trainers that is supposed to supply shared interface between trainers.
"""

from PySide6.QtCore import QObject, Signal


class AbstractModelTrainer(QObject):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
