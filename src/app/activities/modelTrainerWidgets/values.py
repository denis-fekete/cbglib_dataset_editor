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
FASTER_RCNN_MODEL_INDEX = 5

MODELS_NAMES = {
    YOLO_V8_N_MODEL_INDEX: "Yolo V8 N (Ultralytics)",
    YOLO_V8_M_MODEL_INDEX: "Yolo V8 M (Ultralytics)",
    YOLO_V11_N_MODEL_INDEX: "Yolo V11 N (Ultralytics)",
    YOLO_V11_M_MODEL_INDEX: "Yolo V11 M (Ultralytics)",
    YOLO_V26_N_MODEL_INDEX: "Yolo V26 N (Ultralytics)",
    FASTER_RCNN_MODEL_INDEX: "Faster RCNN",
}


DATASET_PATHS = {
    0: "Dataset export path",
    1: "Dataset import path",
}
