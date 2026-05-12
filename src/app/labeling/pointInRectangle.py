"""
Module: pointInRectangle.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Simple function called for getting whenever an point is inside of a rectangle.
"""

from PySide6.QtCore import QPointF, QRectF


# Non rotated rectangles
def pointInRectangle(point: QPointF, rect: QRectF) -> bool:
    """Returns True/False whenever a point lies in rectangle"""

    xStatement = point.x() >= rect.x() and point.x() <= rect.x() + rect.width()
    yStatement = point.y() >= rect.y() and point.y() <= rect.y() + rect.height()
    return xStatement and yStatement
