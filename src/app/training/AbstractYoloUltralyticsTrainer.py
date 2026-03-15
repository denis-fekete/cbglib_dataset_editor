# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pylint: skip-file

"""
Module: YoloUltralyticsTrainer.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Class derived from `AbstractModelTrainer` that implements methods for Ultralytics Yolo model.
"""

from PySide6.QtCore import Slot

from pathlib import Path

from ultralytics.data.utils import check_det_dataset

from .AbstractModelTrainer import AbstractModelTrainer


class AbstractYoloUltralyticsTrainer(AbstractModelTrainer):
    def __init__(self, model) -> None:
        super().__init__()

        self._validated: bool = False
        self.dataYaml: str | None = None
        self.model = model

    @Slot()
    def run(self) -> None:
        if self.dataYaml is None:
            self.errorExit.emit("data.yaml was not set")
            return
        elif self.epochs is None:
            self.errorExit.emit("Number of epochs was not set")
            return
        elif self.workers is None:
            self.errorExit.emit("Number of workers was not set")
            return
        elif self.batch is None:
            self.errorExit.emit("Batch size was not set")
            return
        elif self.modelName is None:
            self.errorExit.emit("Model name was not set")
            return
        elif self.modelPath is None:
            self.errorExit.emit("Model path was not set")
            return

        self.status.emit("Initializing ultralytics...")
        try:
            self.model.add_callback("on_train_epoch_end", self._epochCallback)  # type: ignore
            self.model.add_callback("on_train_start", self._trainStartCallback)  # type: ignore
            self.model.add_callback("on_train_end", self._trainEndCallback)  # type: ignore

            self.model.train(  # type: ignore
                data=self.dataYaml,
                epochs=self.epochs,
                imgsz=640,
                batch=self.batch,
                workers=self.workers,
                project=self.modelPath,
                name=self.modelName,
            )

            self.model.export(format="onnx")

            self.finished.emit()

        except Exception as e:
            self.errorExit.emit(str(e))
            return

    def _epochCallback(self, trainer) -> None:
        msg = f"Epoch {trainer.epoch + 1}/{trainer.epochs}\n"
        self.status.emit(msg)

    def _trainStartCallback(self, trainer) -> None:
        args = trainer.args

        msg = (
            "------- TRAINING START -------\n"
            f"Model: {trainer.model.__class__.__name__}\n"
            f"Epochs: {args.epochs}\n"
            f"Batch size: {args.batch}\n"
            f"Image size: {args.imgsz}\n"
            f"Workers: {args.workers}\n"
            f"Device: {args.device}\n"
            f"Save dir: {trainer.save_dir}\n"
        )

        self.status.emit(msg)

    def _trainEndCallback(self, trainer) -> None:
        best = trainer.best
        last = trainer.last

        msg = (
            "------- TRAINING FINISHED -------\n"
            f"Best model: {best}\n"
            f"Last model: {last}\n"
            f"Results saved to:\n{trainer.save_dir}\n"
        )

        self.progress.emit(100)
        self.status.emit(msg)

    def validateDataset(self, datasetPath: str) -> tuple[bool, str]:
        try:
            fullPath = Path(datasetPath) / "data.yaml"
            result = check_det_dataset(str(fullPath.resolve()), autodownload=False)

            self._validated = True
            self.dataYaml = str(fullPath.resolve())

            return True, f"{str(result)}"
        except Exception as e:
            self._validated = False
            return False, f"{str(e)}"
