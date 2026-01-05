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
