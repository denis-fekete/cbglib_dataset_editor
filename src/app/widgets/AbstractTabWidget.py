"""
Module: AbstractTabWidget
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Abstract class for activities widgets, used mainly for common implementation of `tabSelected` and `tabClosed` methods.
"""

from PySide6.QtWidgets import QWidget


class AbstractTabWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def tabSelected(self) -> None:
        pass

    def tabClosed(self) -> None:
        pass

    def updateSettings(self) -> None:
        pass

    def loadSettings(self) -> None:
        pass
