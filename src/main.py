"""
Module: main.py
Author: Denis Fekete (xfeket01@vutbr.cz, denis.fekete02@gmail.com)
Created: 2026-02-02

Description:
    Main file for project cbglib_dataset_editor. This application (or tool) is to provide a
    simplified way to create a labeled image datasets that can be enhanced with synthetic data.
    Application also provides a way to train data in application.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent

import sys

from app.labeling import *
from app.dataset import *
from app.synthetic import *
from app.widgets import *
from app.utils import *
from app.training import *
from app.activities import *
from app.settings import *

##############################################################################


class MyWindow(QtWidgets.QMainWindow):
    clearCurrentImageSample = Signal()

    def __init__(self, qtApp: QtWidgets.QApplication) -> None:
        super().__init__()
        self.qtApp = qtApp

        SharedValues().screen = self.qtApp.primaryScreen()
        self.lastIndex: int | None = None

        self.initWindow()
        self._initUI()

    def initWindow(self) -> None:
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

    def _initUI(self) -> None:
        self.mainUI = QtWidgets.QTabWidget()
        self.dataLabelerWidget = DataLabeler()
        self.datasetWidget = DatasetLoader(
            self.dataLabelerWidget.screenScaleText, self.setTabsEnabled
        )
        self.syntheticDataCreatorWidget = SyntheticDataCreator(
            self.dataLabelerWidget.getCurrentImageSample
        )
        self.modelTrainerWidget = ModelTrainer(self.setTabsEnabled)

        self.datasetWidget.onImport.connect(
            self.dataLabelerWidget.clearCurrentImageSample
        )

        self.mainUI.addTab(self.datasetWidget, "Dataset")
        self.mainUI.addTab(self.dataLabelerWidget, "Image labeling")
        self.mainUI.addTab(self.syntheticDataCreatorWidget, "Synthetic data")
        self.mainUI.addTab(self.modelTrainerWidget, "Training")

        self.mainUI.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.mainUI)

        self.loadSettings()
        self.datasetWidget.loadSettings()
        self.dataLabelerWidget.loadSettings()
        self.modelTrainerWidget.loadSettings()

        self.showMaximized()

    def tabChanged(self, index: int) -> None:
        if self.lastIndex is not None:
            tab = self.mainUI.widget(self.lastIndex)
            if isinstance(tab, AbstractTabWidget):
                tab.tabClosed()

        tab = self.mainUI.widget(index)
        self.lastIndex = index
        if isinstance(tab, AbstractTabWidget):
            tab.tabSelected()

    def setTabsEnabled(self, value: bool) -> None:
        for i in range(0, self.mainUI.count()):
            if i == self.mainUI.currentIndex():
                continue
            self.mainUI.setTabEnabled(i, value)

    def loadSettings(self) -> None:
        try:
            with open(r"settings.json", "r", encoding="utf-8") as f:
                SharedValues().settings = AppSettings.from_json(f.read())  # type: ignore
        except:
            with open(
                r"src/app/settings/default_settings.json", "r", encoding="utf-8"
            ) as f:
                SharedValues().settings = AppSettings.from_json(f.read())  # type: ignore

        SharedValues().filterPresets = SharedValues().settings.syntheticSettings.filters

    def saveSettings(self) -> None:

        self.datasetWidget.updateSettings()
        self.dataLabelerWidget.updateSettings()
        SharedValues().settings.syntheticSettings.filters = SharedValues().filterPresets
        self.modelTrainerWidget.updateSettings()

        jsonStr = SharedValues().settings.to_json(indent=4)  # type: ignore
        with open("settings.json", "w", encoding="utf-8") as f:
            f.write(jsonStr)  # type: ignore

    def closeEvent(self, event: QCloseEvent) -> None:
        self.modelTrainerWidget.destroyTrainers()

        self.saveSettings()

        return super().closeEvent(event)


##############################################################################

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(app)
    window.show()
    sys.exit(app.exec())

# for direct python execution
if __name__ == "__main__":
    main()