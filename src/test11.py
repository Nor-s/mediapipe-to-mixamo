import sys
import cv2 as cv

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QBoxLayout, QLabel
from PyQt5 import QtGui
import numpy as np
import mss



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
from mss import mss
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
import copy

class Image_View(QThread):
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            widget = ex.geometry()
            l = widget.left()
            t = widget.top()
            w = widget.width()
            h = widget.height()
            with mss() as sct:
                print(l, t, w, h)
                image_pos1 = np.array(sct.grab({'left': l, 'top': t, 'width': w, 'height': h}))[:, :, :3]

            img = cv.cvtColor(image_pos1, cv.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
            # label.adjustSize()
            # ex.resize(pixmap.size())
            
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'My Screen'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480        
        self.initUI()
       
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, self)

        self.th = Image_View()
        form_lbx.addWidget(label)

        self.setLayout(form_lbx)

        self.th.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    label = QLabel()

    ex = App()
    ex.show()
    sys.exit(app.exec_())