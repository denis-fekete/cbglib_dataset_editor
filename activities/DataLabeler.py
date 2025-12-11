import cv2 as cv

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QRectF, QPointF, QModelIndex, QItemSelection
from PySide6.QtGui import QBrush, QPixmap, QScreen, QShortcut, QKeySequence, QCursor, QColor

from widgets import *
from utils import *
from image_manipulation import *

class DataLabeler(QtWidgets.QWidget):
    def __init__(self, imageSamples: list[ImageLabelBox], labelsDict: dict[int, LabelEntry], screen: QScreen):
        super().__init__()        

        self.currentImageSample: ImageSample = None
        self.imageSamples: list[ImageSample] = imageSamples
        self.labelsDict: dict[LabelEntry] = labelsDict

        self._screen: QScreen = screen

        self._initUI()
        self.initShortcuts()

    def _initUI(self):
        self.setLayout(QtWidgets.QGridLayout())

        self._scene = ImageScene()
        self._view = ZoomGraphicsView(self._scene, self.onGraphicsItemClickSlot)
        
        self._scene.setBackgroundBrush(QBrush(QtCore.Qt.GlobalColor.white))
        self._scene.setSceneRect(0, 0, self._view.rect().width() * 0.9, self._view.rect().height() * 0.9)

        self._initLabelSelectorContainer()
        self._initImageSampleSelectorContainer()
        self._initTopToolbarContainer()
        self._initSelectorsContainer()

        self.layout().addWidget(self._topToolbarContainer, 0, 1)
        self.layout().addWidget(self._selectorsContainer, 1, 0)
        self.layout().addWidget(self._view, 1, 1)
        
    def _initTopToolbarContainer(self):
        self._topToolbarContainer = QtWidgets.QWidget()
        self._topToolbarContainer.setLayout(QtWidgets.QHBoxLayout())
        self._topToolbarContainer.layout().setSpacing(0)
        self._topToolbarContainer.layout().setContentsMargins(0, 0, 0, 0)
        self._topToolbarContainer.setMaximumHeight(20)

        self._btnNewLabel = QtWidgets.QPushButton("New label")
        self._btnNewLabel.setMaximumWidth(100)
        self._topToolbarContainer.layout().addWidget(self._btnNewLabel)
        self._topToolbarContainer.layout().addWidget(QtWidgets.QLabel("(Ctrl+W)"))

        self._btnDeleteLabel = QtWidgets.QPushButton("Delete label")
        self._btnDeleteLabel.setMaximumWidth(100)
        self._topToolbarContainer.layout().addWidget(self._btnDeleteLabel)
        self._topToolbarContainer.layout().addWidget(QtWidgets.QLabel("(Del)"))

        self._selectedColorPicker = ColorPicker(QColor(160, 255, 160), self._updateImageLabelBoxesColors)
        self._selectedColorPicker.setMaximumWidth(50)

        self._defaultColorPicker = ColorPicker(QColor(10, 10, 10), self._updateImageLabelBoxesColors)
        self._defaultColorPicker.setMaximumWidth(50)
        
        self._topToolbarContainer.layout().addWidget(self._selectedColorPicker)
        self._topToolbarContainer.layout().addWidget(self._defaultColorPicker)

        self._btnNewLabel.clicked.connect(self.newImageLabelBox_slot)
        self._btnDeleteLabel.clicked.connect(self.deleteImageLabelBox_slot)

    def _initSelectorsContainer(self):
        self._selectorsContainer = QtWidgets.QWidget()
        self._selectorsContainer.setLayout(QtWidgets.QGridLayout())
        self._selectorsContainer.layout().setSpacing(0)

        spacer = QtWidgets.QWidget()
        spacer.setMaximumHeight(60)

        self._selectorsContainer.layout().addWidget(self._labelSelectorContainer, 0, 0)
        self._selectorsContainer.layout().addWidget(spacer, 1, 0)
        self._selectorsContainer.layout().addWidget(self._imageSampleSelectorContainer, 2, 0)
        self._selectorsContainer.setMaximumWidth(250)

    def _initLabelSelectorContainer(self):
        self._labelSelectorContainer = QtWidgets.QWidget()
        self._labelSelectorContainer.setLayout(QtWidgets.QGridLayout())

        self._labelSelector = LabelSelectorTreeView(self.labelsDict)
        self._labelSelector.clicked.connect(self.labelSelected_slot)
        self._labelSelector.model.dataChanged.connect(self.labelChanged_slot)

        self._btnNewLabel = QtWidgets.QPushButton("New")
        self._btnNewLabel.clicked.connect(self.newLabel_slot)

        self._btnDeleteLabel = QtWidgets.QPushButton("Delete")
        self._btnDeleteLabel.clicked.connect(self.deleteLabel_slot)

        self._labelSelectorContainer.layout().addWidget(QtWidgets.QLabel("Labels:"), 0, 0)
        self._labelSelectorContainer.layout().addWidget(self._btnNewLabel, 1, 0)
        self._labelSelectorContainer.layout().addWidget(self._btnDeleteLabel, 1, 1)
        self._labelSelectorContainer.layout().addWidget(self._labelSelector, 2, 0, 1, 2)

    def _initImageSampleSelectorContainer(self):
        self._imageSampleSelectorContainer = QtWidgets.QWidget()
        self._imageSampleSelectorContainer.setLayout(QtWidgets.QGridLayout())

        self._imageSampleTreeView = ImageSampleTreeView(self.imageSamples)
        self._imageSampleTreeView.loadSamples()
        self._imageSampleTreeView.selectionModel().currentChanged.connect(self.imageSampleChanged_slot)

        self._btnNextImageSample = QtWidgets.QPushButton("Next")
        self._btnNextImageSample.clicked.connect(self.nextImageSample_slot)

        self._btnPreviousImageSample = QtWidgets.QPushButton("Previous")
        self._btnPreviousImageSample.clicked.connect(self.previousImageSample_slot)

        self._imageSampleSelectorContainer.layout().addWidget(QtWidgets.QLabel("Image samples:"), 0, 0)
        self._imageSampleSelectorContainer.layout().addWidget(self._imageSampleTreeView, 1, 0, 1, 2)

        self._imageSampleSelectorContainer.layout().addWidget(self._btnPreviousImageSample, 2, 0)
        self._imageSampleSelectorContainer.layout().addWidget(self._btnNextImageSample, 2, 1)

        labelPrevious = QtWidgets.QLabel("(Ctrl+Q)")
        labelPrevious.setContentsMargins(30, 0, 0 , 0)
        labelNext = QtWidgets.QLabel("(Ctrl+E)")
        labelNext.setContentsMargins(30, 0, 0 , 0)

        self._imageSampleSelectorContainer.layout().addWidget(labelPrevious, 3, 0)
        self._imageSampleSelectorContainer.layout().addWidget(labelNext, 3, 1)

    def initShortcuts(self):
        """Initializes shortcuts"""
        self._shortcutNewLabel = QShortcut(QKeySequence("Ctrl+W"), self)
        self._shortcutNewLabel.activated.connect(self.newImageLabelBox_slot)

        self._shortcutDeleteLabel = QShortcut(QKeySequence("Del"), self)
        self._shortcutDeleteLabel.activated.connect(self.deleteImageLabelBox_slot)

        self._shortcutNextImageSample = QShortcut(QKeySequence("Ctrl+E"), self)
        self._shortcutNextImageSample.activated.connect(self.nextImageSample_slot)

        self._shortcutPreviousImageSample = QShortcut(QKeySequence("Ctrl+Q"), self)
        self._shortcutPreviousImageSample.activated.connect(self.previousImageSample_slot)

    def _correctSceneAndView(self):
        """Corrects scale of `QGraphicsView` based on loaded `ImageSample`"""
        self._view.resetTransform()

        wScale = self._view.rect().width() / self.currentImageSample.width
        hScale = self._view.rect().height() / self.currentImageSample.height

        scale = min(wScale, hScale)

        SCALE_CONST = 0.02 # constant for zooming out move to get rid of sliders on sides
        self._view.scale(scale - SCALE_CONST, scale - SCALE_CONST)
    
    def imageSampleChanged_slot(self, current: QModelIndex, previous: QModelIndex):
        """Slot called when `ImageSample`from QTreeView dataset was changed"""
        if(self.currentImageSample is not None):
            self.currentImageSample.unload(save=True)

        if(not current.isValid()):
            return

        clickedItemName = current.data()
        if(clickedItemName is None):
            print("Error: clickedItemName was not found in datasetItemSelected_slot()")
            return 
        
        newCurrentImageSample = next(filter(lambda item: item.name == clickedItemName, self.imageSamples), None)

        if(self.currentImageSample == newCurrentImageSample):
            return
        oldImageSample = self.currentImageSample
        self.currentImageSample = newCurrentImageSample

        if(oldImageSample is not None):
            self._imageSampleTreeView.checkImageSampleWarnings(oldImageSample,
                                                               checkLabelBoxes=True,
                                                               checkImageLabelBoxes=False)
        self.loadImageSample()
            
    def loadImageSample(self):
        """Loads `currentImageSample` image sample into current graphics scene and corrects size and zoom of screen"""
        self.currentImageSample.load(self._selectedColorPicker.color, self._defaultColorPicker.color)

        self._scene.clear()
        self._view.resetZoom()
        self._view.selectedItem = None

        self._scene.setPixmap(self.currentImageSample.getQPixmap())
        self._scene.setSceneRect(0, 0, self.currentImageSample.width, self.currentImageSample.height)
        
        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            self._scene.addItem(imageLabelBox)

        self._correctSceneAndView()

        # reset warning on image samples tree view
        if(self.currentImageSample is not None):
            self._imageSampleTreeView.checkImageSampleWarnings(self.currentImageSample,
                                                               checkLabelBoxes=True,
                                                               checkImageLabelBoxes=False)

    def labelSelected_slot(self, index: QModelIndex):
        """Slot called when label from `_labelSelector` was changed"""

        self._labelSelector.selectLabel(index)
       
        if(self.currentImageSample is not None):
            selectedLabelBox: ImageLabelBox = self._view.selectedItem
            
            if(selectedLabelBox is not None):
                model = index.model()
                row = index.row()
                value = int(model.index(row, 0).data())
                labelEntry: LabelEntry = self.labelsDict[value]
                selectedLabelBox.setLabel(labelEntry.index, labelEntry.name)
            
            # reset warning on image samples tree view
            if(self.currentImageSample is not None):
                self._imageSampleTreeView.checkImageSampleWarnings(self.currentImageSample, 
                                                                   checkLabelBoxes=False, 
                                                                   checkImageLabelBoxes=True)
    
    def labelChanged_slot(self, topLeft, bottomRight, roles):
        """Slot called when label was edited"""
        for row in range(topLeft.row(), bottomRight.row() + 1):
            if(topLeft != bottomRight):
                raise Exception("Shouldn't happen")
            
            name = self._labelSelector.model.index(row, 1).data()
            # shortcut = self._labelSelector.model.index(row, 2).data()
        
            self.labelsDict[row] = LabelEntry(name, row, None)
            # self.labelsDict[row] = LabelEntry(name, row, shortcut) # TODO: add shortcut support

            self.currentImageSample.reloadImageLabels()

    def newImageLabelBox_slot(self):
        """Create new `ImageLabelBox` and add it to the `ImageSample`"""
        if(self.currentImageSample is None):
            return 
        
        defaultW, defaultH = 100, 200
        defaultLabelIndex, defaultLabelName = -1, "default"
        defaultX, defaultY = self._scene.sceneRect().width() / 2, self._scene.sceneRect().height() / 2
        
        if(self._labelSelector.currentIndex is not None): 
            defaultLabelIndex = self._labelSelector.currentIndex
            defaultLabelName = self.labelsDict[defaultLabelIndex].name

        globalPosition = self._view.mapFromGlobal(QCursor.pos())
        scenePosition = self._view.mapToScene(globalPosition)

        if(pointInRectangle(scenePosition, self._scene.sceneRect())):
            defaultX, defaultY = scenePosition.x(), scenePosition.y()
        
        newLabelBox = ImageLabelBox(QRectF( defaultX,
                                            defaultY,
                                            defaultW,
                                            defaultH),
                                    defaultLabelIndex, defaultLabelName,
                                    self._handleScaleByView,
                                    self.currentImageSample.rect())
        
        self.currentImageSample.add(newLabelBox)
        self._scene.addItem(newLabelBox)

    def deleteImageLabelBox_slot(self):
        """Deletes currently selected `ImageLabelBox` from `currentImageSample`"""
        self.currentImageSample.remove(self._view.selectedItem)
        self._scene.removeItem(self._view.selectedItem)
        self._view.selectedItem = None

    def newLabel_slot(self):
        """Creates new `LabelEntry` into global dictionary of labels"""
        index = len(self.labelsDict)
        self.labelsDict[index] = LabelEntry("new", index, None)
        self._labelSelector.loadLabels()

    def deleteLabel_slot(self):
        """Deletes label from global list of labels, all keys will be moved down"""
        # TODO: Add warning!
        index = self._labelSelector.currentIndex
        self.labelsDict.pop(index)

        keys = list(self.labelsDict.keys()) 
        
        maxKey = 0
        for key in keys:
            if(key > index):
                oldValues: LabelEntry = self.labelsDict[key]
                self.labelsDict[key-1] = LabelEntry(oldValues.name, oldValues.index, oldValues.shortcut)
                maxKey = max(key, maxKey)
        
        if(len(self.labelsDict) > 0):
            self.labelsDict.pop(maxKey)

        for imageSample in self.imageSamples:
            for labelBox in imageSample._labelBoxes:
                if(labelBox.label == index):
                    labelBox.label = -1
                elif(labelBox.label > index):
                    labelBox.label = labelBox.label - 1

        if(self.currentImageSample is not None):
            for imageLabelBox in self.currentImageSample.imageLabelBoxes:
                if(imageLabelBox.label == index):
                    imageLabelBox.setLabel(-1, "default")
                elif(imageLabelBox.label > index):
                    imageLabelBox.label = imageLabelBox.label - 1
                

        self._labelSelector.loadLabels()

    def nextImageSample_slot(self):
        if(self.currentImageSample is None):
            return 

        currentIndex = self._imageSampleTreeView.currentIndex()
        nextIndex = self._imageSampleTreeView.indexBelow(currentIndex)
        if(nextIndex.isValid()):
            self._imageSampleTreeView.setCurrentIndex(nextIndex)

    def previousImageSample_slot(self):
        if(self.currentImageSample is None):
            return 

        currentIndex = self._imageSampleTreeView.currentIndex()
        previousIndex = self._imageSampleTreeView.indexAbove(currentIndex)
        if(previousIndex.isValid()):
            self._imageSampleTreeView.setCurrentIndex(previousIndex)

    def _handleScaleByView(self):
        """Returns maximum width or height of windows. Used for scaling different UI elements"""
        return max( self._screen.geometry().width() * 0.03,
                    self._screen.geometry().height() * 0.03)
        
    def onGraphicsItemClickSlot(self):
        # reset warning on image samples tree view
        if(self.currentImageSample is not None):
            self._imageSampleTreeView.checkImageSampleWarnings(self.currentImageSample,
                                                               checkLabelBoxes=False,
                                                               checkImageLabelBoxes=True)
        pass

    def _updateImageLabelBoxesColors(self):
        if (self.currentImageSample is None):
            return
        
        for imageLabelBox in self.currentImageSample.imageLabelBoxes:
            imageLabelBox.updateColors(defaultColor=self._defaultColorPicker.color,
                                       selectedColor=self._selectedColorPicker.color)

    def getCurrentImageSample(self):
        return self.currentImageSample

    def tab_selected(self):
        """Slot called on change of tabs"""
        self._imageSampleTreeView.loadSamples(restoreVerticalPosition=True)
        self._labelSelector.loadLabels()
        
        self._view.selectedItem = None
        if(self.currentImageSample is not None):
            self.loadImageSample()

    def tab_closed(self):
        if(self.currentImageSample is not None):
            self.currentImageSample.unload(save=True)
        self._scene.clear()