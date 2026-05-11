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
        self.trainingWidget = QWidget(DataTrainerWidget)
        self.trainingWidget.setObjectName(u"trainingWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trainingWidget.sizePolicy().hasHeightForWidth())
        self.trainingWidget.setSizePolicy(sizePolicy)
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


        self.gridLayout_2.addWidget(self.trainingWidget, 4, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 3, 0, 1, 1)

        self.validateTrainWidget = QWidget(DataTrainerWidget)
        self.validateTrainWidget.setObjectName(u"validateTrainWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.validateTrainWidget.sizePolicy().hasHeightForWidth())
        self.validateTrainWidget.setSizePolicy(sizePolicy1)
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

        self.exitTrainingButton = QPushButton(self.validateTrainWidget)
        self.exitTrainingButton.setObjectName(u"exitTrainingButton")
        self.exitTrainingButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.exitTrainingButton)


        self.gridLayout_2.addWidget(self.validateTrainWidget, 2, 0, 1, 1)

        self.modelSettingsWidget = QWidget(DataTrainerWidget)
        self.modelSettingsWidget.setObjectName(u"modelSettingsWidget")
        self.gridLayout_3 = QGridLayout(self.modelSettingsWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.onnxExportCheckBox = QCheckBox(self.modelSettingsWidget)
        self.onnxExportCheckBox.setObjectName(u"onnxExportCheckBox")

        self.gridLayout_3.addWidget(self.onnxExportCheckBox, 12, 0, 1, 1)

        self.modelSelectorComboBox = QComboBox(self.modelSettingsWidget)
        self.modelSelectorComboBox.setObjectName(u"modelSelectorComboBox")
        sizePolicy1.setHeightForWidth(self.modelSelectorComboBox.sizePolicy().hasHeightForWidth())
        self.modelSelectorComboBox.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.modelSelectorComboBox, 0, 2, 1, 2)

        self.customModelWidget = QWidget(self.modelSettingsWidget)
        self.customModelWidget.setObjectName(u"customModelWidget")
        self.gridLayout_4 = QGridLayout(self.customModelWidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.customModelPathLineEdit = QLineEdit(self.customModelWidget)
        self.customModelPathLineEdit.setObjectName(u"customModelPathLineEdit")

        self.gridLayout_4.addWidget(self.customModelPathLineEdit, 0, 0, 1, 1)

        self.customModelOpenButton = QPushButton(self.customModelWidget)
        self.customModelOpenButton.setObjectName(u"customModelOpenButton")

        self.gridLayout_4.addWidget(self.customModelOpenButton, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.customModelWidget, 1, 0, 1, 4)

        self.epochsSpinBox = QSpinBox(self.modelSettingsWidget)
        self.epochsSpinBox.setObjectName(u"epochsSpinBox")
        self.epochsSpinBox.setMaximum(9999999)

        self.gridLayout_3.addWidget(self.epochsSpinBox, 4, 2, 1, 2)

        self.modelSelectLabel = QLabel(self.modelSettingsWidget)
        self.modelSelectLabel.setObjectName(u"modelSelectLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modelSelectLabel.sizePolicy().hasHeightForWidth())
        self.modelSelectLabel.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.modelSelectLabel, 0, 0, 1, 1)

        self.batchSpinBox = QSpinBox(self.modelSettingsWidget)
        self.batchSpinBox.setObjectName(u"batchSpinBox")
        self.batchSpinBox.setMinimum(-1)
        self.batchSpinBox.setMaximum(9999999)

        self.gridLayout_3.addWidget(self.batchSpinBox, 5, 2, 1, 2)

        self.workersLabel = QLabel(self.modelSettingsWidget)
        self.workersLabel.setObjectName(u"workersLabel")

        self.gridLayout_3.addWidget(self.workersLabel, 3, 0, 1, 1)

        self.modelOutputPathLineEdit = QLineEdit(self.modelSettingsWidget)
        self.modelOutputPathLineEdit.setObjectName(u"modelOutputPathLineEdit")

        self.gridLayout_3.addWidget(self.modelOutputPathLineEdit, 10, 2, 1, 1)

        self.epochsLabel = QLabel(self.modelSettingsWidget)
        self.epochsLabel.setObjectName(u"epochsLabel")

        self.gridLayout_3.addWidget(self.epochsLabel, 4, 0, 1, 1)

        self.batchSizeLabel = QLabel(self.modelSettingsWidget)
        self.batchSizeLabel.setObjectName(u"batchSizeLabel")

        self.gridLayout_3.addWidget(self.batchSizeLabel, 5, 0, 1, 1)

        self.datasetPathLabel = QLabel(self.modelSettingsWidget)
        self.datasetPathLabel.setObjectName(u"datasetPathLabel")

        self.gridLayout_3.addWidget(self.datasetPathLabel, 15, 0, 1, 1)

        self.widget_2 = QWidget(self.modelSettingsWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.usePathsLabel = QLabel(self.widget_2)
        self.usePathsLabel.setObjectName(u"usePathsLabel")
        self.usePathsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.usePathsLabel)

        self.datasetPathComboBox = QComboBox(self.widget_2)
        self.datasetPathComboBox.setObjectName(u"datasetPathComboBox")

        self.horizontalLayout_2.addWidget(self.datasetPathComboBox)


        self.gridLayout_3.addWidget(self.widget_2, 14, 1, 1, 3)

        self.modelRootLabel = QLabel(self.modelSettingsWidget)
        self.modelRootLabel.setObjectName(u"modelRootLabel")

        self.gridLayout_3.addWidget(self.modelRootLabel, 10, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 0, 1, 4)

        self.generateOutputDirectoryButton = QPushButton(self.modelSettingsWidget)
        self.generateOutputDirectoryButton.setObjectName(u"generateOutputDirectoryButton")

        self.gridLayout_3.addWidget(self.generateOutputDirectoryButton, 10, 3, 1, 1)

        self.datasetPathLineEdit = QLineEdit(self.modelSettingsWidget)
        self.datasetPathLineEdit.setObjectName(u"datasetPathLineEdit")

        self.gridLayout_3.addWidget(self.datasetPathLineEdit, 16, 0, 1, 4)

        self.modelNameLabel = QLabel(self.modelSettingsWidget)
        self.modelNameLabel.setObjectName(u"modelNameLabel")

        self.gridLayout_3.addWidget(self.modelNameLabel, 11, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 13, 0, 1, 4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 9, 0, 1, 4)

        self.generateNameButton = QPushButton(self.modelSettingsWidget)
        self.generateNameButton.setObjectName(u"generateNameButton")

        self.gridLayout_3.addWidget(self.generateNameButton, 11, 3, 1, 1)

        self.modelNameLineEdit = QLineEdit(self.modelSettingsWidget)
        self.modelNameLineEdit.setObjectName(u"modelNameLineEdit")

        self.gridLayout_3.addWidget(self.modelNameLineEdit, 11, 2, 1, 1)

        self.workersSpinBox = QSpinBox(self.modelSettingsWidget)
        self.workersSpinBox.setObjectName(u"workersSpinBox")
        self.workersSpinBox.setMaximum(9999999)

        self.gridLayout_3.addWidget(self.workersSpinBox, 3, 2, 1, 2)

        self.patienceSpinBox = QSpinBox(self.modelSettingsWidget)
        self.patienceSpinBox.setObjectName(u"patienceSpinBox")
        self.patienceSpinBox.setMaximum(9999999)

        self.gridLayout_3.addWidget(self.patienceSpinBox, 6, 2, 1, 2)

        self.patienceLabel = QLabel(self.modelSettingsWidget)
        self.patienceLabel.setObjectName(u"patienceLabel")

        self.gridLayout_3.addWidget(self.patienceLabel, 6, 0, 1, 1)


        self.gridLayout_2.addWidget(self.modelSettingsWidget, 0, 0, 1, 1)


        self.retranslateUi(DataTrainerWidget)

        QMetaObject.connectSlotsByName(DataTrainerWidget)
    # setupUi

    def retranslateUi(self, DataTrainerWidget):
        DataTrainerWidget.setWindowTitle(QCoreApplication.translate("DataTrainerWidget", u"Form", None))
        self.outputLogLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Output log:", None))
        self.trainingLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Training progress", None))
        self.validateButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Validate Dataset", None))
        self.startTrainingButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Start training", None))
        self.exitTrainingButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Exit training", None))
        self.onnxExportCheckBox.setText(QCoreApplication.translate("DataTrainerWidget", u"Export into ONNX format", None))
        self.customModelOpenButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Open", None))
        self.modelSelectLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Select pretrained model:", None))
        self.workersLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Number of additional workers:", None))
        self.epochsLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Number of epochs:", None))
        self.batchSizeLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Batch size:", None))
        self.datasetPathLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Dataset path:", None))
        self.usePathsLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Use import/export from Dataset", None))
        self.modelRootLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Model output root directory:", None))
        self.generateOutputDirectoryButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Auto Generate", None))
        self.modelNameLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Model output name:", None))
        self.generateNameButton.setText(QCoreApplication.translate("DataTrainerWidget", u"Auto Generate", None))
        self.patienceLabel.setText(QCoreApplication.translate("DataTrainerWidget", u"Patience:", None))
    # retranslateUi

