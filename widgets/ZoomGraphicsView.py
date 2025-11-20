from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QMouseEvent, QWheelEvent
from PySide6.QtCore import Qt

from widgets import *

class ZoomGraphicsView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, onGraphicsItemClickSlot_fn, parent=None):
        super().__init__(scene, parent)

        self._scene: QGraphicsScene = scene
        self._zoom: float = 0
        self._zoomStep: float = 1.25
        self._zoomRange: float = (-20, 20)
        self.selectedItem: ImageLabelBox = None
        self.onGraphicsItemClickSlot_fn = onGraphicsItemClickSlot_fn

        self._hScrollConst: float = 2.0
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

    def wheelEvent(self, event: QWheelEvent):
        if (event.modifiers() == Qt.KeyboardModifier.ControlModifier):
            if event.angleDelta().y() > 0:
                zoomFactor = self._zoomStep
                self._zoom += 1
            else:
                zoomFactor = 1 / self._zoomStep
                self._zoom -= 1

            if self._zoom < self._zoomRange[0]:
                self._zoom = self._zoomRange[0]
                return
            elif self._zoom > self._zoomRange[1]:
                self._zoom = self._zoomRange[1]
                return

            self.scale(zoomFactor, zoomFactor)
        elif (event.modifiers() == Qt.KeyboardModifier.ShiftModifier):
            delta = event.angleDelta().y()
            scrollStep = -delta / self._hScrollConst
            hbar = self.horizontalScrollBar()
            hbar.setValue(hbar.value() + scrollStep)
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if(event.button() == Qt.MouseButton.LeftButton): 
            item: ImageLabelBox = self.itemAt(event.pos())
            
            if(self.selectedItem is not None):
                self.selectedItem.setSelected(False)
                self.selectedItem = None
                self.onGraphicsItemClickSlot_fn()

            if item:
                self.selectedItem = item
                item.setSelected(True)
                
        elif(event.button() == Qt.MouseButton.RightButton):
            if(self.selectedItem is not None):
                self.selectedItem.setSelected(False)
                self.selectedItem = None

        return super().mousePressEvent(event)

    def resetZoom(self) -> None:
        self._zoom = 0
