"""
Module: ImageScene
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Derived class from QGraphicsScene that draws a bitmap image onto the QGraphicsScene.
"""

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QRectF, QRect
from PySide6.QtGui import QPixmap, QPainter


class ImageScene(QGraphicsScene):
    def __init__(self, pixmap: QPixmap | None = None):
        super().__init__()
        self._pixmap: QPixmap | None = pixmap

    def drawBackground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        if self._pixmap != None:
            painter.drawPixmap(
                QRect(0, 0, int(self.width()), int(self.height())), self._pixmap
            )

    def setPixmap(self, pixmap: QPixmap) -> None:
        self._pixmap = pixmap
        self.update()
