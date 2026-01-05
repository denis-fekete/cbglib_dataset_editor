from PySide6 import QtWidgets
from PySide6.QtGui import QCloseEvent

import sys

from app.widgets import *
from app.utils import *
from app.activities import *
from app.image_manipulation import *
from app.data_classes import *

##############################################################################


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, qtApp: QtWidgets.QApplication):
        super().__init__()
        self.qtApp = qtApp

        SharedValues().screen = self.qtApp.primaryScreen()
        SharedValues().filterPresets = getDefaultFilterPresets()
        self.lastIndex: int | None = None

        self.initWindow()
        self._initUI()

    def initWindow(self):
        screenWidth, screenHeight = (
            SharedValues().screen.geometry().width(),
            SharedValues().screen.geometry().height(),
        )
        windowWidth, windowHeight = screenWidth / 2, screenHeight / 2

        if windowWidth < 640 or windowHeight < 480:
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
        self.datasetWidget = DatasetLoader(
            self.dataLabelerWidget.screenScaleText, self.setTabsEnabled
        )
        self.syntheticDataCreatorWidget = SyntheticDataCreator(
            self.dataLabelerWidget.getCurrentImageSample
        )
        self.modelTrainerWidget = ModelTrainer(self.setTabsEnabled)

        self.mainUI.addTab(self.datasetWidget, "Dataset")
        self.mainUI.addTab(self.dataLabelerWidget, "Image labeling")
        self.mainUI.addTab(self.syntheticDataCreatorWidget, "Synthetic data")
        self.mainUI.addTab(self.modelTrainerWidget, "Training")

        self.mainUI.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.mainUI)

        self.showMaximized()

    def tabChanged(self, index: int):
        if self.lastIndex is not None:
            tab = self.mainUI.widget(self.lastIndex)
            if isinstance(tab, AbstractTabWidget):
                tab.tabClosed()

        tab = self.mainUI.widget(index)
        self.lastIndex = index
        if isinstance(tab, AbstractTabWidget):
            tab.tabSelected()

    def setTabsEnabled(self, value: bool):
        for i in range(0, self.mainUI.count()):
            if i == self.mainUI.currentIndex():
                continue
            self.mainUI.setTabEnabled(i, value)

    def closeEvent(self, event: QCloseEvent):
        self.modelTrainerWidget.destroyTrainers()
        return super().closeEvent(event)


##############################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(app)
    window.show()
    sys.exit(app.exec())
