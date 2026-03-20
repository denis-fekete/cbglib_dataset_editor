"""
Module: DataLabeler.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Widget containing functionality for labeling image data that were loaded in DatasetLoader
    widget.
"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QModelIndex, Slot, QItemSelection
from PySide6.QtGui import QBrush, QShortcut, QKeySequence, QCursor, QColor

from app.widgets import *
from app.utils import *
from app.analysis import *

from app.labeling.Box import Box
from app.labeling.ImageSample import ImageSample
from app.labeling.ImageLabelBox import ImageLabelBox
from app.labeling.pointInRectangle import pointInRectangle
from app.labeling.LabelEntry import LabelEntry

from app.ui.DataLabeler_ui import Ui_DataLabeler


class DataLabeler(AbstractTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_DataLabeler()
        self.ui.setupUi(self)  # type: ignore

        self.currentImageSample: ImageSample | None = None
        self.imageAnalyzer: ImageAnalyzer | None = None
        self.labelDeleteButtonsInitialized: bool = False
        self.ignoreImageSampleChanged = False

        self._connectUI()
        self._setupShortcuts()

    def _connectUI(self) -> None:
        self._scene = ImageScene()
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.itemClicked.connect(self.graphicsItemClicked)

        self._scene.setBackgroundBrush(QBrush(QtCore.Qt.GlobalColor.white))
        self._scene.setSceneRect(
            0,
            0,
            self.ui.graphicsView.rect().width() * 0.9,
            self.ui.graphicsView.rect().height() * 0.9,
        )

        self.ui.imageSampleTreeView.setImageSamples(SharedValues().imageSamples)
        self.ui.labelSelectorTreeView.setLabels(SharedValues().labelsDict)

        self.ui.newLabelBoxButton.clicked.connect(self.imageLabelBoxNewClicked)
        self.ui.deleteLabelBoxButton.clicked.connect(self.imageLabelBoxDeleteClicked)
        self.ui.selectedColorPicker.clicked.connect(self.updateImageLabelBoxColors)
        self.ui.unselectedColorPicker.clicked.connect(self.updateImageLabelBoxColors)

        self.ui.autoDetectButton.clicked.connect(self.autoDetectLabelsClicked)
        self.ui.openModelButton.clicked.connect(self.openModelClicked)
        self.ui.loadModelButton.clicked.connect(self.loadAutoDetectModel)

        self.ui.previousSampleButton.clicked.connect(self.nextImageSample)
        self.ui.nextSampleButton.clicked.connect(self.nextImageSample)
        self.ui.imageSampleTreeView.selectedSampleChanged.connect(
            self.imageSampleChanged
        )

        self.ui.newClassLabelButton.clicked.connect(self.classLabelsNewEntry)
        self.ui.deleteClassLabelButton.clicked.connect(self.classLabelsDeleteEntry)
        self.ui.labelSelectorTreeView.dataEdited.connect(self.classLabelsEdited)
        self.ui.labelSelectorTreeView.labelsChanged.connect(self.classLabelsChanged)

    def _setupShortcuts(self) -> None:
        """Initializes shortcuts"""
        self._shortcutNewLabel = QShortcut(QKeySequence("Space"), self)
        self._shortcutNewLabel.activated.connect(self.imageLabelBoxNewClicked)

        self._shortcutDeleteLabel = QShortcut(QKeySequence("X"), self)
        self._shortcutDeleteLabel.activated.connect(self.imageLabelBoxDeleteClicked)

        self._shortcutNextImageSample = QShortcut(QKeySequence("E"), self)
        self._shortcutNextImageSample.activated.connect(self.nextImageSample)

        self._shortcutPreviousImageSample = QShortcut(QKeySequence("Q"), self)
        self._shortcutPreviousImageSample.activated.connect(self.previousImageSample)

        self._autoDetectLabels = QShortcut(QKeySequence("Tab"), self)
        self._autoDetectLabels.activated.connect(self.autoDetectLabelsClicked)

    #######################################################
    # Graphics scene and graphics view
    #######################################################

    def correctSceneAndView(self) -> None:
        """Corrects scale of `QGraphicsView` based on loaded `ImageSample`"""
        self.ui.graphicsView.resetTransform()

        wScale = self.ui.graphicsView.rect().width() / self.currentImageSample.width
        hScale = self.ui.graphicsView.rect().height() / self.currentImageSample.height

        scale = min(wScale, hScale)

        SCALE_CONST = (
            0.02  # constant for zooming out move to get rid of sliders on sides
        )
        self.ui.graphicsView.scale(scale - SCALE_CONST, scale - SCALE_CONST)

    def loadImageSample(self) -> None:
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        print("DEBUG: loadImageSample")
        self.currentImageSample.load(
            self.ui.selectedColorPicker.color,
            self.ui.unselectedColorPicker.color,
        )

        self._scene.clear()
        self.ui.graphicsView.resetZoom()
        self.ui.graphicsView.selectedItem = None

        self._scene.setPixmap(self.currentImageSample.getQPixmap())
        self._scene.setSceneRect(
            0, 0, self.currentImageSample.width, self.currentImageSample.height
        )

        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            self._scene.addItem(imageLabelBox)

        self.correctSceneAndView()

        # reset warning on image samples tree view
        # if self.currentImageSample is not None:
        #     print(f"loadImageSample")
        #     self.ui.imageSampleTreeView.checkImageSampleWarnings(
        #         self.currentImageSample,
        #         checkLabelBoxes=True,
        #         checkImageLabelBoxes=False,
        #     )

    def graphicsItemClicked(self) -> None:
        # reset warning on image samples tree view
        if self.currentImageSample is not None:
            print(f"graphicsItemClicked")
            self.ui.imageSampleTreeView.checkImageSampleWarnings(
                self.currentImageSample,
                checkLabelBoxes=False,
                checkImageLabelBoxes=True,
            )

    def getCurrentImageSample(self) -> ImageSample | None:
        return self.currentImageSample

    #######################################################
    # ImageLabelBox tool bar
    #######################################################

    @Slot()
    def imageLabelBoxNewClicked(self) -> None:
        """Create new `ImageLabelBox` and add it to the `ImageSample`"""
        if self.currentImageSample is None:
            return

        defaultW, defaultH = 100, 200
        defaultLabelIndex, defaultLabelName = -1, "default"
        defaultX, defaultY = (
            self._scene.sceneRect().width() / 2,
            self._scene.sceneRect().height() / 2,
        )

        if self.ui.labelSelectorTreeView.currIndex is not None:
            defaultLabelIndex = self.ui.labelSelectorTreeView.currIndex
            defaultLabelName = SharedValues().labelsDict[defaultLabelIndex].name

        globalPosition = self.ui.graphicsView.mapFromGlobal(QCursor.pos())
        scenePosition = self.ui.graphicsView.mapToScene(globalPosition)

        if pointInRectangle(scenePosition, self._scene.sceneRect()):
            defaultX, defaultY = scenePosition.x(), scenePosition.y()

        newLabelBox = ImageLabelBox(
            Box(defaultX, defaultY, defaultW, defaultH),
            defaultLabelIndex,
            defaultLabelName,
            self.screenScaleText,
            self.currentImageSample.rect(),
            self.ui.selectedColorPicker.color,
            self.ui.unselectedColorPicker.color,
        )

        self.currentImageSample.add(newLabelBox)
        self._scene.addItem(newLabelBox)

        if self.ui.graphicsView.selectedItem is not None:
            self.ui.graphicsView.selectedItem.setSelected(False)
        self.ui.graphicsView.selectedItem = newLabelBox
        self.ui.graphicsView.selectedItem.setSelected(True)

    @Slot()
    def imageLabelBoxDeleteClicked(self) -> None:
        """Deletes currently selected `ImageLabelBox` from `currentImageSample`"""
        if (
            self.currentImageSample is not None
            and self.ui.graphicsView.selectedItem is not None
        ):
            self.currentImageSample.remove(self.ui.graphicsView.selectedItem)
            self._scene.removeItem(self.ui.graphicsView.selectedItem)

            print(f"imageLabelBoxDeleteClicked")
            self.ui.imageSampleTreeView.checkImageSampleWarnings(
                self.currentImageSample,
                checkLabelBoxes=False,
                checkImageLabelBoxes=True,
            )

        self.ui.graphicsView.selectedItem = None

    @Slot()
    def updateImageLabelBoxColors(self) -> None:
        """Updates colors of all `ImageLabelBoxes` in current `ImageSample`."""
        if self.currentImageSample is None:
            return

        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            imageLabelBox.updateColors(
                defaultColor=self.ui.unselectedColorPicker.color,
                selectedColor=self.ui.selectedColorPicker.color,
            )

    #######################################################
    # Class Label Browser
    #######################################################

    @Slot()
    def classLabelsChanged(self, index: QModelIndex):
        """Slot called when label from `ui.labelSelectorTreeView` was changed"""

        self.ui.labelSelectorTreeView.selectLabel(index)

        if self.currentImageSample is not None:
            selectedLabelBox: ImageLabelBox | None = self.ui.graphicsView.selectedItem

            if selectedLabelBox is not None:
                model = index.model()
                row = index.row()
                value = int(model.index(row, 0).data())
                labelEntry: LabelEntry = SharedValues().labelsDict[value]
                selectedLabelBox.setLabel(labelEntry.index, labelEntry.name)

            # reset warning on image samples tree view
            if self.currentImageSample is not None:  # type: ignore
                print(f"classLabelsChanged")
                self.ui.imageSampleTreeView.checkImageSampleWarnings(
                    self.currentImageSample,
                    checkLabelBoxes=False,
                    checkImageLabelBoxes=True,
                )

    @Slot(QModelIndex, QModelIndex, list)
    def classLabelsEdited(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: list[int]
    ) -> None:
        """Slot called when label was edited"""
        for row in range(topLeft.row(), bottomRight.row() + 1):
            if topLeft != bottomRight:
                raise Exception("Shouldn't happen")

            name = self.ui.labelSelectorTreeView.model.index(row, 1).data()

            SharedValues().labelsDict[row] = LabelEntry(name, row)
            if self.currentImageSample is not None:
                self.currentImageSample.reloadImageLabels()

    @Slot()
    def classLabelsNewEntry(self) -> None:
        """Creates new `LabelEntry` into global dictionary of labels"""
        index = len(SharedValues().labelsDict)
        SharedValues().labelsDict[index] = LabelEntry("new", index)
        self.ui.labelSelectorTreeView.loadLabels()

    @Slot()
    def classLabelsDeleteEntry(self) -> None:
        """Deletes label from global list of labels, all keys will be moved down"""
        if self.ui.labelSelectorTreeView.currIndex is None:
            return

        if not self.labelDeleteButtonsInitialized:
            self.confirmLabelDeleteButton = QtWidgets.QPushButton("Confirm")
            self.cancelLabelDeleteButton = QtWidgets.QPushButton("Cancel")

        warningReply = QtWidgets.QMessageBox.warning(
            self,
            "Warning",
            "Deleting a class will cause all other classes to move down with their indexes. "
            "Furthermore this change is not reversible.",
            QtWidgets.QMessageBox.StandardButton.Ok
            | QtWidgets.QMessageBox.StandardButton.Abort,
        )

        if warningReply == QtWidgets.QMessageBox.StandardButton.Abort:
            return

        index = self.ui.labelSelectorTreeView.currIndex
        SharedValues().labelsDict.pop(index)

        keys = list(SharedValues().labelsDict.keys())

        maxKey = 0
        for key in keys:
            if key > index:
                oldValues: LabelEntry = SharedValues().labelsDict[key]
                SharedValues().labelsDict[key - 1] = LabelEntry(
                    oldValues.name, oldValues.index
                )
                maxKey = max(key, maxKey)

        if len(SharedValues().labelsDict) > 0:
            SharedValues().labelsDict.pop(maxKey)

        for imageSample in SharedValues().imageSamples:
            for labelBox in imageSample.labelBoxes:
                if labelBox.label == index:
                    labelBox.label = -1
                elif labelBox.label > index:
                    labelBox.label = labelBox.label - 1

        if self.currentImageSample is not None:
            for imageLabelBox in self.currentImageSample.imageLabelBoxes:
                if imageLabelBox.label == index:
                    imageLabelBox.setLabel(-1, "default")
                elif imageLabelBox.label > index:
                    imageLabelBox.label = imageLabelBox.label - 1

        self.ui.labelSelectorTreeView.loadLabels()

    #######################################################
    # Image Sample Browser
    #######################################################

    @Slot(QItemSelection, QItemSelection)
    def imageSampleChanged(
        self, current: QItemSelection, previous: QItemSelection
    ) -> None:
        """Slot called when `ImageSample`from QTreeView dataset was changed"""
        if self.ignoreImageSampleChanged:
            return
        print("DEBUG: imageSampleChanged")

        if self.currentImageSample is not None:
            self.currentImageSample.unload(save=True)

        if not current.indexes():
            return

        index = current.indexes()[0]

        if not index.isValid():
            return

        clickedItemName = index.data()
        if clickedItemName is None:
            print("Error: clickedItemName was not found in datasetItemSelected_slot()")
            return

        newCurrentImageSample: ImageSample = next(  # type: ignore
            filter(
                lambda item: item.name == clickedItemName, SharedValues().imageSamples
            ),  # type: ignore
            None,
        )

        if self.currentImageSample == newCurrentImageSample:
            return
        oldImageSample = self.currentImageSample
        self.currentImageSample = newCurrentImageSample

        if oldImageSample is not None:
            self.ignoreImageSampleChanged = True
            self.ui.imageSampleTreeView.checkImageSampleWarnings(
                oldImageSample, checkLabelBoxes=True, checkImageLabelBoxes=False
            )
            self.ignoreImageSampleChanged = False
        self.loadImageSample()

    @Slot()
    def nextImageSample(self) -> None:
        """Selects next image sample in `ImageSampleView`"""
        if self.currentImageSample is None:
            return

        currentIndex = self.ui.imageSampleTreeView.currentIndex()
        nextIndex = self.ui.imageSampleTreeView.indexBelow(currentIndex)
        if nextIndex.isValid():
            self.ui.imageSampleTreeView.setCurrentIndex(nextIndex)

    @Slot()
    def previousImageSample(self) -> None:
        """Selects previous image sample in `ImageSampleView`"""
        if self.currentImageSample is None:
            return

        currentIndex = self.ui.imageSampleTreeView.currentIndex()
        previousIndex = self.ui.imageSampleTreeView.indexAbove(currentIndex)
        if previousIndex.isValid():
            self.ui.imageSampleTreeView.setCurrentIndex(previousIndex)

    @Slot()
    def reloadImageSamplesTree(self) -> None:
        print("Reloading samples")
        self.ui.imageSampleTreeView.loadSamples(restoreVerticalPosition=True)
        self.ui.labelSelectorTreeView.loadLabels()

    #######################################################
    # Automatic Detection Toolbar
    #######################################################

    @Slot()
    def autoDetectLabelsClicked(self) -> None:
        """
        Attempts to detect objects in current `ImageSample`. Existing detections are not
        considered and duplicates might be created.
        """
        if self.imageAnalyzer is None:
            self.ui.autoDetectButton.setEnabled(False)
            return
        else:
            if self.currentImageSample is None:
                return

            image = self.currentImageSample.getCvImage()
            if image is None:
                return

            detections = self.imageAnalyzer.analyze(image)

            for det in detections:
                box = ImageLabelBox(
                    Box(det.xCenter, det.yCenter, det.width, det.height),
                    det.classIndex,
                    SharedValues().labelsDict[det.classIndex].name,
                    self.screenScaleText,
                    self.currentImageSample.rect(),
                    self.ui.selectedColorPicker.color,
                    self.ui.unselectedColorPicker.color,
                )

                self.currentImageSample.add(box)
                self._scene.addItem(box)

    @Slot()
    def loadAutoDetectModel(self) -> None:
        """Loads model from `ui.modelPathLineEdit` and tries to initialize the `ImageAnalyzer`."""
        EXPECTED_MODEL_SIZE = 640

        if self.ui.modelPathLineEdit.text() != "":
            self.ui.autoDetectButton.setEnabled(True)
            self.imageAnalyzer = ImageAnalyzer(
                self.ui.modelPathLineEdit.text(),
                EXPECTED_MODEL_SIZE,
                (114, 114, 114),
                0.6,
                0.4,
            )

    @Slot()
    def openModelClicked(self) -> None:
        """Open OS dialog window to choose a directory from which a dataset will be imported"""
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a model", "", "ONNX models (*.onnx)"
        )
        if fileName:
            self.ui.modelPathLineEdit.setText(fileName)

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        """Loads values from SharedValues.AppSettings into the app."""
        settings = SharedValues().settings.labeling
        defaultColor = QColor(
            settings.defaultColorRed,
            settings.defaultColorGreen,
            settings.defaultColorBlue,
        )
        self.ui.unselectedColorPicker.color = defaultColor
        self.ui.unselectedColorPicker.updateBackgroundColor()

        selectedColor = QColor(
            settings.selectedColorRed,
            settings.selectedColorGreen,
            settings.selectedColorBlue,
        )
        self.ui.selectedColorPicker.color = selectedColor
        self.ui.selectedColorPicker.updateBackgroundColor()

        self.updateImageLabelBoxColors()

        self.ui.modelPathLineEdit.setText(settings.modelPath)

    def updateSettings(self):
        """Updates current values of the SharedValues.AppSettings."""
        settings = SharedValues().settings.labeling
        defaultColor = self.ui.unselectedColorPicker.color
        settings.defaultColorRed = defaultColor.red()
        settings.defaultColorGreen = defaultColor.green()
        settings.defaultColorBlue = defaultColor.blue()

        selectedColor = self.ui.selectedColorPicker.color
        settings.selectedColorRed = selectedColor.red()
        settings.selectedColorGreen = selectedColor.green()
        settings.selectedColorBlue = selectedColor.blue()

        settings.modelPath = self.ui.modelPathLineEdit.text()

    #######################################################
    # Other
    #######################################################

    def screenScaleText(self) -> float:
        """Returns maximum width or height of windows. Used for scaling different UI elements"""
        return max(
            SharedValues().screen.geometry().width() * 0.03,
            SharedValues().screen.geometry().height() * 0.03,
        )

    def tabSelected(self) -> None:
        """Slot called on change of tabs"""
        print(f"DataLabeler.tabSelected")

        self.ui.graphicsView.selectedItem = None
        if self.currentImageSample is not None:
            self.loadImageSample()

        self.ignoreImageSampleChanged = False

    @Slot()
    def clearCurrentImageSample(self):
        self.currentImageSample = None

    def tabClosed(self) -> None:
        """Method called when tab was closed, another tab was clicked."""
        self.ignoreImageSampleChanged = True

        if self.currentImageSample is not None:
            self.currentImageSample.unload(save=True)
        self._scene.clear()
