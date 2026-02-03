"""
Module:
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class that is analyzes image and performs object detection, its main function is to help with
    automatic labeling of data in data labeling part of this application.
"""

import cv2 as cv
import numpy as np
from typing import Tuple
from numpy.typing import NDArray

from .ONNXModel import ONNXModel
from .LetterboxInfo import LetterboxInfo
from .Detection import Detection


class ImageAnalyzer:
    def __init__(
        self,
        modelPath: str,
        modelInputSize: int,
        paddingValue: Tuple[int, int, int],
        confidenceThreshold: float,
        iouThreshold: float,
    ) -> None:
        """
        :param modelPath: String path to the .onnx model
        :type modelPath: str
        :param modelInputSize: Image size that is expected by model, in this configuration 1:1
        aspect ratio is expected
        :type modelInputSize: int
        :param paddingValue: Scalar of Tuple of RGB values to be put as padding for letter-boxing
        :type paddingValue: Tuple[int, int, int]
        :param confidenceThreshold: Threshold for class score confidences, if confidence is below
        this value a detection will be discarded
        :type confidenceThreshold: float
        :param iouThreshold: Intersection Over Union threshold, threshold for area of two detection
        to be that are crossing each other, used for applying Non Maximum Suppression
        :type iouThreshold: float
        """
        self.modelPath: str = modelPath
        self.modelInputSize: int = modelInputSize
        self.paddingValue: Tuple[int, int, int] = paddingValue
        self.letterBoxInfo: LetterboxInfo | None = None
        self.confidenceThreshold = confidenceThreshold
        self.iouThreshold = iouThreshold
        self.model = ONNXModel(self.modelPath)

    def analyze(self, image: cv.Mat) -> list[Detection]:
        """
        Method called for analyzing and getting list of detections as result

        :param image: Input image onto which a object detection will be performed
        :type image: cv.Mat
        :return: List of Detection objects containing objects that the model detected
        :rtype: list[Detection]
        """
        self.image: cv.Mat = image
        resized, letterboxInfo = self.resizeAndLetterBox(self.image)
        converted = self.toTensor(resized)
        boxes, confidences, classes = self.model.run(
            converted, self.confidenceThreshold, letterboxInfo
        )
        detections = self.applyNMS(boxes, confidences, classes)

        return detections

    def resizeAndLetterBox(
        self, image: cv.Mat
    ) -> Tuple[cv.typing.MatLike, LetterboxInfo]:
        """
        Resizes `image` into expected input model dimensions while keeping aspect ration 1:1 and applies letterboxing if input had wrong aspect ration.

        Returns a letterboxed `MatLike`
        """
        height, width = image.shape[:2]

        scale = self.modelInputSize / max(width, height)

        newWidth, newHeight = int(width * scale), int(height * scale)

        resized = cv.resize(image, (newWidth, newHeight))

        paddingW = self.modelInputSize - newWidth
        paddingH = self.modelInputSize - newHeight

        left, right = paddingW // 2, paddingW - paddingW // 2
        top, bottom = paddingH // 2, paddingH - paddingH // 2

        letterBoxed = cv.copyMakeBorder(
            resized,
            top,
            bottom,
            left,
            right,
            cv.BORDER_CONSTANT,
            value=self.paddingValue,
        )

        return letterBoxed, LetterboxInfo(scale, left, top)

    def toTensor(self, image: cv.typing.MatLike) -> NDArray[np.float32]:
        """
        Converts input image `MatLike` to expected input model, in this case a tensor

        Returns a tensor in as `NDArray[np.float32]`
        """
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        normalized = rgb.astype(np.float32) / 255.0

        # convert normalized image from HWC into CHW format that is expected by model
        chw = np.transpose(normalized, (2, 0, 1))

        # add batch dimension
        # (3, modelInputSize, modelInputSize) -> (1, 3, modelInputSize, modelInputSize)
        return np.expand_dims(chw, axis=0)

    def applyNMS(
        self,
        boxes: list[Tuple[int, int, int, int]],
        confidences: list[float],
        classes: list[int],
    ) -> list[Detection]:
        indices = cv.dnn.NMSBoxes(
            boxes,
            confidences,
            score_threshold=self.confidenceThreshold,
            nms_threshold=self.iouThreshold,
        )

        detections: list[Detection] = []
        if len(indices) > 0:
            indices = indices.flatten()  # type: ignore

        for i in indices:  # type: ignore
            x, y, w, h = boxes[i]
            clsId = classes[i]
            conf = confidences[i]
            detections.append(Detection(x + w / 2, y + h / 2, w, h, clsId, conf))
        return detections
