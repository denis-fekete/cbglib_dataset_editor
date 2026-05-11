from ultralytics import YOLO  # type: ignore
from .AbstractYoloUltralyticsTrainer import AbstractYoloUltralyticsTrainer

"""
Module: Settings.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Definition of different trainers for different models from the Ultralytics.
"""


class YoloUltralyticsTrainerV8n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolov8n.pt"))


class YoloUltralyticsTrainerV8s(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolov8s.pt"))


class YoloUltralyticsTrainerV8m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolov8m.pt"))


class YoloUltralyticsTrainerV11n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo11n.pt"))


class YoloUltralyticsTrainerV11s(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo11s.pt"))


class YoloUltralyticsTrainerV11m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo11m.pt"))


class YoloUltralyticsTrainerV26n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo26n.pt"))


class YoloUltralyticsTrainerV26s(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo26s.pt"))


class YoloUltralyticsTrainerV26m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo26m.pt"))


class CustomYoloUltralyticsTrainer(AbstractYoloUltralyticsTrainer):
    def __init__(self, path: str):
        super().__init__(model=YOLO(path))
