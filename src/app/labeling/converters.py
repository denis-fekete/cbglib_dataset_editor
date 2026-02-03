"""
Module: converters.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    File containing functions for converting different types of data used in this project, example:
    Image representation in OpenCV <-> Image representation in Qt
"""

import cv2 as cv

from PySide6.QtGui import QImage


def Mat2QImage(mat: cv.Mat | None) -> QImage:
    if mat is None:
        return QImage()

    h, w, ch = mat.shape
    bytesPerLine = ch * w

    rgbMat = cv.cvtColor(mat, cv.COLOR_BGR2RGB)
    qimage = QImage(rgbMat.data, w, h, bytesPerLine, QImage.Format_RGB888)  # type: ignore

    return qimage


def Norm2Pixels(
    x: float, y: float, w: float, h: float, imgW: float, imgH: float
) -> tuple[float, float, float, float]:
    """
    Converts normalized coordinate and dimension values into the pixel format. Example:\n
    x:0.5 y:0.5 w:0.1 h:0.1 for image 1000x1000 -> x:500 y:500 w:100 h:100
    """
    pixX = imgW * x
    pixY = imgH * y
    pixW = imgW * w
    pixH = imgH * h
    return pixX, pixY, pixW, pixH


def Pixels2Norm(
    x: float, y: float, w: float, h: float, imgW: float, imgH: float
) -> tuple[float, float, float, float]:
    """
    Converts pixel coordinate and dimension values into the normalized format. Example:\n
    x:500 y:500 w:100 h:100 for image 1000x1000 -> x:0.5 y:0.5 w:0.1 h:0.1
    """
    normX = x / imgW
    normY = y / imgH
    normW = w / imgW
    normH = h / imgH
    return normX, normY, normW, normH
