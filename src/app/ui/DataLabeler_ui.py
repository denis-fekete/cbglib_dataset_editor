# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataLabeler.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

from app.widgets.ColorPicker import ColorPicker
from app.widgets.ImageSampleTreeView import ImageSampleTreeView
from app.widgets.LabelSelectorTreeView import LabelSelectorTreeView
from app.widgets.ZoomGraphicsView import ZoomGraphicsView

class Ui_DataLabeler(object):
    def setupUi(self, DataLabeler):
        if not DataLabeler.objectName():
            DataLabeler.setObjectName(u"DataLabeler")
        DataLabeler.resize(1062, 636)
        self.gridLayout = QGridLayout(DataLabeler)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolbarWidget = QWidget(DataLabeler)
        self.toolbarWidget.setObjectName(u"toolbarWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbarWidget.sizePolicy().hasHeightForWidth())
        self.toolbarWidget.setSizePolicy(sizePolicy)
        self.toolbarWidget.setMinimumSize(QSize(0, 60))
        self.toolbarWidget.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_3 = QHBoxLayout(self.toolbarWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelboxToolbarWidget = QWidget(self.toolbarWidget)
        self.labelboxToolbarWidget.setObjectName(u"labelboxToolbarWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelboxToolbarWidget.sizePolicy().hasHeightForWidth())
        self.labelboxToolbarWidget.setSizePolicy(sizePolicy1)
        self.labelboxToolbarWidget.setMinimumSize(QSize(300, 0))
        self.labelboxToolbarWidget.setMaximumSize(QSize(300, 16777215))
        self.horizontalLayout = QHBoxLayout(self.labelboxToolbarWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.newLabelBoxButton = QPushButton(self.labelboxToolbarWidget)
        self.newLabelBoxButton.setObjectName(u"newLabelBoxButton")

        self.horizontalLayout.addWidget(self.newLabelBoxButton)

        self.deleteLabelBoxButton = QPushButton(self.labelboxToolbarWidget)
        self.deleteLabelBoxButton.setObjectName(u"deleteLabelBoxButton")

        self.horizontalLayout.addWidget(self.deleteLabelBoxButton)


        self.horizontalLayout_3.addWidget(self.labelboxToolbarWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_3.addItem(self.verticalSpacer)

        self.autodetectWidget = QWidget(self.toolbarWidget)
        self.autodetectWidget.setObjectName(u"autodetectWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.autodetectWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.autoDetectButton = QPushButton(self.autodetectWidget)
        self.autoDetectButton.setObjectName(u"autoDetectButton")

        self.horizontalLayout_4.addWidget(self.autoDetectButton)

        self.modelPathLabel = QLabel(self.autodetectWidget)
        self.modelPathLabel.setObjectName(u"modelPathLabel")

        self.horizontalLayout_4.addWidget(self.modelPathLabel)

        self.modelPathLineEdit = QLineEdit(self.autodetectWidget)
        self.modelPathLineEdit.setObjectName(u"modelPathLineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modelPathLineEdit.sizePolicy().hasHeightForWidth())
        self.modelPathLineEdit.setSizePolicy(sizePolicy2)
        self.modelPathLineEdit.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.modelPathLineEdit)

        self.openModelButton = QPushButton(self.autodetectWidget)
        self.openModelButton.setObjectName(u"openModelButton")

        self.horizontalLayout_4.addWidget(self.openModelButton)

        self.loadModelButton = QPushButton(self.autodetectWidget)
        self.loadModelButton.setObjectName(u"loadModelButton")

        self.horizontalLayout_4.addWidget(self.loadModelButton)


        self.horizontalLayout_3.addWidget(self.autodetectWidget)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_3.addItem(self.verticalSpacer_2)

        self.colorsWidget = QWidget(self.toolbarWidget)
        self.colorsWidget.setObjectName(u"colorsWidget")
        sizePolicy1.setHeightForWidth(self.colorsWidget.sizePolicy().hasHeightForWidth())
        self.colorsWidget.setSizePolicy(sizePolicy1)
        self.colorsWidget.setMinimumSize(QSize(150, 0))
        self.colorsWidget.setMaximumSize(QSize(150, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.colorsWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.selectedColorPicker = ColorPicker(self.colorsWidget)
        self.selectedColorPicker.setObjectName(u"selectedColorPicker")

        self.horizontalLayout_2.addWidget(self.selectedColorPicker)

        self.unselectedColorPicker = ColorPicker(self.colorsWidget)
        self.unselectedColorPicker.setObjectName(u"unselectedColorPicker")

        self.horizontalLayout_2.addWidget(self.unselectedColorPicker)


        self.horizontalLayout_3.addWidget(self.colorsWidget)


        self.gridLayout.addWidget(self.toolbarWidget, 0, 0, 1, 3)

        self.imageSamplesWidget = QWidget(DataLabeler)
        self.imageSamplesWidget.setObjectName(u"imageSamplesWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.imageSamplesWidget.sizePolicy().hasHeightForWidth())
        self.imageSamplesWidget.setSizePolicy(sizePolicy3)
        self.imageSamplesWidget.setMinimumSize(QSize(200, 0))
        self.imageSamplesWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_3 = QGridLayout(self.imageSamplesWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.previousSampleButton = QPushButton(self.imageSamplesWidget)
        self.previousSampleButton.setObjectName(u"previousSampleButton")

        self.gridLayout_3.addWidget(self.previousSampleButton, 1, 0, 1, 1)

        self.nextSampleButton = QPushButton(self.imageSamplesWidget)
        self.nextSampleButton.setObjectName(u"nextSampleButton")

        self.gridLayout_3.addWidget(self.nextSampleButton, 1, 1, 1, 1)

        self.imageSampleTreeView = ImageSampleTreeView(self.imageSamplesWidget)
        self.imageSampleTreeView.setObjectName(u"imageSampleTreeView")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.imageSampleTreeView.sizePolicy().hasHeightForWidth())
        self.imageSampleTreeView.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.imageSampleTreeView, 2, 0, 1, 2)

        self.imageSamplesLabel = QLabel(self.imageSamplesWidget)
        self.imageSamplesLabel.setObjectName(u"imageSamplesLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.imageSamplesLabel.sizePolicy().hasHeightForWidth())
        self.imageSamplesLabel.setSizePolicy(sizePolicy5)
        self.imageSamplesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.imageSamplesLabel, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.imageSamplesWidget, 1, 0, 1, 1)

        self.graphicsView = ZoomGraphicsView(DataLabeler)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy4.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.graphicsView, 1, 1, 1, 1)

        self.labelsWidget = QWidget(DataLabeler)
        self.labelsWidget.setObjectName(u"labelsWidget")
        sizePolicy3.setHeightForWidth(self.labelsWidget.sizePolicy().hasHeightForWidth())
        self.labelsWidget.setSizePolicy(sizePolicy3)
        self.labelsWidget.setMinimumSize(QSize(150, 0))
        self.labelsWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_5 = QGridLayout(self.labelsWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.deleteClassLabelButton = QPushButton(self.labelsWidget)
        self.deleteClassLabelButton.setObjectName(u"deleteClassLabelButton")

        self.gridLayout_5.addWidget(self.deleteClassLabelButton, 1, 1, 1, 1)

        self.newClassLabelButton = QPushButton(self.labelsWidget)
        self.newClassLabelButton.setObjectName(u"newClassLabelButton")

        self.gridLayout_5.addWidget(self.newClassLabelButton, 1, 0, 1, 1)

        self.labelSelectorTreeView = LabelSelectorTreeView(self.labelsWidget)
        self.labelSelectorTreeView.setObjectName(u"labelSelectorTreeView")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.labelSelectorTreeView.sizePolicy().hasHeightForWidth())
        self.labelSelectorTreeView.setSizePolicy(sizePolicy6)
        self.labelSelectorTreeView.setMinimumSize(QSize(0, 0))

        self.gridLayout_5.addWidget(self.labelSelectorTreeView, 2, 0, 1, 2)

        self.labelClassesLabel = QLabel(self.labelsWidget)
        self.labelClassesLabel.setObjectName(u"labelClassesLabel")
        sizePolicy5.setHeightForWidth(self.labelClassesLabel.sizePolicy().hasHeightForWidth())
        self.labelClassesLabel.setSizePolicy(sizePolicy5)
        self.labelClassesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.labelClassesLabel, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.labelsWidget, 1, 2, 2, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(DataLabeler)

        QMetaObject.connectSlotsByName(DataLabeler)
    # setupUi

    def retranslateUi(self, DataLabeler):
        DataLabeler.setWindowTitle(QCoreApplication.translate("DataLabeler", u"Form", None))
        self.newLabelBoxButton.setText(QCoreApplication.translate("DataLabeler", u"New Label ( Space )", None))
        self.deleteLabelBoxButton.setText(QCoreApplication.translate("DataLabeler", u"Delete Label ( X )", None))
        self.autoDetectButton.setText(QCoreApplication.translate("DataLabeler", u"Detect ( Tab )", None))
        self.modelPathLabel.setText(QCoreApplication.translate("DataLabeler", u"Model path:", None))
        self.openModelButton.setText(QCoreApplication.translate("DataLabeler", u"Open", None))
        self.loadModelButton.setText(QCoreApplication.translate("DataLabeler", u"Load", None))
        self.selectedColorPicker.setText("")
        self.unselectedColorPicker.setText("")
        self.previousSampleButton.setText(QCoreApplication.translate("DataLabeler", u"Previous ( Q )", None))
        self.nextSampleButton.setText(QCoreApplication.translate("DataLabeler", u"Next ( E )", None))
        self.imageSamplesLabel.setText(QCoreApplication.translate("DataLabeler", u"Image Samples", None))
        self.deleteClassLabelButton.setText(QCoreApplication.translate("DataLabeler", u"Delete", None))
        self.newClassLabelButton.setText(QCoreApplication.translate("DataLabeler", u"New", None))
        self.labelClassesLabel.setText(QCoreApplication.translate("DataLabeler", u"Label classes", None))
    # retranslateUi

