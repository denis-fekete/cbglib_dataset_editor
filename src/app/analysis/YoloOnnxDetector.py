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

import onnxruntime as ort  # type: ignore
import cv2 as cv
from typing import Tuple
import numpy as np

from .LetterboxInfo import LetterboxInfo


class YoloOnnxDetector:
    def __init__(self, modelPath: str) -> None:
        providers = [
            "CPUExecutionProvider",
        ]

        sessionOptions = ort.SessionOptions()
        sessionOptions.log_severity_level = 0  # verbose logging
        sessionOptions.log_verbosity_level = 4  # most details

        self.model = ort.InferenceSession(
            modelPath, so=sessionOptions, providers=providers  # type: ignore
        )

    def run(self, image: cv.typing.MatLike, threshold: float, letterboxInfo: LetterboxInfo):
        """Runs `image` with ONNX Runtime model and returns its outputs"""
        input_name = self.model.get_inputs()[0].name
        output_name = self.model.get_outputs()[0].name

        outputsList = self.model.run([output_name], {input_name: image})
        return self._extractDetections(outputsList, threshold, letterboxInfo)

    def _extractDetections(
        self, outputsList, threshold: float, letterboxInfo: LetterboxInfo
    ) -> Tuple[list[Tuple[int, int, int, int]], list[float], list[int]]:
        # model returns list, get first and dispose of batch dimension
        outputs = outputsList[0][0]
        # transpose
        # from ([x, y, w, h, [class_scores]], number_of_detection)
        # to (number_of_detection, [x, y, w, h, [class_scores]])
        transposed = outputs.T

        # contains det. boxes [x, y, w, h]
        # where x,y is top left corner
        boxes: list[Tuple[int, int, int, int]] = []
        confidences: list[float] = []
        classes: list[int] = []

        for det in transposed:
            classConfidences = det[4:]
            classId = np.argmax(classConfidences)  # type: ignore
            confidence = classConfidences[classId]

            if confidence < threshold:
                continue

            x, y, w, h = det[:4]
            left: float = x - w / 2
            top: float = y - h / 2

            # rescale to original
            left = int((left - letterboxInfo.paddingLeft) / letterboxInfo.scale)  # type: ignore
            top = int((top - letterboxInfo.paddingTop) / letterboxInfo.scale)  # type: ignore
            w = int(w / letterboxInfo.scale)  # type: ignore
            h = int(h / letterboxInfo.scale)  # type: ignore

            boxes.append((left, top, w, h))
            confidences.append(float(confidence))  # type: ignore
            classes.append(classId)  # type: ignore
        return boxes, confidences, classes
