# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt_gui/gui.xml'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 387)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 361, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(300, 300))
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(300, 200))
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.layoutWidget = QtWidgets.QWidget(self.tab2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 311, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lbl_display2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_display2.sizePolicy().hasHeightForWidth())
        self.lbl_display2.setSizePolicy(sizePolicy)
        self.lbl_display2.setObjectName("lbl_display2")
        self.gridLayout_3.addWidget(self.lbl_display2, 2, 0, 1, 1)
        self.cmb_gif = QtWidgets.QComboBox(self.layoutWidget)
        self.cmb_gif.setObjectName("cmb_gif")
        self.gridLayout_3.addWidget(self.cmb_gif, 3, 1, 1, 1)
        self.lbl_display = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_display.sizePolicy().hasHeightForWidth())
        self.lbl_display.setSizePolicy(sizePolicy)
        self.lbl_display.setObjectName("lbl_display")
        self.gridLayout_3.addWidget(self.lbl_display, 0, 0, 1, 1)
        self.btn_add_model = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_model.sizePolicy().hasHeightForWidth())
        self.btn_add_model.setSizePolicy(sizePolicy)
        self.btn_add_model.setObjectName("btn_add_model")
        self.gridLayout_3.addWidget(self.btn_add_model, 0, 1, 1, 1)
        self.cmb_model = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_model.sizePolicy().hasHeightForWidth())
        self.cmb_model.setSizePolicy(sizePolicy)
        self.cmb_model.setObjectName("cmb_model")
        self.gridLayout_3.addWidget(self.cmb_model, 1, 1, 1, 1)
        self.btn_add_gif = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_gif.sizePolicy().hasHeightForWidth())
        self.btn_add_gif.setSizePolicy(sizePolicy)
        self.btn_add_gif.setObjectName("btn_add_gif")
        self.gridLayout_3.addWidget(self.btn_add_gif, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab2, "Input")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 10, 311, 221))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_add_output = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_output.sizePolicy().hasHeightForWidth())
        self.btn_add_output.setSizePolicy(sizePolicy)
        self.btn_add_output.setObjectName("btn_add_output")
        self.gridLayout_4.addWidget(self.btn_add_output, 0, 1, 1, 1)
        self.cmb_output = QtWidgets.QComboBox(self.layoutWidget1)
        self.cmb_output.setObjectName("cmb_output")
        self.gridLayout_4.addWidget(self.cmb_output, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "Output")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 327, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_slider_min_visibility = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_slider_min_visibility.setObjectName("lbl_slider_min_visibility")
        self.gridLayout.addWidget(self.lbl_slider_min_visibility, 0, 2, 1, 1)
        self.h_slider_min_visibility = QtWidgets.QSlider(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.h_slider_min_visibility.sizePolicy().hasHeightForWidth())
        self.h_slider_min_visibility.setSizePolicy(sizePolicy)
        self.h_slider_min_visibility.setMaximum(99)
        self.h_slider_min_visibility.setSliderPosition(70)
        self.h_slider_min_visibility.setOrientation(QtCore.Qt.Horizontal)
        self.h_slider_min_visibility.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.h_slider_min_visibility.setTickInterval(10)
        self.h_slider_min_visibility.setObjectName("h_slider_min_visibility")
        self.gridLayout.addWidget(self.h_slider_min_visibility, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.chk_is_move = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.chk_is_move.setChecked(True)
        self.chk_is_move.setObjectName("chk_is_move")
        self.gridLayout.addWidget(self.chk_is_move, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lbl_slider_model_complexity = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_slider_model_complexity.setObjectName("lbl_slider_model_complexity")
        self.gridLayout.addWidget(self.lbl_slider_model_complexity, 2, 2, 1, 1)
        self.chk_is_show_result = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.chk_is_show_result.setChecked(True)
        self.chk_is_show_result.setObjectName("chk_is_show_result")
        self.gridLayout.addWidget(self.chk_is_show_result, 4, 1, 1, 1)
        self.h_slider_model_complexity = QtWidgets.QSlider(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.h_slider_model_complexity.sizePolicy().hasHeightForWidth())
        self.h_slider_model_complexity.setSizePolicy(sizePolicy)
        self.h_slider_model_complexity.setMaximum(2)
        self.h_slider_model_complexity.setSliderPosition(1)
        self.h_slider_model_complexity.setOrientation(QtCore.Qt.Horizontal)
        self.h_slider_model_complexity.setInvertedAppearance(False)
        self.h_slider_model_complexity.setInvertedControls(False)
        self.h_slider_model_complexity.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.h_slider_model_complexity.setTickInterval(1)
        self.h_slider_model_complexity.setObjectName("h_slider_model_complexity")
        self.gridLayout.addWidget(self.h_slider_model_complexity, 2, 1, 1, 1)
        self.lbl_slider_max_frame_num = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_slider_max_frame_num.setObjectName("lbl_slider_max_frame_num")
        self.gridLayout.addWidget(self.lbl_slider_max_frame_num, 3, 2, 1, 1)
        self.h_slider_max_frame_num = QtWidgets.QSlider(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.h_slider_max_frame_num.sizePolicy().hasHeightForWidth())
        self.h_slider_max_frame_num.setSizePolicy(sizePolicy)
        self.h_slider_max_frame_num.setMinimum(1)
        self.h_slider_max_frame_num.setMaximum(5000)
        self.h_slider_max_frame_num.setSliderPosition(5000)
        self.h_slider_max_frame_num.setOrientation(QtCore.Qt.Horizontal)
        self.h_slider_max_frame_num.setInvertedAppearance(False)
        self.h_slider_max_frame_num.setInvertedControls(False)
        self.h_slider_max_frame_num.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.h_slider_max_frame_num.setTickInterval(100)
        self.h_slider_max_frame_num.setObjectName("h_slider_max_frame_num")
        self.gridLayout.addWidget(self.h_slider_max_frame_num, 3, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.h_slider_min_detection_confidence = QtWidgets.QSlider(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.h_slider_min_detection_confidence.sizePolicy().hasHeightForWidth())
        self.h_slider_min_detection_confidence.setSizePolicy(sizePolicy)
        self.h_slider_min_detection_confidence.setSliderPosition(50)
        self.h_slider_min_detection_confidence.setOrientation(QtCore.Qt.Horizontal)
        self.h_slider_min_detection_confidence.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.h_slider_min_detection_confidence.setTickInterval(10)
        self.h_slider_min_detection_confidence.setObjectName("h_slider_min_detection_confidence")
        self.gridLayout.addWidget(self.h_slider_min_detection_confidence, 1, 1, 1, 1)
        self.lbl_slider_min_detection_confidence = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_slider_min_detection_confidence.setObjectName("lbl_slider_min_detection_confidence")
        self.gridLayout.addWidget(self.lbl_slider_min_detection_confidence, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, "Options")
        self.verticalLayout.addWidget(self.tabWidget)
        self.line1 = QtWidgets.QFrame(self.frame)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.verticalLayout.addWidget(self.line1)
        self.btn_convert = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_convert.sizePolicy().hasHeightForWidth())
        self.btn_convert.setSizePolicy(sizePolicy)
        self.btn_convert.setObjectName("btn_convert")
        self.verticalLayout.addWidget(self.btn_convert)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Mediapipe Pose"))
        self.lbl_display2.setText(_translate("Dialog", "Animation GIF"))
        self.lbl_display.setText(_translate("Dialog", "Model Json"))
        self.btn_add_model.setText(_translate("Dialog", "Add Model"))
        self.btn_add_gif.setText(_translate("Dialog", "Add Gif"))
        self.btn_add_output.setText(_translate("Dialog", "Add Output"))
        self.lbl_slider_min_visibility.setText(_translate("Dialog", "70"))
        self.label_3.setText(_translate("Dialog", "Maximum Frame"))
        self.label.setText(_translate("Dialog", "Model Complexity"))
        self.chk_is_move.setText(_translate("Dialog", "Move"))
        self.label_2.setText(_translate("Dialog", "Min Visibility"))
        self.lbl_slider_model_complexity.setText(_translate("Dialog", "1"))
        self.chk_is_show_result.setText(_translate("Dialog", "Show Result"))
        self.lbl_slider_max_frame_num.setText(_translate("Dialog", "5000"))
        self.label_4.setText(_translate("Dialog", "Min Detection"))
        self.label_5.setText(_translate("Dialog", "confidence"))
        self.lbl_slider_min_detection_confidence.setText(_translate("Dialog", "50"))
        self.btn_convert.setText(_translate("Dialog", "Convert"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
