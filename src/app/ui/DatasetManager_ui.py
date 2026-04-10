# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatasetManager.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from app.widgets.ImageSampleTreeView import ImageSampleTreeView
from app.widgets.LabelSelectorTreeView import LabelSelectorTreeView

class Ui_DatasetManager(object):
    def setupUi(self, DatasetManager):
        if not DatasetManager.objectName():
            DatasetManager.setObjectName(u"DatasetManager")
        DatasetManager.resize(1055, 644)
        DatasetManager.setMinimumSize(QSize(1055, 616))
        self.gridLayout_2 = QGridLayout(DatasetManager)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.detailsWidget = QWidget(DatasetManager)
        self.detailsWidget.setObjectName(u"detailsWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailsWidget.sizePolicy().hasHeightForWidth())
        self.detailsWidget.setSizePolicy(sizePolicy)
        self.detailsWidget.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(self.detailsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.statisticsForm = QFormLayout()
        self.statisticsForm.setObjectName(u"statisticsForm")
        self.labelFilesLabel = QLabel(self.detailsWidget)
        self.labelFilesLabel.setObjectName(u"labelFilesLabel")

        self.statisticsForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelFilesLabel)

        self.labelFilesLineEdit = QLineEdit(self.detailsWidget)
        self.labelFilesLineEdit.setObjectName(u"labelFilesLineEdit")

        self.statisticsForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.labelFilesLineEdit)

        self.imagesSamplesLabel = QLabel(self.detailsWidget)
        self.imagesSamplesLabel.setObjectName(u"imagesSamplesLabel")

        self.statisticsForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.imagesSamplesLabel)

        self.imageSamplesLineEdit = QLineEdit(self.detailsWidget)
        self.imageSamplesLineEdit.setObjectName(u"imageSamplesLineEdit")

        self.statisticsForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.imageSamplesLineEdit)

        self.annotatedSamplesLabel = QLabel(self.detailsWidget)
        self.annotatedSamplesLabel.setObjectName(u"annotatedSamplesLabel")

        self.statisticsForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.annotatedSamplesLabel)

        self.annotatedLineEdit = QLineEdit(self.detailsWidget)
        self.annotatedLineEdit.setObjectName(u"annotatedLineEdit")

        self.statisticsForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.annotatedLineEdit)

        self.emptySamplesLabel = QLabel(self.detailsWidget)
        self.emptySamplesLabel.setObjectName(u"emptySamplesLabel")

        self.statisticsForm.setWidget(4, QFormLayout.ItemRole.LabelRole, self.emptySamplesLabel)

        self.emptySamplesLineEdit = QLineEdit(self.detailsWidget)
        self.emptySamplesLineEdit.setObjectName(u"emptySamplesLineEdit")

        self.statisticsForm.setWidget(4, QFormLayout.ItemRole.FieldRole, self.emptySamplesLineEdit)

        self.classesLabel = QLabel(self.detailsWidget)
        self.classesLabel.setObjectName(u"classesLabel")

        self.statisticsForm.setWidget(5, QFormLayout.ItemRole.LabelRole, self.classesLabel)

        self.totalClassesLineEdit = QLineEdit(self.detailsWidget)
        self.totalClassesLineEdit.setObjectName(u"totalClassesLineEdit")

        self.statisticsForm.setWidget(5, QFormLayout.ItemRole.FieldRole, self.totalClassesLineEdit)

        self.imageLabelBoxesLabel = QLabel(self.detailsWidget)
        self.imageLabelBoxesLabel.setObjectName(u"imageLabelBoxesLabel")

        self.statisticsForm.setWidget(6, QFormLayout.ItemRole.LabelRole, self.imageLabelBoxesLabel)

        self.labelBoxesLineEdit = QLineEdit(self.detailsWidget)
        self.labelBoxesLineEdit.setObjectName(u"labelBoxesLineEdit")

        self.statisticsForm.setWidget(6, QFormLayout.ItemRole.FieldRole, self.labelBoxesLineEdit)

        self.datasetStatisticsLabel = QLabel(self.detailsWidget)
        self.datasetStatisticsLabel.setObjectName(u"datasetStatisticsLabel")

        self.statisticsForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.datasetStatisticsLabel)

        self.trainSamplesLabel = QLabel(self.detailsWidget)
        self.trainSamplesLabel.setObjectName(u"trainSamplesLabel")

        self.statisticsForm.setWidget(7, QFormLayout.ItemRole.LabelRole, self.trainSamplesLabel)

        self.valSamplesLabel = QLabel(self.detailsWidget)
        self.valSamplesLabel.setObjectName(u"valSamplesLabel")

        self.statisticsForm.setWidget(8, QFormLayout.ItemRole.LabelRole, self.valSamplesLabel)

        self.testSamplesLabel = QLabel(self.detailsWidget)
        self.testSamplesLabel.setObjectName(u"testSamplesLabel")

        self.statisticsForm.setWidget(9, QFormLayout.ItemRole.LabelRole, self.testSamplesLabel)

        self.trainSamplesLineEdit = QLineEdit(self.detailsWidget)
        self.trainSamplesLineEdit.setObjectName(u"trainSamplesLineEdit")

        self.statisticsForm.setWidget(7, QFormLayout.ItemRole.FieldRole, self.trainSamplesLineEdit)

        self.valSamplesLineEdit = QLineEdit(self.detailsWidget)
        self.valSamplesLineEdit.setObjectName(u"valSamplesLineEdit")

        self.statisticsForm.setWidget(8, QFormLayout.ItemRole.FieldRole, self.valSamplesLineEdit)

        self.testSamplesLineEdit = QLineEdit(self.detailsWidget)
        self.testSamplesLineEdit.setObjectName(u"testSamplesLineEdit")

        self.statisticsForm.setWidget(9, QFormLayout.ItemRole.FieldRole, self.testSamplesLineEdit)


        self.verticalLayout.addLayout(self.statisticsForm)

        self.calcStatisticsButton = QPushButton(self.detailsWidget)
        self.calcStatisticsButton.setObjectName(u"calcStatisticsButton")

        self.verticalLayout.addWidget(self.calcStatisticsButton)

        self.datasetDetailsLabel = QLabel(self.detailsWidget)
        self.datasetDetailsLabel.setObjectName(u"datasetDetailsLabel")

        self.verticalLayout.addWidget(self.datasetDetailsLabel)

        self.detailsForm = QFormLayout()
        self.detailsForm.setObjectName(u"detailsForm")
        self.dataPathLabel = QLabel(self.detailsWidget)
        self.dataPathLabel.setObjectName(u"dataPathLabel")

        self.detailsForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.dataPathLabel)

        self.dataPathLineEdit = QLineEdit(self.detailsWidget)
        self.dataPathLineEdit.setObjectName(u"dataPathLineEdit")
        self.dataPathLineEdit.setEnabled(False)

        self.detailsForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dataPathLineEdit)

        self.trainLabel = QLabel(self.detailsWidget)
        self.trainLabel.setObjectName(u"trainLabel")

        self.detailsForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.trainLabel)

        self.trainLineEdit = QLineEdit(self.detailsWidget)
        self.trainLineEdit.setObjectName(u"trainLineEdit")
        self.trainLineEdit.setEnabled(False)

        self.detailsForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.trainLineEdit)

        self.valLabel = QLabel(self.detailsWidget)
        self.valLabel.setObjectName(u"valLabel")

        self.detailsForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.valLabel)

        self.valLineEdit = QLineEdit(self.detailsWidget)
        self.valLineEdit.setObjectName(u"valLineEdit")
        self.valLineEdit.setEnabled(False)

        self.detailsForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.valLineEdit)

        self.testLabel = QLabel(self.detailsWidget)
        self.testLabel.setObjectName(u"testLabel")

        self.detailsForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.testLabel)

        self.testLineEdit = QLineEdit(self.detailsWidget)
        self.testLineEdit.setObjectName(u"testLineEdit")
        self.testLineEdit.setEnabled(False)

        self.detailsForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.testLineEdit)


        self.verticalLayout.addLayout(self.detailsForm)

        self.classesTreeView = LabelSelectorTreeView(self.detailsWidget)
        self.classesTreeView.setObjectName(u"classesTreeView")

        self.verticalLayout.addWidget(self.classesTreeView)


        self.gridLayout_2.addWidget(self.detailsWidget, 0, 0, 2, 1)

        self.line_3 = QFrame(DatasetManager)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 0, 1, 2, 1)

        self.importExportWidget = QWidget(DatasetManager)
        self.importExportWidget.setObjectName(u"importExportWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.importExportWidget.sizePolicy().hasHeightForWidth())
        self.importExportWidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.importExportWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 0, 1, 3)

        self.importWidget = QWidget(self.importExportWidget)
        self.importWidget.setObjectName(u"importWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.importWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.importLabel = QLabel(self.importWidget)
        self.importLabel.setObjectName(u"importLabel")

        self.horizontalLayout_2.addWidget(self.importLabel)


        self.gridLayout.addWidget(self.importWidget, 0, 0, 1, 2)

        self.line = QFrame(self.importExportWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 11, 0, 1, 3)

        self.imageSampleTreeView = ImageSampleTreeView(self.importExportWidget)
        self.imageSampleTreeView.setObjectName(u"imageSampleTreeView")

        self.gridLayout.addWidget(self.imageSampleTreeView, 3, 0, 1, 3)

        self.exportButton = QPushButton(self.importExportWidget)
        self.exportButton.setObjectName(u"exportButton")

        self.gridLayout.addWidget(self.exportButton, 9, 2, 1, 1)

        self.importButton = QPushButton(self.importExportWidget)
        self.importButton.setObjectName(u"importButton")

        self.gridLayout.addWidget(self.importButton, 1, 2, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.workerThreadsLabel = QLabel(self.importExportWidget)
        self.workerThreadsLabel.setObjectName(u"workerThreadsLabel")
        self.workerThreadsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.workerThreadsLabel, 0, 4, 1, 1)

        self.exportOriginalCheckBox = QCheckBox(self.importExportWidget)
        self.exportOriginalCheckBox.setObjectName(u"exportOriginalCheckBox")

        self.gridLayout_3.addWidget(self.exportOriginalCheckBox, 0, 2, 1, 1)

        self.workerThreadsSpinBox = QSpinBox(self.importExportWidget)
        self.workerThreadsSpinBox.setObjectName(u"workerThreadsSpinBox")
        self.workerThreadsSpinBox.setMinimum(1)
        self.workerThreadsSpinBox.setMaximum(64)

        self.gridLayout_3.addWidget(self.workerThreadsSpinBox, 2, 4, 1, 1)

        self.separateCheckBox = QCheckBox(self.importExportWidget)
        self.separateCheckBox.setObjectName(u"separateCheckBox")

        self.gridLayout_3.addWidget(self.separateCheckBox, 0, 1, 1, 1)

        self.trainPercentSpinBox = QSpinBox(self.importExportWidget)
        self.trainPercentSpinBox.setObjectName(u"trainPercentSpinBox")
        self.trainPercentSpinBox.setMaximum(100)
        self.trainPercentSpinBox.setValue(80)

        self.gridLayout_3.addWidget(self.trainPercentSpinBox, 0, 0, 1, 1)

        self.genNamesCheckBox = QCheckBox(self.importExportWidget)
        self.genNamesCheckBox.setObjectName(u"genNamesCheckBox")

        self.gridLayout_3.addWidget(self.genNamesCheckBox, 2, 2, 1, 1)

        self.genSyntheticValCheckBox = QCheckBox(self.importExportWidget)
        self.genSyntheticValCheckBox.setObjectName(u"genSyntheticValCheckBox")

        self.gridLayout_3.addWidget(self.genSyntheticValCheckBox, 2, 1, 1, 1)

        self.genSyntheticTrainCheckBox = QCheckBox(self.importExportWidget)
        self.genSyntheticTrainCheckBox.setObjectName(u"genSyntheticTrainCheckBox")

        self.gridLayout_3.addWidget(self.genSyntheticTrainCheckBox, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 5, 0, 1, 3)

        self.exportLineEdit = QLineEdit(self.importExportWidget)
        self.exportLineEdit.setObjectName(u"exportLineEdit")

        self.gridLayout.addWidget(self.exportLineEdit, 9, 0, 1, 1)

        self.exportLabel = QLabel(self.importExportWidget)
        self.exportLabel.setObjectName(u"exportLabel")

        self.gridLayout.addWidget(self.exportLabel, 8, 0, 1, 1)

        self.exportOpenButton = QPushButton(self.importExportWidget)
        self.exportOpenButton.setObjectName(u"exportOpenButton")

        self.gridLayout.addWidget(self.exportOpenButton, 9, 1, 1, 1)

        self.importOpenButton = QPushButton(self.importExportWidget)
        self.importOpenButton.setObjectName(u"importOpenButton")

        self.gridLayout.addWidget(self.importOpenButton, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 3)

        self.importLineEdit = QLineEdit(self.importExportWidget)
        self.importLineEdit.setObjectName(u"importLineEdit")

        self.gridLayout.addWidget(self.importLineEdit, 1, 0, 1, 1)

        self.exportWorkersWidget = QWidget(self.importExportWidget)
        self.exportWorkersWidget.setObjectName(u"exportWorkersWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.exportWorkersWidget.sizePolicy().hasHeightForWidth())
        self.exportWorkersWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.exportWorkersWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.gridLayout.addWidget(self.exportWorkersWidget, 6, 0, 1, 2)


        self.gridLayout_2.addWidget(self.importExportWidget, 0, 2, 1, 1)

        self.exportWidget = QWidget(DatasetManager)
        self.exportWidget.setObjectName(u"exportWidget")
        self.exportWidget.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.exportWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.exportProgressBar = QProgressBar(self.exportWidget)
        self.exportProgressBar.setObjectName(u"exportProgressBar")
        self.exportProgressBar.setEnabled(True)
        self.exportProgressBar.setValue(0)

        self.horizontalLayout.addWidget(self.exportProgressBar)


        self.gridLayout_2.addWidget(self.exportWidget, 1, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(2, 1)

        self.retranslateUi(DatasetManager)

        QMetaObject.connectSlotsByName(DatasetManager)
    # setupUi

    def retranslateUi(self, DatasetManager):
        DatasetManager.setWindowTitle(QCoreApplication.translate("DatasetManager", u"Form", None))
        self.labelFilesLabel.setText(QCoreApplication.translate("DatasetManager", u"Label files", None))
        self.imagesSamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Image Samples:", None))
        self.annotatedSamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Annotated Image Samples", None))
        self.emptySamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Empty image samples", None))
        self.classesLabel.setText(QCoreApplication.translate("DatasetManager", u"Total classes", None))
        self.imageLabelBoxesLabel.setText(QCoreApplication.translate("DatasetManager", u"Image label boxes count", None))
        self.datasetStatisticsLabel.setText(QCoreApplication.translate("DatasetManager", u"Dataset statistics:", None))
        self.trainSamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Train samples", None))
        self.valSamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Validation samples", None))
        self.testSamplesLabel.setText(QCoreApplication.translate("DatasetManager", u"Test samples", None))
        self.calcStatisticsButton.setText(QCoreApplication.translate("DatasetManager", u"Calculate Statistics", None))
        self.datasetDetailsLabel.setText(QCoreApplication.translate("DatasetManager", u"Dataset details (data.yaml):", None))
        self.dataPathLabel.setText(QCoreApplication.translate("DatasetManager", u"path:", None))
        self.trainLabel.setText(QCoreApplication.translate("DatasetManager", u"train:", None))
        self.valLabel.setText(QCoreApplication.translate("DatasetManager", u"val:", None))
        self.testLabel.setText(QCoreApplication.translate("DatasetManager", u"test:", None))
        self.importLabel.setText(QCoreApplication.translate("DatasetManager", u"Import path:", None))
        self.exportButton.setText(QCoreApplication.translate("DatasetManager", u"Export", None))
        self.importButton.setText(QCoreApplication.translate("DatasetManager", u"Import", None))
        self.workerThreadsLabel.setText(QCoreApplication.translate("DatasetManager", u"Export Worker threads:", None))
        self.exportOriginalCheckBox.setText(QCoreApplication.translate("DatasetManager", u"Export original image", None))
        self.separateCheckBox.setText(QCoreApplication.translate("DatasetManager", u"Separate into subdirectories", None))
        self.trainPercentSpinBox.setPrefix(QCoreApplication.translate("DatasetManager", u"Traid data %:  ", None))
        self.genNamesCheckBox.setText(QCoreApplication.translate("DatasetManager", u"Generate names", None))
        self.genSyntheticValCheckBox.setText(QCoreApplication.translate("DatasetManager", u"Generate synthetic for validation", None))
        self.genSyntheticTrainCheckBox.setText(QCoreApplication.translate("DatasetManager", u"Generate synthetic for training", None))
        self.exportLabel.setText(QCoreApplication.translate("DatasetManager", u"Export path:", None))
        self.exportOpenButton.setText(QCoreApplication.translate("DatasetManager", u"Open", None))
        self.importOpenButton.setText(QCoreApplication.translate("DatasetManager", u"Open", None))
    # retranslateUi

