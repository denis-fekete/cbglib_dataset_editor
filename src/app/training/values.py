"""
Module: Settings.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Values for GUI.
"""

YOLO_V8_N_MODEL_INDEX = 0
YOLO_V8_M_MODEL_INDEX = 1
YOLO_V11_N_MODEL_INDEX = 2
YOLO_V11_M_MODEL_INDEX = 3
YOLO_V26_N_MODEL_INDEX = 4
YOLO_V26_N_SEG_MODEL_INDEX = 20
FASTER_RCNN_MODEL_INDEX = 30

MODELS_NAMES = {
    YOLO_V8_N_MODEL_INDEX: "Yolo 8 Nano from Ultralytics",
    YOLO_V8_M_MODEL_INDEX: "Yolo 11 Medium from Ultralytics",
    YOLO_V11_N_MODEL_INDEX: "Yolo 11 Nano from Ultralytics",
    YOLO_V11_M_MODEL_INDEX: "Yolo 11 Medium from Ultralytics",
    YOLO_V26_N_MODEL_INDEX: "Yolo 26 Nano from Ultralytics",
    YOLO_V26_N_SEG_MODEL_INDEX: "Yolo 26 Nano Segment from Ultralytics",
    FASTER_RCNN_MODEL_INDEX: "Faster RCNN",
}


DATASET_PATHS = {
    0: "Dataset export path",
    1: "Dataset import path",
}
