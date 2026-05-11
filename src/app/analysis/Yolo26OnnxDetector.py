# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: ignore[reportUnknownArgumentType]
# pylint: skip-file

"""
Module: ONNXModel.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    ONNX Runtime wrapper that initializes model, and puts runs the object detection. Separation
    from ImageAnalyzer is done because the onnxruntime library does not contain hints for pyright
    and pylint used in this projects, therefore a ImageAnalyzer can be statically controlled only
    this file is excepted from control.
"""

from typing import Tuple

from .LetterboxInfo import LetterboxInfo
from .YoloOnnxDetector import YoloOnnxDetector


class Yolo26OnnxDetector(YoloOnnxDetector):
    def __init__(self, modelPath: str):
        super().__init__(modelPath)

    def _extractDetections(
        self, outputsList, threshold: float, letterboxInfo: LetterboxInfo
    ) -> Tuple[list[Tuple[int, int, int, int]], list[float], list[int]]:
        # model returns list, get first and dispose of batch dimension
        outputs = outputsList[0][0]

        # contains det. boxes [x, y, w, h]
        # where x,y is top left corner
        boxes: list[Tuple[int, int, int, int]] = []
        confidences: list[float] = []
        classes: list[int] = []

        for det in outputs:
            confidence = det[4]

            if confidence < threshold:
                continue

            classId = det[5]
            left = det[0]
            top = det[1]
            right = det[2]
            bottom = det[3]
            width = right - left
            height = bottom - top

            # rescale to original
            left = int((left - letterboxInfo.paddingLeft) / letterboxInfo.scale)  # type: ignore
            top = int((top - letterboxInfo.paddingTop) / letterboxInfo.scale)  # type: ignore
            width = int(width / letterboxInfo.scale)  # type: ignore
            height = int(height / letterboxInfo.scale)  # type: ignore

            boxes.append((left, top, width, height))
            confidences.append(float(confidence))  # type: ignore
            classes.append(classId)  # type: ignore
        return boxes, confidences, classes
