import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QScreen

from widgets import *
from utils import *
from activities import *
from image_manipulation import *
from data_classes import *

##############################################################################

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, qtApp):
        super().__init__()
        self.qtApp = qtApp

        SharedValues().screen = self.qtApp.primaryScreen()
        SharedValues().filterPresets = getDefaultFilterPresets()
        self.lastIndex = None

        self.initWindow()
        self._initUI()

        
    def initWindow(self):
        screenWidth, screenHeight = SharedValues().screen.geometry().width(), SharedValues().screen.geometry().height()
        windowWidth, windowHeight = screenWidth/2, screenHeight/2

        if(windowWidth < 640 or windowHeight < 480):
            windowWidth = 640
            windowHeight = 480

        self.setGeometry(
            int(screenWidth / 2 - windowWidth / 2),
            int(screenHeight / 2 - windowHeight / 2),
            int(windowWidth),
            int(windowHeight),
        )

    def _initUI(self):
        self.mainUI = QtWidgets.QTabWidget()
        self.dataLabelerWidget = DataLabeler() 
        self.datasetWidget = DatasetLoader(self.dataLabelerWidget._handleScaleByView, self.setTabsEnabled) 
        self.syntheticDataCreatorWidget = SyntheticDataCreator(self.dataLabelerWidget.getCurrentImageSample)
        self.modelTrainerWidget = ModelTrainer(self.setTabsEnabled)

        self.mainUI.addTab(self.datasetWidget, "Dataset")
        self.mainUI.addTab(self.dataLabelerWidget, "Image labeling")
        self.mainUI.addTab(self.syntheticDataCreatorWidget, "Synthetic data")
        self.mainUI.addTab(self.modelTrainerWidget, "Training")

        self.mainUI.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.mainUI)

        self.showMaximized()

    def tab_changed(self, index):
        if(self.lastIndex is not None):
            tab = self.mainUI.widget(self.lastIndex)
            if (hasattr(tab, "tab_closed")):
                tab.tab_closed()

        tab = self.mainUI.widget(index)
        self.lastIndex = index
        if (hasattr(tab, "tab_selected")):
            tab.tab_selected()

    def setTabsEnabled(self, value: bool):
        for i in range(0, self.mainUI.count()):
            if(i == self.mainUI.currentIndex()):
                continue
            self.mainUI.setTabEnabled(i, value)

    def closeEvent(self, event):
        self.modelTrainerWidget.destroyTrainers()
        return super().closeEvent(event)

##############################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(app)
    window.show()
    sys.exit(app.exec())