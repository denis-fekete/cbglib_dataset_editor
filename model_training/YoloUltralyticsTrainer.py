from PySide6.QtCore import Signal, Slot
from PySide6 import QtWidgets

from pathlib import Path

from ultralytics import YOLO
from ultralytics.data.utils import check_det_dataset

from .AbstractModelTrainer import AbstractModelTrainer

class YoloUltralyticsTrainer(AbstractModelTrainer):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    errorExit = Signal(str)
    finished = Signal()

    def __init__(self):
        super().__init__()
        
        self.connectedToThread = False
        self.epochs = None
        self.workers = None
        self.batch = None
        self._validated = False
        self.modelPath = None
        self.modelName = None


    @Slot()
    def run(self):
        if(self.dataYaml is None):
            self.errorExit.emit("data.yaml was not set")
            return
        elif(self.epochs is None):
            self.errorExit.emit("Number of epochs was not set")
            return
        elif(self.workers is None):
            self.errorExit.emit("Number of workers was not set")
            return
        elif(self.workers is None):
            self.errorExit.emit("Batch size was not set")
            return
        elif(self.modelName is None):
            self.errorExit.emit("Model name was not set")
            return
        elif(self.modelPath is None):
            self.errorExit.emit("Model path was not set")
            return

        self.status.emit("Initializing ultralytics...")
        try:
            model = YOLO("yolov8n.pt")

            model.add_callback("on_train_epoch_end", self._epochCallback)
            model.add_callback("on_train_start", self._trainStartCallback)
            model.add_callback("on_train_end", self._trainEndCallback)

            model.train(
                data=self.dataYaml,
                epochs=self.epochs,
                imgsz=640,
                batch=self.batch,
                workers=self.workers,
                project=self.modelPath,
                name=self.modelName,
            )

            self.finished.emit()

        except Exception as e:
            self.errorExit.emit(str(e))
            return

    def _epochCallback(self, trainer):
        msg = (
            f"Epoch {trainer.epoch + 1}/{trainer.epochs}\n"
        )
        self.status.emit(msg)

    def _trainStartCallback(self, trainer):
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

    def _trainEndCallback(self, trainer):
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


    def validateDataset(self, datasetPath):
        try:
            fullPath = Path(datasetPath) / "data.yaml"
            result = check_det_dataset(fullPath.resolve()._str, autodownload=False)
            self._validated = True
            self.dataYaml = fullPath.resolve()._str
            return True, f"{result}"
        except Exception as e:
            self._validated = False
            return False, f"{str(e)}"