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

from .dataLabelerWidgets.ImageBrowser import ImageBrowser
from .dataLabelerWidgets.ClassLabelsBrowser import ClassLabelsBrowser
from .dataLabelerWidgets.AutoDetectToolbar import AutoDetectToolbar
from .dataLabelerWidgets.ImageLabelBoxToolbar import ImageLabelBoxToolbar


class DataLabeler(AbstractTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.currentImageSample: ImageSample | None = None
        self.imageAnalyzer: ImageAnalyzer | None = None

        self._initUI()
        self.setupShortcuts()

    def _initUI(self) -> None:
        self.setLayout(QtWidgets.QGridLayout())

        self._scene = ImageScene()
        self.imageView = ZoomGraphicsView(self._scene, self.graphicsItemClicked)

        self._scene.setBackgroundBrush(QBrush(QtCore.Qt.GlobalColor.white))
        self._scene.setSceneRect(
            0,
            0,
            self.imageView.rect().width() * 0.9,
            self.imageView.rect().height() * 0.9,
        )

        self.imageLabelBoxToolbar = ImageLabelBoxToolbar()
        self.imageLabelBoxToolbar.new.connect(self.imageLabelBoxNewClicked)
        self.imageLabelBoxToolbar.delete.connect(self.imageLabelBoxDeleteClicked)
        self.imageLabelBoxToolbar.updateColors.connect(self.updateImageLabelBoxColors)

        self.autoDetectToolbar = AutoDetectToolbar()
        self.autoDetectToolbar.autoDetect.connect(self.autoDetectLabelsClicked)
        self.autoDetectToolbar.openModel.connect(self.openModelClicked)
        self.autoDetectToolbar.loadModel.connect(self.loadModelClicked)

        self.imageBrowser = ImageBrowser()
        self.imageBrowser.nextImage.connect(self.nextImageSampleClicked)
        self.imageBrowser.previousImage.connect(self.previousImageSampleClicked)
        self.imageBrowser.imageSampleChanged.connect(self.imageSampleChanged)

        self.classLabelsBrowser = ClassLabelsBrowser()
        self.classLabelsBrowser.labelsChanged.connect(self.classLabelsChanged)
        self.classLabelsBrowser.dataEdited.connect(self.classLabelsEdited)
        self.classLabelsBrowser.new.connect(self.classLabelsNewEntry)
        self.classLabelsBrowser.delete.connect(self.classLabelsDeleteEntry)

        self.layout().addWidget(self.imageLabelBoxToolbar, 0, 0)
        self.layout().addWidget(self.autoDetectToolbar, 0, 1)
        self.layout().layout().addWidget(self.imageBrowser, 1, 0)
        self.layout().addWidget(self.imageView, 1, 1)
        self.layout().addWidget(self.classLabelsBrowser, 1, 2)

    def setupShortcuts(self) -> None:
        """Initializes shortcuts"""
        self._shortcutNewLabel = QShortcut(QKeySequence("Space"), self)
        self._shortcutNewLabel.activated.connect(self.imageLabelBoxNewClicked)

        self._shortcutDeleteLabel = QShortcut(QKeySequence("X"), self)
        self._shortcutDeleteLabel.activated.connect(self.imageLabelBoxDeleteClicked)

        self._shortcutNextImageSample = QShortcut(QKeySequence("E"), self)
        self._shortcutNextImageSample.activated.connect(self.nextImageSampleClicked)

        self._shortcutPreviousImageSample = QShortcut(QKeySequence("Q"), self)
        self._shortcutPreviousImageSample.activated.connect(
            self.previousImageSampleClicked
        )

        self._autoDetectLabels = QShortcut(QKeySequence("Tab"), self)
        self._autoDetectLabels.activated.connect(self.autoDetectLabelsClicked)

    #######################################################
    # Graphics scene and graphics view
    #######################################################

    def correctSceneAndView(self) -> None:
        """Corrects scale of `QGraphicsView` based on loaded `ImageSample`"""
        self.imageView.resetTransform()

        wScale = self.imageView.rect().width() / self.currentImageSample.width
        hScale = self.imageView.rect().height() / self.currentImageSample.height

        scale = min(wScale, hScale)

        SCALE_CONST = (
            0.02  # constant for zooming out move to get rid of sliders on sides
        )
        self.imageView.scale(scale - SCALE_CONST, scale - SCALE_CONST)

    def loadImageSample(self) -> None:
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        self.currentImageSample.load(
            self.imageLabelBoxToolbar.selectedColorPicker.color,
            self.imageLabelBoxToolbar.defaultColorPicker.color,
        )

        self._scene.clear()
        self.imageView.resetZoom()
        self.imageView.selectedItem = None

        self._scene.setPixmap(self.currentImageSample.getQPixmap())
        self._scene.setSceneRect(
            0, 0, self.currentImageSample.width, self.currentImageSample.height
        )

        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            self._scene.addItem(imageLabelBox)

        self.correctSceneAndView()

        # reset warning on image samples tree view
        if self.currentImageSample is not None:
            self.imageBrowser.treeView.checkImageSampleWarnings(
                self.currentImageSample,
                checkLabelBoxes=True,
                checkImageLabelBoxes=False,
            )

    def graphicsItemClicked(self) -> None:
        # reset warning on image samples tree view
        if self.currentImageSample is not None:
            self.imageBrowser.treeView.checkImageSampleWarnings(
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

        if self.classLabelsBrowser.treeView.currIndex is not None:
            defaultLabelIndex = self.classLabelsBrowser.treeView.currIndex
            defaultLabelName = SharedValues().labelsDict[defaultLabelIndex].name

        globalPosition = self.imageView.mapFromGlobal(QCursor.pos())
        scenePosition = self.imageView.mapToScene(globalPosition)

        if pointInRectangle(scenePosition, self._scene.sceneRect()):
            defaultX, defaultY = scenePosition.x(), scenePosition.y()

        newLabelBox = ImageLabelBox(
            Box(defaultX, defaultY, defaultW, defaultH),
            defaultLabelIndex,
            defaultLabelName,
            self.screenScaleText,
            self.currentImageSample.rect(),
            self.imageLabelBoxToolbar.selectedColorPicker.color,
            self.imageLabelBoxToolbar.defaultColorPicker.color,
        )

        self.currentImageSample.add(newLabelBox)
        self._scene.addItem(newLabelBox)

        if self.imageView.selectedItem is not None:
            self.imageView.selectedItem.setSelected(False)
        self.imageView.selectedItem = newLabelBox
        self.imageView.selectedItem.setSelected(True)

    @Slot()
    def imageLabelBoxDeleteClicked(self) -> None:
        """Deletes currently selected `ImageLabelBox` from `currentImageSample`"""
        if (
            self.currentImageSample is not None
            and self.imageView.selectedItem is not None
        ):
            self.currentImageSample.remove(self.imageView.selectedItem)
            self._scene.removeItem(self.imageView.selectedItem)

            self.imageBrowser.treeView.checkImageSampleWarnings(
                self.currentImageSample,
                checkLabelBoxes=False,
                checkImageLabelBoxes=True,
            )

        self.imageView.selectedItem = None

    @Slot()
    def updateImageLabelBoxColors(self) -> None:
        if self.currentImageSample is None:
            return

        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            imageLabelBox.updateColors(
                defaultColor=self.imageLabelBoxToolbar.defaultColorPicker.color,
                selectedColor=self.imageLabelBoxToolbar.selectedColorPicker.color,
            )

    #######################################################
    # Class Label Browser
    #######################################################

    @Slot()
    def classLabelsChanged(self, index: QModelIndex):
        """Slot called when label from `classLabelsBrowser.treeView` was changed"""

        self.classLabelsBrowser.treeView.selectLabel(index)

        if self.currentImageSample is not None:
            selectedLabelBox: ImageLabelBox | None = self.imageView.selectedItem

            if selectedLabelBox is not None:
                model = index.model()
                row = index.row()
                value = int(model.index(row, 0).data())
                labelEntry: LabelEntry = SharedValues().labelsDict[value]
                selectedLabelBox.setLabel(labelEntry.index, labelEntry.name)

            # reset warning on image samples tree view
            if self.currentImageSample is not None:  # type: ignore
                self.imageBrowser.treeView.checkImageSampleWarnings(
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

            name = self.classLabelsBrowser.treeView.model.index(row, 1).data()

            SharedValues().labelsDict[row] = LabelEntry(name, row)
            self.currentImageSample.reloadImageLabels()

    @Slot()
    def classLabelsNewEntry(self) -> None:
        """Creates new `LabelEntry` into global dictionary of labels"""
        index = len(SharedValues().labelsDict)
        SharedValues().labelsDict[index] = LabelEntry("new", index)
        self.classLabelsBrowser.treeView.loadLabels()

    @Slot()
    def classLabelsDeleteEntry(self) -> None:
        """Deletes label from global list of labels, all keys will be moved down"""
        if self.classLabelsBrowser.treeView.currIndex is None:
            return

        # TODO: Add warning!
        index = self.classLabelsBrowser.treeView.currIndex
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

        self.classLabelsBrowser.treeView.loadLabels()

    #######################################################
    # Image Sample Browser
    #######################################################

    @Slot(QItemSelection, QItemSelection)
    def imageSampleChanged(
        self, current: QItemSelection, previous: QItemSelection
    ) -> None:
        """Slot called when `ImageSample`from QTreeView dataset was changed"""
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
            self.imageBrowser.treeView.checkImageSampleWarnings(
                oldImageSample, checkLabelBoxes=True, checkImageLabelBoxes=False
            )
        self.loadImageSample()

    @Slot()
    def nextImageSampleClicked(self) -> None:
        if self.currentImageSample is None:
            return

        currentIndex = self.imageBrowser.treeView.currentIndex()
        nextIndex = self.imageBrowser.treeView.indexBelow(currentIndex)
        if nextIndex.isValid():
            self.imageBrowser.treeView.setCurrentIndex(nextIndex)

    @Slot()
    def previousImageSampleClicked(self) -> None:
        if self.currentImageSample is None:
            return

        currentIndex = self.imageBrowser.treeView.currentIndex()
        previousIndex = self.imageBrowser.treeView.indexAbove(currentIndex)
        if previousIndex.isValid():
            self.imageBrowser.treeView.setCurrentIndex(previousIndex)

    #######################################################
    # Automatic Detection Toolbar
    #######################################################

    @Slot()
    def autoDetectLabelsClicked(self) -> None:
        if self.imageAnalyzer is None:
            self.autoDetectToolbar.btnAutoDetect.setEnabled(False)
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
                    self.imageLabelBoxToolbar.selectedColorPicker.color,
                    self.imageLabelBoxToolbar.defaultColorPicker.color,
                )

                self.currentImageSample.add(box)
                self._scene.addItem(box)

    @Slot()
    def loadModelClicked(self) -> None:
        EXPECTED_MODEL_SIZE = 640

        if self.autoDetectToolbar.textEditModelPath.text() != "":
            self.autoDetectToolbar.btnAutoDetect.setEnabled(True)
            self.imageAnalyzer = ImageAnalyzer(
                self.autoDetectToolbar.textEditModelPath.text(),
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
            self.autoDetectToolbar.textEditModelPath.setText(fileName)

    #######################################################
    # Settings
    #######################################################

    def loadSettings(self):
        settings = SharedValues().settings.labeling
        defaultColor = QColor(
            settings.defaultColorRed,
            settings.defaultColorGreen,
            settings.defaultColorBlue,
        )
        self.imageLabelBoxToolbar.defaultColorPicker.color = defaultColor
        self.imageLabelBoxToolbar.defaultColorPicker.updateBackgroundColor()

        selectedColor = QColor(
            settings.selectedColorRed,
            settings.selectedColorGreen,
            settings.selectedColorBlue,
        )
        self.imageLabelBoxToolbar.selectedColorPicker.color = selectedColor
        self.imageLabelBoxToolbar.selectedColorPicker.updateBackgroundColor()

        self.imageLabelBoxToolbar.updateColors.emit()

        self.autoDetectToolbar.textEditModelPath.setText(settings.modelPath)

    def updateSettings(self):
        settings = SharedValues().settings.labeling
        defaultColor = self.imageLabelBoxToolbar.defaultColorPicker.color
        settings.defaultColorRed = defaultColor.red()
        settings.defaultColorGreen = defaultColor.green()
        settings.defaultColorBlue = defaultColor.blue()

        selectedColor = self.imageLabelBoxToolbar.selectedColorPicker.color
        settings.selectedColorRed = selectedColor.red()
        settings.selectedColorGreen = selectedColor.green()
        settings.selectedColorBlue = selectedColor.blue()

        settings.modelPath = self.autoDetectToolbar.textEditModelPath.text()

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
        self.imageBrowser.treeView.loadSamples(restoreVerticalPosition=True)
        self.classLabelsBrowser.treeView.loadLabels()

        self.imageView.selectedItem = None
        if self.currentImageSample is not None:
            self.loadImageSample()

    @Slot()
    def clearCurrentImageSample(self):
        self.currentImageSample = None

    def tabClosed(self) -> None:
        if self.currentImageSample is not None:
            self.currentImageSample.unload(save=True)

        self._scene.clear()
