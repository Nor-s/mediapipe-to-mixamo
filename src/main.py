# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# from multiprocessing import freeze_support
import json
from helper.mediapipe_to_mixamo import mediapipe_to_mixamo, MediapipeManager
from PyQt5.QtWidgets import QApplication, QMainWindow,  QFileDialog
import sys
from pyqt_gui.text_code1 import Ui_Dialog
import argparse
import os

# %%
class WindowClass(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP2MM")
        self.setupUi(self)
        self.statusBar().showMessage('Ready')

        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())
        self.is_converting = False

        self.btn_add_model.adjustSize()
        # 버튼에 기능을 연결하는 코드
        self.btn_add_model.clicked.connect(self.add_model_path)
        self.btn_add_gif.clicked.connect(self.add_gif_path)
        self.btn_add_output.clicked.connect(self.add_output_path)
        self.btn_convert.clicked.connect(self.convert)
        # self.cmb_gif.currentIndexChanged.connect(self.show_gif)
        self.h_slider_min_visibility.valueChanged.connect(
            self.set_lbl_min_visibility)
        self.h_slider_model_complexity.valueChanged.connect(
            self.set_lbl_model_complexity)
        self.h_slider_max_frame_num.valueChanged.connect(
            self.set_lbl_max_frame_num)
        self.h_slider_min_detection_confidence.valueChanged.connect(
            self.set_lbl_min_detection_confidence)
        self.mp_manager = MediapipeManager()

    def set_lbl_min_visibility(self):
        self.lbl_slider_min_visibility.setText(
            str(self.h_slider_min_visibility.value()))

    def set_lbl_model_complexity(self):
        self.lbl_slider_model_complexity.setText(
            str(self.h_slider_model_complexity.value()))

    def set_lbl_max_frame_num(self):
        self.lbl_slider_max_frame_num.setText(
            str(self.h_slider_max_frame_num.value()))

    def set_lbl_min_detection_confidence(self):
        self.lbl_slider_min_detection_confidence.setText(
            str(self.h_slider_min_detection_confidence.value()))



    def add_model_path(self):
        self.add_cmb_item_from_dialog(
            "Add Model Json File", "./", "Json (*.json)", self.cmb_model)

    def add_gif_path(self):
        self.add_cmb_item_from_dialog(
            "Add Animation GIF File", "./", "GIF (*.gif);; MP4 (*.mp4);; AVI (*.avi);; All files (*.*)", self.cmb_gif)

    def add_output_path(self):
        self.add_cmb_item_from_dialog(
            "Select Output File", "./", "Json (*.json)", self.cmb_output, is_save=True)
        
    def set_mp_manager(self):
            self.mp_manager.set_key(min_detection_confidence= self.h_slider_min_detection_confidence.value()/100.0,
                                    model_complexity= self.h_slider_model_complexity.value())

            self.mp_manager.min_visibility = self.h_slider_min_visibility.value()/100.0
            self.mp_manager.max_frame_num = self.h_slider_max_frame_num.value()
            self.mp_manager.is_hips_move = self.chk_is_move.isChecked()
            self.mp_manager.is_show_result = self.chk_is_show_result.isChecked()
    def convert(self):
        if self.is_converting:
            return
        self.statusBar().showMessage('Converting...')
        if self.cmb_model.currentIndex() == -1 or self.cmb_gif.currentIndex() == -1 or self.cmb_output.currentIndex() == -1:
            self.statusBar().showMessage('Please try again')
            return
        
        try:
            self.is_converting = True
            self.set_mp_manager()
            model_path = self.cmb_model.currentText()
            gif_path = self.cmb_gif.currentText()
            output_path = self.cmb_output.currentText()
            if gif_path == "youtube URL":
                gif_path = self.line_link.text()
            _, anim_json = mediapipe_to_mixamo(
                                self.mp_manager,
                                model_path, 
                                gif_path,) 
            if _ == False:
                self.statusBar().showMessage("mediapipe_to_mixamo: False")
                self.is_converting = False
                return

            with open(output_path, 'w') as f:
                json.dump(anim_json, f, indent=2)

            self.statusBar().showMessage('Success!')
            self.is_converting = False

        except Exception as e:
            self.statusBar().showMessage('Error! ' + str(e))
            self.is_converting = False
            return

    def add_cmb_item(self, item, cmb):
        cmb.addItem(item)
        cmb.setCurrentIndex(cmb.count() - 1)

    def add_cmb_item_from_dialog(self, title, path, filter, cmb, is_save=False):
        fname = self.show_dialog(title, path, filter, is_save)
        if fname != '':
            self.add_cmb_item(os.path.abspath(fname), cmb)

    # filter: "Images (*.png *.xpm .jpg);;Text files (.txt);;XML files (*.xml)"
    def show_dialog(self, title, path, filter, is_save=False):
        if not is_save:
            fname = QFileDialog.getOpenFileName(self, title, path, filter)
        else:
            fname = QFileDialog.getSaveFileName(self, title, path, filter)
        return fname[0]
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mediapipe To Mixamo')
    parser.add_argument(
        '--arg1', help='model binding pose json data (pixel3d: Export model)', default=None)
    parser.add_argument('--arg2', help='output path', default=None)

    args = parser.parse_args()
    model_path = args.arg1
    output_path = args.arg2

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    if(model_path != None):
        myWindow.add_cmb_item(os.path.abspath(model_path), myWindow.cmb_model)
    if(output_path != None):
        myWindow.add_cmb_item(os.path.abspath(output_path), myWindow.cmb_output)
    myWindow.add_cmb_item("youtube URL", myWindow.cmb_gif)
    myWindow.show()
    app.exec_()