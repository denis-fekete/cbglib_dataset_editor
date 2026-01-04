from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QTextCursor

import os
from pathlib import Path
from datetime import datetime


from widgets import *
from image_manipulation import *
from utils import *
from data_classes import SharedValues
from model_training import YoloUltralyticsTrainer, AbstractModelTrainer

class ModelTrainer(QtWidgets.QWidget):
    def __init__(self, setTabsEnabled_fn):
        super().__init__()
        self.pathValidated : bool = False
        self.setTabsEnabled_fn = setTabsEnabled_fn
        self.thread : QtCore.QThread = None
        self.currentModelTrainer : AbstractModelTrainer = None
        self._initUI()

    YOLO_V8_MODEL_INDEX = 0
    YOLO_V11_MODEL_INDEX = 1
    FASTER_RCNN_MODEL_INDEX = 2
    MODELS = {
        0 : "Yolo V8 (Ultralytics)",
        1 : "Yolo V11 (Ultralytics)",
        2 : "Faster RCNN",
    }

    DATASET_PATHS = {
        0 : "Dataset export path",
        1 : "Dataset import path",
    }

    def _initUI(self):
        self.setLayout(QtWidgets.QGridLayout())
        
        self.currentModelTrainer = None

        self._initModelSelectorContainer()
        self._initSettingsContainer()
        self._initProgressContainer()

        self.layout().addWidget(self._modelSelectorContainer, 0, 0)
        self.layout().addWidget(self._settingsContainer, 1, 0)
        self.layout().addWidget(self._progressContainer, 2, 0)

    def _initModelSelectorContainer(self):
        self._modelSelectorContainer = QtWidgets.QWidget()
        self._modelSelectorContainer.setLayout(QtWidgets.QGridLayout())

        self.modelSelector = QtWidgets.QComboBox()
        for i in range(0, len(self.MODELS)):
            self.modelSelector.addItem(self.MODELS[i])

        self.modelSelector.currentIndexChanged.connect(self.modelChanged)

        self._modelSelectorContainer.layout().addWidget(QtWidgets.QLabel("Model selection:"), 0, 0)
        self._modelSelectorContainer.layout().addWidget(self.modelSelector, 1, 0)

    def _initSettingsContainer(self):
        self._settingsContainer = QtWidgets.QWidget()
        self._settingsContainer.setLayout(QtWidgets.QGridLayout())

        self._settingsLabel = QtWidgets.QLabel("Settings:")

        self._workerSpinBox = QtWidgets.QSpinBox()
        self._workerSpinBox.setValue(0);
        self._workerSpinBox.setMinimum(0);
        self._workerSpinBox.setMaximum(99999);

        self._epochsSpinBox = QtWidgets.QSpinBox()
        self._epochsSpinBox.setValue(20);
        self._epochsSpinBox.setMinimum(0);
        self._epochsSpinBox.setMaximum(99999);

        self._batchSpinBox = QtWidgets.QSpinBox()
        self._batchSpinBox.setValue(4);
        self._batchSpinBox.setMinimum(0);
        self._batchSpinBox.setMaximum(99999);
        
        self._modelPathTextEdit = QtWidgets.QLineEdit()
        self._modelPathGenerateBtn = QtWidgets.QPushButton("Generate")
        self._modelPathGenerateBtn.clicked.connect(self.generateModelPath)

        self._modelNameTextEdit = QtWidgets.QLineEdit()
        self._modelNameGenerateBtn = QtWidgets.QPushButton("Generate")
        self._modelNameGenerateBtn.clicked.connect(self.generateModelName)

        labelDatasetPath = QtWidgets.QLabel("Dataset path")
        labelDatasetPath.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self._datasetPathTextEdit = QtWidgets.QLineEdit()
        self._datasetPathTextEdit.textChanged.connect(self._datasetPathTextEdit_changed)

        self._btnValidateDataset = QtWidgets.QPushButton("Validate")
        self._btnValidateDataset.clicked.connect(self.validateDataset)
        
        self._btnStartTraining = QtWidgets.QPushButton("Start training")
        self._btnStartTraining.clicked.connect(self.startTraining)

        self._datasetPathSelector = QtWidgets.QComboBox()
        self._datasetPathSelector.addItem(self.DATASET_PATHS[0])
        self._datasetPathSelector.addItem(self.DATASET_PATHS[1])
        self._datasetPathSelector.currentIndexChanged.connect(self.datasetPathChanged)
        self.datasetPathChanged(0)

        subSettingsContainer = QtWidgets.QWidget()
        subSettingsContainer.setLayout(QtWidgets.QGridLayout())
        subSettingsContainer.layout().addWidget(self._settingsLabel, 0, 0)
        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Number of workers (0 = single worker):"), 1, 0)
        subSettingsContainer.layout().addWidget(self._workerSpinBox, 1, 1, 1, 2)

        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Number of epochs (training runs):"), 2, 0)
        subSettingsContainer.layout().addWidget(self._epochsSpinBox, 2, 1, 1, 2)
        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Batch size:"), 3, 0)
        subSettingsContainer.layout().addWidget(self._batchSpinBox, 3, 1, 1, 2)

        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Model output path:"), 4, 0)
        subSettingsContainer.layout().addWidget(self._modelPathGenerateBtn, 4, 1)
        subSettingsContainer.layout().addWidget(self._modelPathTextEdit, 4, 2, 1, 2)

        subSettingsContainer.layout().addWidget(QtWidgets.QLabel("Model name:"), 5, 0)
        subSettingsContainer.layout().addWidget(self._modelNameGenerateBtn, 5, 1)
        subSettingsContainer.layout().addWidget(self._modelNameTextEdit, 5, 2, 1, 2)

        self._settingsContainer.layout().addWidget(subSettingsContainer, 0, 0, 1, 2)
        self._settingsContainer.layout().addWidget(labelDatasetPath, 1, 0)
        self._settingsContainer.layout().addWidget(self._datasetPathSelector, 1, 1)

        self._settingsContainer.layout().addWidget(self._datasetPathTextEdit, 2, 0, 1, 2)
        self._settingsContainer.layout().addWidget(self._btnValidateDataset, 3, 0)
        self._settingsContainer.layout().addWidget(self._btnStartTraining, 3, 1)

    def _initProgressContainer(self):
        self._progressContainer = QtWidgets.QWidget()
        self._progressContainer.setLayout(QtWidgets.QGridLayout())

        self._statusTextEdit = QtWidgets.QTextEdit()
        self._statusTextEdit.setReadOnly(True)

        self._progressBar = QtWidgets.QProgressBar()
        self._progressBar.setMaximum(100)


        self._progressContainer.layout().addWidget(self._statusTextEdit, 0, 0)
        self._progressContainer.layout().addWidget(self._progressBar, 1, 0)

    def modelChanged(self, index):
        self._settingsLabel.setText(f"Settings for {self.MODELS[index]}:")

    def datasetPathChanged(self, index):
        if(index == 0): # dataset export path
            self._datasetPathTextEdit.setText(SharedValues().datasetExportPath)
        elif(index == 1):
            self._datasetPathTextEdit.setText(SharedValues().datasetImportPath)

        self.pathValidated = False
        self._btnStartTraining.setEnabled(False)

    def _datasetPathTextEdit_changed(self, text):
        self.pathValidated = False
        self._btnStartTraining.setEnabled(False)

    def validateDataset(self):
        if(self.modelSelector.currentIndex() == self.YOLO_V8_MODEL_INDEX):
            if(self.currentModelTrainer is None):
                self.currentModelTrainer = YoloUltralyticsTrainer()
            
            isValid, message = self.currentModelTrainer.validateDataset(self._datasetPathTextEdit.text())

            if(not isValid):
                self._btnStartTraining.setEnabled(False)
                QtWidgets.QMessageBox.critical(self, "Dataset is not correct", message)
                return
            else:
                self._btnStartTraining.setEnabled(True)

    def generateModelName(self):
        timestamp = datetime.now().strftime("%Y_%m_%d")
        self._modelNameTextEdit.setText(f"project_{timestamp}_ver")

    def generateModelPath(self):
        if(self._datasetPathTextEdit == ""):
             QtWidgets.QMessageBox.warning(self, "Select dataset path for generating model output path")
        else:
            path = Path(os.getcwd()) / "models"
            self._modelPathTextEdit.setText(path.resolve()._str)

    def startTraining(self):
        if(self.currentModelTrainer is not None):
            self.setTabsEnabled_fn(False)
            self._modelSelectorContainer.setEnabled(False)
            self._settingsContainer.setEnabled(False)

            self.currentModelTrainer.epochs = self._epochsSpinBox.value()
            self.currentModelTrainer.workers = self._workerSpinBox.value()
            self.currentModelTrainer.batch = self._batchSpinBox.value()
            self.currentModelTrainer.modelPath = self._modelPathTextEdit.text()
            self.currentModelTrainer.modelName = self._modelNameTextEdit.text()

            if(self.thread is None):
                self.thread = QtCore.QThread()
            
            if(not self.currentModelTrainer.connectedToThread):
                self.currentModelTrainer.moveToThread(self.thread)

                self.thread.started.connect(self.currentModelTrainer.run)
            
                self.currentModelTrainer.progress.connect(self._progressBar.setValue)
                self.currentModelTrainer.status.connect(self._statusText_slot)
                self.currentModelTrainer.error.connect(self._showError_slot)
                self.currentModelTrainer.errorExit.connect(self._errorExit_slot)

                self.currentModelTrainer.finished.connect(self._trainingEnded_slot)
                self.currentModelTrainer.connectedToThread = True

            self._statusTextEdit.clear()
            self.thread.start()
        else:
            QtWidgets.QMessageBox.critical(self, 
                                           "Model trainer not selected", 
                                           "Model trainer is not selected or not supported. " \
                                           "Training will not start")

    def _trainingEnded_slot(self):
        self.setTabsEnabled_fn(True)
        self._modelSelectorContainer.setEnabled(True)
        self._settingsContainer.setEnabled(True)

    def destroyTrainers(self):
        if(self.thread is None):
            return
        
        if(self.thread.isRunning()):
            try:
                self.currentModelTrainer.requestStop = True
            except Exception as e:
                print(f"Error in closing ModelTrainer.currentModelTrainer: {e}")

            self.thread.quit()
            self.thread.wait()

        if(self.currentModelTrainer is not None):
            self.currentModelTrainer.deleteLater()
            self.currentModelTrainer = None

        self.thread.deleteLater()
        self.thread = None

    @QtCore.Slot(str)
    def _statusText_slot(self, text:str ):
        self._statusTextEdit.setPlainText(self._statusTextEdit.toPlainText() + "\n" + text)
        self._statusTextEdit.moveCursor(QTextCursor.End)

    def _showError_slot(self, text: str):
        QtWidgets.QMessageBox.critical(self, "Training error", text)

    def _errorExit_slot(self, text: str):
        QtWidgets.QMessageBox.critical(self, "Error occurred during training", text)
        self._trainingEnded_slot()

    def tab_selected(self):
        pass

    def tab_closed(self):
        pass