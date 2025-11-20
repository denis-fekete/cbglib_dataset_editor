import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QScreen

from widgets import *
from utils import *
from activities import *

##############################################################################

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, qtApp):
        super().__init__()
        self.qtApp = qtApp
        self.imageSamples = []
        self._screen: QScreen = self.qtApp.primaryScreen()
        self.labelsDict: dict[int, LabelEntry] = {}
        self.lastIndex = None

        self.initWindow()
        self.initUI()

        
    def initWindow(self):
        screenWidth, screenHeight = self._screen.geometry().width(), self._screen.geometry().height()
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

        self.showMaximized()

    def initUI(self):
        self.mainUI = QtWidgets.QTabWidget()
        self.dataLabelerWidget = DataLabeler(self.imageSamples, self.labelsDict, self._screen) 
        self.datasetWidget = DatasetLoader(self.imageSamples, self.labelsDict, self.dataLabelerWidget._handleScaleByView) 
        self.modelTrainingWidget = QtWidgets.QWidget() 

        self.mainUI.addTab(self.datasetWidget, "Dataset")
        self.mainUI.addTab(self.dataLabelerWidget, "Image labeling")
        self.mainUI.addTab(self.modelTrainingWidget, "Training")

        self.mainUI.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.mainUI)

    def tab_changed(self, index):
        if(self.lastIndex is not None):
            tab = self.mainUI.widget(self.lastIndex)
            if (hasattr(tab, "tab_closed")):
                tab.tab_closed()

        tab = self.mainUI.widget(index)
        self.lastIndex = index
        if (hasattr(tab, "tab_selected")):
            tab.tab_selected()



##############################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(app)
    window.show()
    sys.exit(app.exec())