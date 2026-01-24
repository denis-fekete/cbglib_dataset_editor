# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pylint: skip-file

from PySide6.QtCore import Signal, Slot

from pathlib import Path

from ultralytics import YOLO  # type: ignore
from ultralytics.data.utils import check_det_dataset

from .AbstractModelTrainer import AbstractModelTrainer


class YoloUltralyticsTrainer(AbstractModelTrainer):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    errorExit = Signal(str)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.connectedToThread: bool = False
        self.epochs: int | None = None
        self.workers: int | None = None
        self.batch: int | None = None
        self._validated: bool = False
        self.modelPath: str | None = None
        self.modelName: str | None = None
        self.dataYaml: str | None = None

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
            model = YOLO("yolov8n.pt")

            model.add_callback("on_train_epoch_end", self._epochCallback)  # type: ignore
            model.add_callback("on_train_start", self._trainStartCallback)  # type: ignore
            model.add_callback("on_train_end", self._trainEndCallback)  # type: ignore

            model.train(  # type: ignore
                data=self.dataYaml,
                epochs=self.epochs,
                imgsz=640,
                batch=self.batch,
                workers=self.workers,
                project=self.modelPath,
                name=self.modelName,
            )

            model.export(format="onnx")

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
