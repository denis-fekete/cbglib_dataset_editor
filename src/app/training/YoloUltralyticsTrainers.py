from ultralytics import YOLO  # type: ignore
from .AbstractYoloUltralyticsTrainer import AbstractYoloUltralyticsTrainer


class YoloUltralyticsTrainerV8n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolov8n.pt"))


class YoloUltralyticsTrainerV8m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolov8m.pt"))


class YoloUltralyticsTrainerV11n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo11n.pt"))


class YoloUltralyticsTrainerV11m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo11m.pt"))


class YoloUltralyticsTrainerV26n(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo26n.pt"))


class YoloUltralyticsTrainerV26m(AbstractYoloUltralyticsTrainer):
    def __init__(self):
        super().__init__(model=YOLO("yolo26m.pt"))
