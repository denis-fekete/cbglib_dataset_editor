from PySide6.QtCore import QPointF, QRectF

# Non rotated rectangles
def pointInRectangle(point: QPointF, rect: QRectF) -> bool:
    """Returns True/False whenever a point lies in rectangle"""

    xStatement = point.x() >= rect.x() and point.x() <= rect.x() + rect.width()
    yStatement = point.y() >= rect.y() and point.y() <= rect.y() + rect.height()
    return xStatement and yStatement

# Rotated rectangles
# def pointInRectangle(point: QPointF, rect: QRectF) -> bool:
#     return ( 
#         # Top line of rectangle
#         pointOnLeftSide(point, rect.x(), rect.y(), rect.x() + rect.width(), rect.y()) and
#         # Right line
#         pointOnLeftSide(point, rect.x() + rect.width(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()) and
#         # Bottom line
#         pointOnLeftSide(point, rect.x() + rect.width(), rect.y() + rect.height(), rect.x(), rect.y() + rect.height()) and
#         # Left line
#         pointOnLeftSide(point, rect.x(), rect.y() + rect.height(), rect.x(), rect.y())
#     )

# def pointOnLeftSide(point: QPointF, startX: float, startY: float, endX: float, endY: float) -> bool:
#     res = (endX - startX) * (point.y() - startY) - (point.x() - startX) * (endY - startY)
#     return (res >= 0)