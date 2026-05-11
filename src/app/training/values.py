"""
Module: Settings.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Training model options for UI.
"""

CUSTOM_MODEL = 0
YOLO_V8_N_MODEL_INDEX = CUSTOM_MODEL + 1
YOLO_V8_S_MODEL_INDEX = YOLO_V8_N_MODEL_INDEX + 1
YOLO_V8_M_MODEL_INDEX = YOLO_V8_S_MODEL_INDEX + 1
YOLO_V11_N_MODEL_INDEX = YOLO_V8_M_MODEL_INDEX + 1
YOLO_V11_S_MODEL_INDEX = YOLO_V11_N_MODEL_INDEX + 1
YOLO_V11_M_MODEL_INDEX = YOLO_V11_S_MODEL_INDEX + 1
YOLO_V26_N_MODEL_INDEX = YOLO_V11_M_MODEL_INDEX + 1
YOLO_V26_S_MODEL_INDEX = YOLO_V26_N_MODEL_INDEX + 1
YOLO_V26_M_MODEL_INDEX = YOLO_V26_S_MODEL_INDEX + 1

MODELS_NAMES = {
    CUSTOM_MODEL: "Custom .pt model",
    YOLO_V8_N_MODEL_INDEX: "Yolo 8 Nano from Ultralytics",
    YOLO_V8_S_MODEL_INDEX: "Yolo 8 Small from Ultralytics",
    YOLO_V8_M_MODEL_INDEX: "Yolo 8 Medium from Ultralytics",
    YOLO_V11_N_MODEL_INDEX: "Yolo 11 Nano from Ultralytics",
    YOLO_V11_S_MODEL_INDEX: "Yolo 11 Small from Ultralytics",
    YOLO_V11_M_MODEL_INDEX: "Yolo 11 Medium from Ultralytics",
    YOLO_V26_N_MODEL_INDEX: "Yolo 26 Nano from Ultralytics",
    YOLO_V26_S_MODEL_INDEX: "Yolo 26 Small from Ultralytics",
    YOLO_V26_M_MODEL_INDEX: "Yolo 26 Medium from Ultralytics",
}


DATASET_PATHS = {
    0: "Dataset export path",
    1: "Dataset import path",
}
