# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SyntheticFiltersEditor.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QWidget)

from app.widgets.FilterPresetTreeView import FilterPresetTreeView
from app.widgets.ZoomGraphicsView import ZoomGraphicsView

class Ui_SyntheticFiltersEditor(object):
    def setupUi(self, SyntheticFiltersEditor):
        if not SyntheticFiltersEditor.objectName():
            SyntheticFiltersEditor.setObjectName(u"SyntheticFiltersEditor")
        SyntheticFiltersEditor.resize(1036, 537)
        self.gridLayout_3 = QGridLayout(SyntheticFiltersEditor)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.scrollArea = QScrollArea(SyntheticFiltersEditor)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(300, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, -115, 286, 668))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.filterSettingsWidget = QWidget(self.scrollAreaWidgetContents_2)
        self.filterSettingsWidget.setObjectName(u"filterSettingsWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filterSettingsWidget.sizePolicy().hasHeightForWidth())
        self.filterSettingsWidget.setSizePolicy(sizePolicy1)
        self.filterSettingsWidget.setMinimumSize(QSize(200, 0))
        self.filterSettingsWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(self.filterSettingsWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 18, 0, 1, 2)

        self.gaussianSpinBox = QSpinBox(self.filterSettingsWidget)
        self.gaussianSpinBox.setObjectName(u"gaussianSpinBox")
        self.gaussianSpinBox.setMaximum(1000)

        self.gridLayout_2.addWidget(self.gaussianSpinBox, 16, 1, 1, 1)

        self.blurSpinBox = QSpinBox(self.filterSettingsWidget)
        self.blurSpinBox.setObjectName(u"blurSpinBox")
        self.blurSpinBox.setMaximum(100)
        self.blurSpinBox.setSingleStep(2)

        self.gridLayout_2.addWidget(self.blurSpinBox, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 6, 0, 1, 2)

        self.saturationSlider = QSlider(self.filterSettingsWidget)
        self.saturationSlider.setObjectName(u"saturationSlider")
        self.saturationSlider.setMinimum(50)
        self.saturationSlider.setMaximum(150)
        self.saturationSlider.setValue(99)
        self.saturationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.saturationSlider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.gridLayout_2.addWidget(self.saturationSlider, 5, 0, 1, 2)

        self.sapSpinBox = QSpinBox(self.filterSettingsWidget)
        self.sapSpinBox.setObjectName(u"sapSpinBox")
        self.sapSpinBox.setMaximum(1000)

        self.gridLayout_2.addWidget(self.sapSpinBox, 13, 1, 1, 1)

        self.sapLabel = QLabel(self.filterSettingsWidget)
        self.sapLabel.setObjectName(u"sapLabel")

        self.gridLayout_2.addWidget(self.sapLabel, 13, 0, 1, 1)

        self.gaussianSlider = QSlider(self.filterSettingsWidget)
        self.gaussianSlider.setObjectName(u"gaussianSlider")
        self.gaussianSlider.setMaximum(1000)
        self.gaussianSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.gaussianSlider, 17, 0, 1, 2)

        self.contrastSlider = QSlider(self.filterSettingsWidget)
        self.contrastSlider.setObjectName(u"contrastSlider")
        self.contrastSlider.setMinimum(50)
        self.contrastSlider.setMaximum(150)
        self.contrastSlider.setValue(100)
        self.contrastSlider.setOrientation(Qt.Orientation.Horizontal)
        self.contrastSlider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.gridLayout_2.addWidget(self.contrastSlider, 8, 0, 1, 2)

        self.brightnessSlider = QSlider(self.filterSettingsWidget)
        self.brightnessSlider.setObjectName(u"brightnessSlider")
        self.brightnessSlider.setMinimum(-50)
        self.brightnessSlider.setMaximum(50)
        self.brightnessSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.brightnessSlider, 11, 0, 1, 2)

        self.flipWidget = QWidget(self.filterSettingsWidget)
        self.flipWidget.setObjectName(u"flipWidget")
        self.flipWidget.setMinimumSize(QSize(0, 50))
        self.horizontalLayout = QHBoxLayout(self.flipWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalCheckBox = QCheckBox(self.flipWidget)
        self.verticalCheckBox.setObjectName(u"verticalCheckBox")

        self.horizontalLayout.addWidget(self.verticalCheckBox)

        self.horizontalCheckBox = QCheckBox(self.flipWidget)
        self.horizontalCheckBox.setObjectName(u"horizontalCheckBox")

        self.horizontalLayout.addWidget(self.horizontalCheckBox)


        self.gridLayout_2.addWidget(self.flipWidget, 19, 0, 1, 2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 20, 0, 1, 2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 15, 0, 1, 2)

        self.saturationLabel = QLabel(self.filterSettingsWidget)
        self.saturationLabel.setObjectName(u"saturationLabel")

        self.gridLayout_2.addWidget(self.saturationLabel, 4, 0, 1, 1)

        self.blurLabel = QLabel(self.filterSettingsWidget)
        self.blurLabel.setObjectName(u"blurLabel")

        self.gridLayout_2.addWidget(self.blurLabel, 1, 0, 1, 1)

        self.gaussianLabel = QLabel(self.filterSettingsWidget)
        self.gaussianLabel.setObjectName(u"gaussianLabel")

        self.gridLayout_2.addWidget(self.gaussianLabel, 16, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 12, 0, 1, 2)

        self.sapSlider = QSlider(self.filterSettingsWidget)
        self.sapSlider.setObjectName(u"sapSlider")
        self.sapSlider.setMaximum(1000)
        self.sapSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.sapSlider, 14, 0, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 9, 0, 1, 2)

        self.brightnessSpinBox = QSpinBox(self.filterSettingsWidget)
        self.brightnessSpinBox.setObjectName(u"brightnessSpinBox")
        self.brightnessSpinBox.setMinimum(-50)
        self.brightnessSpinBox.setMaximum(50)

        self.gridLayout_2.addWidget(self.brightnessSpinBox, 10, 1, 1, 1)

        self.contrastSpinBox = QSpinBox(self.filterSettingsWidget)
        self.contrastSpinBox.setObjectName(u"contrastSpinBox")
        self.contrastSpinBox.setMinimum(50)
        self.contrastSpinBox.setMaximum(150)
        self.contrastSpinBox.setValue(100)

        self.gridLayout_2.addWidget(self.contrastSpinBox, 7, 1, 1, 1)

        self.contrastLabel = QLabel(self.filterSettingsWidget)
        self.contrastLabel.setObjectName(u"contrastLabel")

        self.gridLayout_2.addWidget(self.contrastLabel, 7, 0, 1, 1)

        self.brightnessLabel = QLabel(self.filterSettingsWidget)
        self.brightnessLabel.setObjectName(u"brightnessLabel")

        self.gridLayout_2.addWidget(self.brightnessLabel, 10, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 3, 0, 1, 2)

        self.saturationSpinBox = QSpinBox(self.filterSettingsWidget)
        self.saturationSpinBox.setObjectName(u"saturationSpinBox")
        self.saturationSpinBox.setMinimum(50)
        self.saturationSpinBox.setMaximum(150)
        self.saturationSpinBox.setValue(100)

        self.gridLayout_2.addWidget(self.saturationSpinBox, 4, 1, 1, 1)

        self.blurSlider = QSlider(self.filterSettingsWidget)
        self.blurSlider.setObjectName(u"blurSlider")
        self.blurSlider.setMaximum(100)
        self.blurSlider.setSingleStep(2)
        self.blurSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.blurSlider, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.filterSettingsWidget, 2, 0, 1, 1)

        self.imageSamplesLabel = QLabel(self.scrollAreaWidgetContents_2)
        self.imageSamplesLabel.setObjectName(u"imageSamplesLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.imageSamplesLabel.sizePolicy().hasHeightForWidth())
        self.imageSamplesLabel.setSizePolicy(sizePolicy2)
        self.imageSamplesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.imageSamplesLabel, 0, 0, 1, 1)

        self.applyFiltersButton = QPushButton(self.scrollAreaWidgetContents_2)
        self.applyFiltersButton.setObjectName(u"applyFiltersButton")

        self.gridLayout.addWidget(self.applyFiltersButton, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.graphicsView = ZoomGraphicsView(SyntheticFiltersEditor)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy1.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.graphicsView, 0, 1, 1, 1)

        self.filterBrowserWidget = QWidget(SyntheticFiltersEditor)
        self.filterBrowserWidget.setObjectName(u"filterBrowserWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filterBrowserWidget.sizePolicy().hasHeightForWidth())
        self.filterBrowserWidget.setSizePolicy(sizePolicy3)
        self.filterBrowserWidget.setMinimumSize(QSize(150, 0))
        self.filterBrowserWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_5 = QGridLayout(self.filterBrowserWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.deleteFilterButton = QPushButton(self.filterBrowserWidget)
        self.deleteFilterButton.setObjectName(u"deleteFilterButton")

        self.gridLayout_5.addWidget(self.deleteFilterButton, 1, 1, 1, 1)

        self.newFilterButton = QPushButton(self.filterBrowserWidget)
        self.newFilterButton.setObjectName(u"newFilterButton")

        self.gridLayout_5.addWidget(self.newFilterButton, 1, 0, 1, 1)

        self.filterPresetTreeView = FilterPresetTreeView(self.filterBrowserWidget)
        self.filterPresetTreeView.setObjectName(u"filterPresetTreeView")
        sizePolicy.setHeightForWidth(self.filterPresetTreeView.sizePolicy().hasHeightForWidth())
        self.filterPresetTreeView.setSizePolicy(sizePolicy)
        self.filterPresetTreeView.setMinimumSize(QSize(0, 0))

        self.gridLayout_5.addWidget(self.filterPresetTreeView, 2, 0, 1, 2)

        self.filtersLabel = QLabel(self.filterBrowserWidget)
        self.filtersLabel.setObjectName(u"filtersLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.filtersLabel.sizePolicy().hasHeightForWidth())
        self.filtersLabel.setSizePolicy(sizePolicy4)
        self.filtersLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.filtersLabel, 0, 0, 1, 2)


        self.gridLayout_3.addWidget(self.filterBrowserWidget, 0, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(1, 1)

        self.retranslateUi(SyntheticFiltersEditor)

        QMetaObject.connectSlotsByName(SyntheticFiltersEditor)
    # setupUi

    def retranslateUi(self, SyntheticFiltersEditor):
        SyntheticFiltersEditor.setWindowTitle(QCoreApplication.translate("SyntheticFiltersEditor", u"Form", None))
        self.gaussianSpinBox.setSuffix(QCoreApplication.translate("SyntheticFiltersEditor", u" / 10 %", None))
        self.sapSpinBox.setSuffix(QCoreApplication.translate("SyntheticFiltersEditor", u" / 10 %", None))
        self.sapLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Salt and Pepper noise", None))
        self.verticalCheckBox.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Flip vertically", None))
        self.horizontalCheckBox.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Flip horizontally", None))
        self.saturationLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Saturation", None))
        self.blurLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Blur", None))
        self.gaussianLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Gaussian noise", None))
        self.contrastLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Contrast", None))
        self.brightnessLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Brightness", None))
        self.imageSamplesLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Filter settings:", None))
        self.applyFiltersButton.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Apply ( Tab )", None))
        self.deleteFilterButton.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Delete", None))
        self.newFilterButton.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"New", None))
        self.filtersLabel.setText(QCoreApplication.translate("SyntheticFiltersEditor", u"Filters for synthetic data", None))
    # retranslateUi

