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
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QCloseEvent

from app.ui import *

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


class MainWindow(QtWidgets.QMainWindow):
    clearCurrentImageSample = Signal()

    def __init__(self, qtApp: QtWidgets.QApplication) -> None:
        super().__init__()
        self.lastIndex: int | None = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.qtApp = qtApp
        SharedValues().screen = self.qtApp.primaryScreen()

        self.setupTabs()
        self.showMaximized()

    def setupTabs(self) -> None:
        """Sets up tabs of the widget."""
        # designer does not allow to change the type of central widget, force the change in code
        self.setCentralWidget(self.ui.tabWidget)

        self.ui.tabWidget.clear()

        self.dataLabelerWidget = DataLabeler()
        self.datasetWidget = DatasetManager(
            self.dataLabelerWidget.screenScaleText, self.setTabsEnabled
        )
        self.syntheticDataCreatorWidget = SyntheticFiltersEditor(
            self.dataLabelerWidget.getCurrentImageSample
        )
        self.modelTrainerWidget = ModelTrainer(self.setTabsEnabled)

        self.datasetWidget.onImportStart.connect(
            self.dataLabelerWidget.clearCurrentImageSample
        )
        self.datasetWidget.onImportEnded.connect(
            self.dataLabelerWidget.reloadImageSamplesTree
        )

        self.ui.tabWidget.addTab(self.datasetWidget, "Dataset")
        self.ui.tabWidget.addTab(self.dataLabelerWidget, "Image labeling")
        self.ui.tabWidget.addTab(self.syntheticDataCreatorWidget, "Synthetic data")
        self.ui.tabWidget.addTab(self.modelTrainerWidget, "Training")

        self.ui.tabWidget.currentChanged.connect(self.tabChanged)

        self.loadSettings()
        self.datasetWidget.loadSettings()
        self.dataLabelerWidget.loadSettings()
        self.modelTrainerWidget.loadSettings()

    def setTabsEnabled(self, value: bool) -> None:
        """Enables/disable all tabs except the current one."""
        for i in range(0, self.ui.tabWidget.count()):
            if i == self.ui.tabWidget.currentIndex():
                continue
            self.ui.tabWidget.setTabEnabled(i, value)

    @Slot(int)
    def tabChanged(self, index: int) -> None:
        """Slot called when tab was changed."""
        if self.lastIndex is not None:
            tab = self.ui.tabWidget.widget(self.lastIndex)
            if isinstance(tab, AbstractTabWidget):
                tab.tabClosed()

        tab = self.ui.tabWidget.widget(index)
        self.lastIndex = index
        if isinstance(tab, AbstractTabWidget):
            tab.tabSelected()

    def loadSettings(self) -> None:
        """Loads values used by the application from `settings.json`"""
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
        """Saves values used by the application into `settings.json`."""

        self.datasetWidget.updateSettings()
        self.dataLabelerWidget.updateSettings()
        SharedValues().settings.syntheticSettings.filters = SharedValues().filterPresets
        self.modelTrainerWidget.updateSettings()

        jsonStr = SharedValues().settings.to_json(indent=4)  # type: ignore
        with open("settings.json", "w", encoding="utf-8") as f:
            f.write(jsonStr)  # type: ignore

    def closeEvent(self, event: QCloseEvent) -> None:
        """Event called when window is destroyed/closed."""
        self.modelTrainerWidget.destroyTrainers()

        self.saveSettings()

        return super().closeEvent(event)


##############################################################################


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(app)

    window.show()
    sys.exit(app.exec())


# for direct python execution
if __name__ == "__main__":
    main()
