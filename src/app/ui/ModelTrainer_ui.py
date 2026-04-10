# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModelTrainer.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTextEdit, QWidget)

class Ui_DataTrainerWidget(object):
    def setupUi(self, DataTrainerWidget):
        if not DataTrainerWidget.objectName():
            DataTrainerWidget.setObjectName(u"DataTrainerWidget")
        DataTrainerWidget.resize(1051, 701)
        self.gridLayout_2 = QGridLayout(DataTrainerWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.validateTrainWidget = QWidget(DataTrainerWidget)
        self.validateTrainWidget.setObjectName(u"validateTrainWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.validateTrainWidget.sizePolicy().hasHeightForWidth())
        self.validateTrainWidget.setSizePolicy(sizePolicy)
        self.validateTrainWidget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.validateTrainWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.validateButton = QPushButton(self.validateTrainWidget)
        self.validateButton.setObjectName(u"validateButton")

        self.horizontalLayout.addWidget(self.validateButton)

        self.startTrainingButton = QPushButton(self.validateTrainWidget)
        self.startTrainingButton.setObjectName(u"startTrainingButton")
        self.startTrainingButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.startTrainingButton)


        self.gridLayout_2.addWidget(self.validateTrainWidget, 1, 0, 1, 1)

        self.trainingWidget = QWidget(DataTrainerWidget)
        self.trainingWidget.setObjectName(u"trainingWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.trainingWidget.sizePolicy().hasHeightForWidth())
        self.trainingWidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.trainingWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.outputLogLabel = QLabel(self.trainingWidget)
        self.outputLogLabel.setObjectName(u"outputLogLabel")

        self.gridLayout.addWidget(self.outputLogLabel, 1, 0, 1, 1)

        self.trainingLabel = QLabel(self.trainingWidget)
        self.trainingLabel.setObjectName(u"trainingLabel")

        self.gridLayout.addWidget(self.trainingLabel, 3, 0, 1, 1)

        self.trainingProgressBar = QProgressBar(self.trainingWidget)
        self.trainingProgressBar.setObjectName(u"trainingProgressBar")
        self.trainingProgressBar.setValue(0)

        self.gridLayout.addWidget(self.trainingProgressBar, 3, 1, 1, 1)

        self.logOutputTextEdit = QTextEdit(self.trainingWidget)
        self.logOutputTextEdit.setObjectName(u"logOutputTextEdit")

        self.gridLayout.addWidget(self.logOutputTextEdit, 2, 0, 1, 2)


        self.gridLayout_2.addWidget(self.trainingWidget, 3, 0, 1, 1)

        self.modelSettingsWidget = QGridLayout()
        self.modelSettingsWidget.setObjectName(u"modelSettingsWidget")
        self.workersLabel = QLabel(DataTrainerWidget)
        self.workersLabel.setObjectName(u"workersLabel")

        self.modelSettingsWidget.addWidget(self.workersLabel, 3, 0, 1, 1)

        self.workersSpinBox = QSpinBox(DataTrainerWidget)
        self.workersSpinBox.setObjectName(u"workersSpinBox")

        self.modelSettingsWidget.addWidget(self.workersSpinBox, 3, 1, 1, 2)

        self.batchInfoButton = QPushButton(DataTrainerWidget)
        self.batchInfoButton.setObjectName(u"batchInfoButton")

        self.modelSettingsWidget.addWidget(self.batchInfoButton, 5, 3, 1, 1)

        self.epochsSpinBox = QSpinBox(DataTrainerWidget)
        self.epochsSpinBox.setObjectName(u"epochsSpinBox")

        self.modelSettingsWidget.addWidget(self.epochsSpinBox, 4, 1, 1, 2)

        self.modelNameLabel = QLabel(DataTrainerWidget)
        self.modelNameLabel.setObjectName(u"modelNameLabel")

        self.modelSettingsWidget.addWidget(self.modelNameLabel, 9, 0, 1, 1)

        self.generateNameButton = QPushButton(DataTrainerWidget)
        self.generateNameButton.setObjectName(u"generateNameButton")

        self.modelSettingsWidget.addWidget(self.generateNameButton, 9, 3, 1, 1)

        self.workersInfoButton = QPushButton(DataTrainerWidget)
        self.workersInfoButton.setObjectName(u"workersInfoButton")

        self.modelSettingsWidget.addWidget(self.workersInfoButton, 3, 3, 1, 1)

        self.batchSpinBox = QSpinBox(DataTrainerWidget)
        self.batchSpinBox.setObjectName(u"batchSpinBox")

        self.modelSettingsWidget.addWidget(self.batchSpinBox, 5, 1, 1, 2)

        self.batchSizeLabel = QLabel(DataTrainerWidget)
        self.batchSizeLabel.setObjectName(u"batchSizeLabel")

        self.modelSettingsWidget.addWidget(self.batchSizeLabel, 5, 0, 1, 1)

        self.modelNameLineEdit = QLineEdit(DataTrainerWidget)
        self.modelNameLineEdit.setObjectName(u"modelNameLineEdit")

        self.modelSettingsWidget.addWidget(self.modelNameLineEdit, 9, 1, 1, 2)

        self.generateOutputDirectoryButton = QPushButton(DataTrainerWidget)
        self.generateOutputDirectoryButton.setObjectName(u"generateOutputDirectoryButton")

        self.modelSettingsWidget.addWidget(self.generateOutputDirectoryButton, 8, 3, 1, 1)

        self.modelSelectionLayout = QHBoxLayout()
        self.modelSelectionLayout.setObjectName(u"modelSelectionLayout")
        self.modelSelectLabel = QLabel(DataTrainerWidget)
        self.modelSelectLabel.setObjectName(u"modelSelectLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modelSelectLabel.sizePolicy().hasHeightForWidth())
        self.modelSelectLabel.setSizePolicy(sizePolicy2)

        self.modelSelectionLayout.addWidget(self.modelSelectLabel)

        self.modelSelectorComboBox = QComboBox(DataTrainerWidget)
        self.modelSelectorComboBox.setObjectName(u"modelSelectorComboBox")
        sizePolicy.setHeightForWidth(self.modelSelectorComboBox.sizePolicy().hasHeightForWidth())
        self.modelSelectorComboBox.setSizePolicy(sizePolicy)

        self.modelSelectionLayout.addWidget(self.modelSelectorComboBox)


        self.modelSettingsWidget.addLayout(self.modelSelectionLayout, 1, 0, 1, 4)

        self.modelRootLabel = QLabel(DataTrainerWidget)
        self.modelRootLabel.setObjectName(u"modelRootLabel")

        self.modelSettingsWidget.addWidget(self.modelRootLabel, 8, 0, 1, 1)

        self.datasetLayout = QHBoxLayout()
        self.datasetLayout.setObjectName(u"datasetLayout")
        self.datasetPathLabel = QLabel(DataTrainerWidget)
        self.datasetPathLabel.setObjectName(u"datasetPathLabel")

        self.datasetLayout.addWidget(self.datasetPathLabel)

        self.usePathsLabel = QLabel(DataTrainerWidget)
        self.usePathsLabel.setObjectName(u"usePathsLabel")
        self.usePathsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.datasetLayout.addWidget(self.usePathsLabel)

        self.datasetPathComboBox = QComboBox(DataTrainerWidget)
        self.datasetPathComboBox.setObjectName(u"datasetPathComboBox")

        self.datasetLayout.addWidget(self.datasetPathComboBox)


        self.modelSettingsWidget.addLayout(self.datasetLayout, 12, 0, 1, 4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.modelSettingsWidget.addItem(self.horizontalSpacer_3, 11, 0, 1, 4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.modelSettingsWidget.addItem(self.horizontalSpacer_2, 7, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.modelSettingsWidget.addItem(self.horizontalSpacer, 2, 0, 1, 4)

        self.epochsLabel = QLabel(DataTrainerWidget)
        self.epochsLabel.setObjectName(u"epochsLabel")

        self.modelSettingsWidget.addWidget(self.epochsLabel, 4, 0, 1, 1)

        self.epochsInfoButton = QPushButton(DataTrainerWidget)
        self.epochsInfoButton.setObjectName(u"epochsInfoButton")

        self.modelSettingsWidget.addWidget(self.epochsInfoButton, 4, 3, 1, 1)

        self.datasetPathLineEdit = QLineEdit(DataTrainerWidget)
        self.datasetPathLineEdit.setObjectName(u"datasetPathLineEdit")

        self.modelSettingsWidget.addWidget(self.datasetPathLineEdit, 15, 0, 1, 4)

        self.modelOutputPathLineEdit = QLineEdit(DataTrainerWidget)
        self.modelOutputPathLineEdit.setObjectName(u"modelOutputPathLineEdit")

        self.modelSettingsWidget.addWidget(self.modelOutputPathLineEdit, 8, 1, 1, 2)

        self.onnxExportCheckBox = QCheckBox(DataTrainerWidget)
        self.onnxExportCheckBox.setObjectName(u"onnxExportCheckBox")

        self.modelSettingsWidget.addWidget(self.onnxExportCheckBox, 10, 0, 1, 1)

        self.modelSettingsWidget.setColumnStretch(1, 1)

        self.gridLayout_2.addLayout(self.modelSettingsWidget, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 0, 1, 1)


        self.retranslateUi(DataTrainerWidget)

        QMetaObject.connectSlotsByName(DataTrainerWidget)
    # setupUi

    def retranslateUi(self, DataTrainerWidget):
        DataTrainerWidget.setWindowTitle(QCoreApplication.translate("DataTrainerWidget", u"Form", None))
        self.validateButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Validate Dataset", None))
        self.startTrainingButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Start training", None))
        self.outputLogLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Output log:", None))
        self.trainingLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Training progress", None))
        self.workersLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Number of additional workers:", None))
        self.batchInfoButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Info", None))
        self.modelNameLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Model output name:", None))
        self.generateNameButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Auto Generate", None))
        self.workersInfoButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Info", None))
        self.batchSizeLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Batch size:", None))
        self.generateOutputDirectoryButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Auto Generate", None))
        self.modelSelectLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Select pretrained model:", None))
        self.modelRootLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Model output root directory:", None))
        self.datasetPathLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Dataset path:", None))
        self.usePathsLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Use import/export from Dataset", None))
        self.epochsLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Number of epochs:", None))
        self.epochsInfoButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Info", None))
        self.onnxExportCheckBox.setText(QCoreApplication.translate("DataTrainerWidget", u"Export into ONNX format", None))
    # retranslateUi

