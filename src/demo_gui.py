# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from pyqt_gui.text_code1 import Ui_Dialog
from multiprocessing import freeze_support
import json
from helper import pyglm_helper as glmh
from helper import mixamo_helper as mmh
from helper import mediapipe_helper as mph
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow,  QFileDialog
import sys
from PIL import Image


def smooth_gif_resize(gif, frameWidth, frameHeight):
    gif = Image.open(gif)
    gifWidth0, gifHeight0 = gif.size

    widthRatio = frameWidth / gifWidth0
    heightRatio = frameHeight / gifHeight0

    if widthRatio >= heightRatio:
        gifWidth1 = gifWidth0 * heightRatio
        gifHeight1 = frameHeight
        return gifWidth1, gifHeight1

    gifWidth1 = frameWidth
    gifHeight1 = gifHeight0 * widthRatio
    return round(gifWidth1), round(gifHeight1)


# %%


class WindowClass(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar().showMessage('Ready')

        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        self.btn_add_model.adjustSize()
        # 버튼에 기능을 연결하는 코드
        self.btn_add_model.clicked.connect(self.add_model_path)
        self.btn_add_gif.clicked.connect(self.add_gif_path)
        self.btn_add_output.clicked.connect(self.add_output_path)
        self.btn_convert.clicked.connect(self.convert)
        self.cmb_gif.currentIndexChanged.connect(self.show_gif)
        self.h_slider_min_visibility.valueChanged.connect(
            self.set_lbl_min_visibility)
        self.h_slider_model_complexity.valueChanged.connect(
            self.set_lbl_model_complexity)
        self.h_slider_max_frame_num.valueChanged.connect(
            self.set_lbl_max_frame_num)

    def set_lbl_min_visibility(self):
        self.lbl_slider_min_visibility.setText(
            str(self.h_slider_min_visibility.value()))

    def set_lbl_model_complexity(self):
        self.lbl_slider_model_complexity.setText(
            str(self.h_slider_model_complexity.value()))

    def set_lbl_max_frame_num(self):
        self.lbl_slider_max_frame_num.setText(
            str(self.h_slider_max_frame_num.value()))

    def add_model_path(self):
        self.add_cmb_item_from_dialog(
            "Add Model Json File", "./", "Json (*.json)", self.cmb_model)

    def add_gif_path(self):
        self.add_cmb_item_from_dialog(
            "Add Animation GIF File", "./", "GIF (*.gif)", self.cmb_gif)

    def add_output_path(self):
        self.add_cmb_item_from_dialog(
            "Select Output File", "./", "Json (*.json)", self.cmb_output, is_save=True)

    def convert(self):
        self.statusBar().showMessage('Converting...')
        if self.cmb_model.currentIndex() == -1 or self.cmb_gif.currentIndex() == -1 or self.cmb_output.currentIndex() == -1:
            self.statusBar().showMessage('Please try again')
            return
        try:
            model_path = self.cmb_model.currentText()
            gif_path = self.cmb_gif.currentText()
            output_path = self.cmb_output.currentText()
            max_frame_num = self.h_slider_max_frame_num.value()
            model_complexity = self.h_slider_model_complexity.value()
            min_visibility = self.h_slider_min_visibility.value()/100.0
            max_frame_num = self.h_slider_max_frame_num.value()
            is_move_hips = self.chk_is_move.isChecked()
            mediapipe_json_object = mph.gif_to_mediapipe_json(
                fileName=gif_path, maxFrameNum=max_frame_num, modelComplexity=model_complexity)
            mixamo_json_object = mmh.mediapipeToMixamo(
                mph.get_name_idx_map(), mediapipe_json_object)
            anim_json = glmh.get_anim_json3(
                mixamo_json_object, model_path, is_hips_move=is_move_hips, min_visibility=min_visibility)
            with open(output_path, 'w') as f:
                json.dump(anim_json, f, indent=2)
            self.statusBar().showMessage('Success!')
        except Exception as e:
            print(e)
            self.statusBar().showMessage('Error! ' + str(e))
            return

    def add_cmb_item_from_dialog(self, title, path, filter, cmb, is_save=False):
        fname = self.show_dialog(title, path, filter, is_save)
        if fname != '':
            cmb.addItem(fname)
            cmb.setCurrentIndex(cmb.count() - 1)

    # filter: "Images (*.png *.xpm .jpg);;Text files (.txt);;XML files (*.xml)"
    def show_dialog(self, title, path, filter, is_save=False):
        if not is_save:
            fname = QFileDialog.getOpenFileName(self, title, path, filter)
        else:
            fname = QFileDialog.getSaveFileName(self, title, path, filter)
        return fname[0]

    def show_gif(self):
        if self.cmb_gif.currentIndex() != -1:
            movie = QMovie(self.cmb_gif.currentText())

            gif_size = QSize(
                *smooth_gif_resize(self.cmb_gif.currentText(), 150, 150))
            movie.setScaledSize(gif_size)
            self.lbl_gif_movie.setMovie(movie)
            self.lbl_gif_movie.adjustSize()
            movie.start()


if __name__ == '__main__':
    freeze_support()

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
