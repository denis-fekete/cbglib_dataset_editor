from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QFont, QMouseEvent
from PySide6.QtCore import Qt, QRectF, QPointF

from utils.pointInRectangle import pointInRectangle

class ImageLabelBox(QtWidgets.QGraphicsItem):
    def __init__(self, rect: QRectF, label: int, labelText: str, handle_fn, imageRect: QRectF, selectedColor: QColor = None, defaultColor: QColor = None):
        super().__init__()

        self.label: int = label
        self.labelText: str = labelText
        self.imageRect: QRectF = imageRect

        self.w: float = rect.width()
        self.h: float = rect.height()
        self._wHalf: float = self.w/2
        self._hHalf:float = self.h/2
        self.setPos(rect.x(), rect.y())

        # if handle_fn is not provided create lambda function that return 50 as a default value
        self._handle_fn = handle_fn if (handle_fn is not None) else (lambda: 50)
        self._handleSize: float = self._handle_fn()

        self.updateColors(defaultColor, selectedColor)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True) 
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self._isBeingDragged: bool = False
        self._isBeingResized: bool = False
        self._offset: QRectF = QRectF()

        self._topLeftMoving: bool = False
        self._topRightMoving: bool = False
        self._bottomRightMoving: bool = False
        self._bottomLeftMoving: bool = False

    def paint(self, painter: QPainter, option, widget=None):
        self._handleSize = self._handle_fn()

        if(self.isSelected()):
            self._pen.setColor(self._selectedColor)
            self._backgroundBrush.setColor(self._selectedColor)
            self._handleBrush.setColor(self._selectedColor)
        else:
            self._pen.setColor(self._defaultColor)
            self._backgroundBrush.setColor(self._defaultColor)
            self._handleBrush.setColor(self._defaultColor)

        painter.setPen(self._pen)
            
        painter.setOpacity(0.5)
        painter.setBrush(self._backgroundBrush)
            
        painter.drawRect(QRectF(-self._wHalf,
                                -self._hHalf,
                                self.w,
                                self.h))

        painter.setOpacity(0.7)
        painter.setBrush(self._handleBrush)

        painter.drawRect(self.getTopLeftRect())        
        painter.drawRect(self.getTopRightRect())
        painter.drawRect(self.getBottomRightRect())
        painter.drawRect(self.getBottomLeftRect())

        painter.setFont(QFont("Arial", min(max(self.w * 0.1, 20), 80)))
        painter.drawText(   self.getTextRect(), 
                            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                            str(self.labelText))

    def boundingRect(self) -> QRectF:
        return QRectF(-self._wHalf - self._penWidth,
                      -self._hHalf - self._penWidth,
                      self.w + self._penWidth,
                      self.h + self._penWidth)
    
    def shape(self) -> QPainterPath:
        path: QPainterPath = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def getTopLeftRect(self) -> QRectF:
        return QRectF(  -self._wHalf, 
                        -self._hHalf,
                        self._handleSize,
                        self._handleSize)
    
    def getTopRightRect(self) -> QRectF:
        return QRectF(  self._wHalf - self._handleSize,
                        -self._hHalf,
                        self._handleSize,
                        self._handleSize)
    
    def getBottomLeftRect(self) -> QRectF:
        return QRectF(  -self._wHalf,
                         self._hHalf - self._handleSize,
                         self._handleSize,
                         self._handleSize)

    def getBottomRightRect(self) -> QRectF:
        return QRectF(  self._wHalf - self._handleSize, 
                        self._hHalf - self._handleSize,
                        self._handleSize,
                        self._handleSize)

    def getTextRect(self) -> QRectF:
        return QRectF(  -self._wHalf + self._handleSize, 
                        -self._hHalf,
                        self._wHalf,
                        self._hHalf)

    def mousePressEvent(self, event: QMouseEvent):
        if(event.button() == Qt.MouseButton.LeftButton):  
            self._isBeingResized = True

            if(pointInRectangle(event.pos(), self.getTopLeftRect())):
                self._topLeftMoving = True
                self._offset = self.getTopLeftRect().topLeft() - event.pos()
            elif(pointInRectangle(event.pos(), self.getTopRightRect())):
                self._topRightMoving = True 
                self._offset = self.getTopRightRect().topRight() - event.pos()
            elif(pointInRectangle(event.pos(), self.getBottomRightRect())):
                self._bottomRightMoving = True
                self._offset = self.getBottomRightRect().bottomRight() - event.pos()
            elif(pointInRectangle(event.pos(), self.getBottomLeftRect())):
                self._bottomLeftMoving = True
                self._offset = self.getBottomLeftRect().bottomLeft() - event.pos()
            else:
                self._offset = event.pos()
                self._isBeingResized = False
                self._isBeingDragged = True
            self.update()

            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if (self._isBeingDragged):
            newPos = self.mapToScene(event.pos() - self._offset)
            self.setPos(newPos)
        elif (self._isBeingResized):
            movePointX = event.scenePos().x() + self._offset.x()
            movePointY = event.scenePos().y() + self._offset.y()

            if(self._topLeftMoving):
                # anchor is bottom right
                anchorPointX = self.x() + self._wHalf
                anchorPointY = self.y() + self._hHalf

                newWidth = abs(anchorPointX - movePointX)
                newHeight = abs(anchorPointY - movePointY)
                newCenterX = anchorPointX - newWidth/2
                newCenterY = anchorPointY - newHeight/2
            elif(self._topRightMoving):
                # anchor is bottom left
                anchorPointX = self.x() - self._wHalf
                anchorPointY = self.y() + self._hHalf

                newWidth = abs(anchorPointX - movePointX)
                newHeight = abs(anchorPointY - movePointY)
                newCenterX = anchorPointX + newWidth/2
                newCenterY = anchorPointY - newHeight/2
            elif(self._bottomRightMoving):
                # anchor is top left
                anchorPointX = self.x() - self._wHalf
                anchorPointY = self.y() - self._hHalf

                newWidth = abs(anchorPointX - movePointX)
                newHeight = abs(anchorPointY - movePointY)
                newCenterX = anchorPointX + newWidth/2
                newCenterY = anchorPointY + newHeight/2
            elif(self._bottomLeftMoving):
                # anchor is top right
                anchorPointX = self.x() + self._wHalf
                anchorPointY = self.y() - self._hHalf
                newWidth = abs(anchorPointX - movePointX)
                newHeight = abs(anchorPointY - movePointY)
                newCenterX = anchorPointX - newWidth/2
                newCenterY = anchorPointY + newHeight/2
            else:
                raise Exception("Error: Mouse event for resizing was triggered not by handle rectangles!")
            
            tmpX = self.x()
            tmpY = self.y()

            if(movePointX >= self.imageRect.x() and movePointX <= self.imageRect.x() + self.imageRect.width()):
                tmpX = newCenterX
                self.w = newWidth
                self._wHalf = self.w/2

            if(movePointY >= self.imageRect.y() and movePointY <= self.imageRect.y() + self.imageRect.height()):
                tmpY = newCenterY
                self.h = newHeight
                self._hHalf = self.h/2

            self.setPos(QPointF(tmpX, tmpY))

            self.update()
        event.accept()
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if(event.button() == Qt.MouseButton.LeftButton): 
            self._isBeingDragged = False
            self._isBeingResized = False
            self._topLeftMoving = False
            self._topRightMoving = False
            self._bottomRightMoving = False
            self._bottomLeftMoving = False
        self.update()
        event.accept()
        # return super().mouseReleaseEvent(event)

    def rect(self) -> QRectF:
        return QRectF(self.x(), self.y(), self.width(), self.height())
    
    def getLabel(self) -> int:
        return self.label

    def setLabel(self, label: int, labelText: str) -> None:
        """Sets label and labelText of ImageLabelBox"""
        self.label = label
        self.labelText = labelText
        self.update()

    def updateColors(self, defaultColor, selectedColor):
        self._defaultColor: QColor = defaultColor if (defaultColor is not None and defaultColor.isValid()) else QColor(40, 40, 40) 
        self._selectedColor: QColor = selectedColor if (selectedColor is not None and selectedColor.isValid()) else QColor(100, 100, 255)

        self._penWidth: float = 5
        self._pen: QPen = QPen(QBrush(self._defaultColor), self._penWidth, s=Qt.PenStyle.SolidLine)

        self._backgroundBrush: QBrush = QBrush(self._defaultColor, Qt.BrushStyle.BDiagPattern)
        self._handleBrush: QBrush = QBrush(self._defaultColor, Qt.BrushStyle.SolidPattern)

        self.update()

    def width(self) -> float:
        return self.w
    
    def height(self) -> float:
        return self.h
