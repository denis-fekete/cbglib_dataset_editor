from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QRect

class ImageScene(QGraphicsScene):
    def __init__(self, pixmap=None):
        super().__init__()
        self._pixmap = pixmap
        
    def drawBackground(self, painter, rect):
        if(self._pixmap != None):
            painter.drawPixmap(QRect(0, 0, self.width(), self.height()),
                           self._pixmap)
        
    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()