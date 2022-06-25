import os
import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsPixmapItem, QGraphicsScene

import project_config as cf
from data.tool.anime import DrawOneFrame
from data.tool.bad_frame import badframe
from data.tool.detectron2_pic import detect_pic
from data.tool.hit import find_hit_by_ao
from data.tool.hit import findhit
from data.tool.hit import findevent
from data.tool.mydtw import drawforDTW
from data.tool.prepare_data import PATH_ex

# picture path
os.chdir(cf.PROJECT_ROOT + "data/gui")


# warp function
def funlist(*args):
    for fun in args:
        fun()


# generate by qt
class Ui_Widget(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.setWindowTitle('golf analysis')
        Widget.resize(1280, 720)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bilibili_33.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Widget.setWindowIcon(icon)
        Widget.setWindowIconText("golf analysis")
        self.gridLayout_2 = QtWidgets.QGridLayout(Widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_3 = QtWidgets.QPushButton(Widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_4.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_4.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(Widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_4.addWidget(self.pushButton_5, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 3, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(Widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(Widget)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 5, 1, 1)
        self.graphicsView_5 = QtWidgets.QGraphicsView(Widget)
        self.graphicsView_5.setObjectName("graphicsView_5")
        self.gridLayout_3.addWidget(self.graphicsView_5, 3, 2, 1, 4)
        self.label_5 = QtWidgets.QLabel(Widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 6, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(Widget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_3.addWidget(self.graphicsView, 1, 2, 2, 4)
        self.lineEdit_3 = QtWidgets.QLineEdit(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 0, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(Widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(Widget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 10, 1, 1)
        self.label_8 = QtWidgets.QLabel(Widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 8, 1, 1)
        self.label_4 = QtWidgets.QLabel(Widget)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 3, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_3.addWidget(self.lineEdit_4, 0, 9, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_3.addWidget(self.lineEdit_5, 0, 11, 1, 1)
        self.graphicsView_2 = QtWidgets.QGraphicsView(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_2.setSizePolicy(sizePolicy)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout_3.addWidget(self.graphicsView_2, 1, 6, 1, 3)
        self.graphicsView_3 = QtWidgets.QGraphicsView(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_3.sizePolicy().hasHeightForWidth())
        self.graphicsView_3.setSizePolicy(sizePolicy)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout_3.addWidget(self.graphicsView_3, 1, 9, 1, 3)
        self.graphicsView_4 = QtWidgets.QGraphicsView(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_4.sizePolicy().hasHeightForWidth())
        self.graphicsView_4.setSizePolicy(sizePolicy)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout_3.addWidget(self.graphicsView_4, 2, 6, 2, 6)
        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "golf swing visualizer"))
        Widget.setWindowIconText(_translate("golf analysis", "golf analysis"))
        self.pushButton.setText(_translate("Widget", "choose"))
        self.pushButton_2.setText(_translate("Widget", "choose"))
        self.label.setText(_translate("Widget", "std(red)"))
        self.label_2.setText(_translate("Widget", "test(blue)"))
        self.pushButton_3.setText(_translate("Widget", "run"))
        self.pushButton_4.setText(_translate("Widget", "display"))
        self.pushButton_5.setText(_translate("Widget", "rotate"))
        self.label_6.setText(_translate("Widget", "Euclidean distance"))
        self.label_5.setText(_translate("Widget", "Customised display frame"))
        self.label_3.setText(_translate("Widget", "max diff frame"))
        self.label_9.setText(_translate("Widget", "Horizontal angle"))
        self.label_8.setText(_translate("Widget", "Vertical angle"))


class MainWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.dpi = 200
        self.max = None
        self.ans = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(lambda: funlist(self.dispic, self.show_frame, self.setdtw))
        self.ui.pushButton_4.clicked.connect(self.show_frame)
        self.ui.pushButton_5.clicked.connect(lambda x: self.show_frame(isupdate=True))
        self.ui.pushButton_2.clicked.connect(lambda x: self.msg(self.ui.lineEdit_2))
        self.ui.pushButton.clicked.connect(lambda y: self.msg(self.ui.lineEdit))

    def msg(self, object):
        directory = QtWidgets.QFileDialog.getOpenFileName(None, "choose file", f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/')
        object.setText(directory[0])

    def read_path(self):
        pa = self.ui.lineEdit.text()
        pb = self.ui.lineEdit_2.text()
        if pa != "" and pb != "":
            return [pa, pb]
        else:
            return [None, None]

    def dispic(self):
        [pa, pb] = self.read_path()
        if pa and pb is not None:
            # try:
            self.ans = badframe(pa, pb, hit_method=cf.the_hit_method_for_gui)
            pic = self.ans[0]
            self.max = self.ans[1][0]['index_id']
            self.ui.label_4.setText(str(self.max))
            # except:
            #     print("path error")
            #     self.max = None
            #     return
            try:
                pic.savefig('data.png', dpi=self.dpi)
                # print(self.frameGeometry().width())
                pic.close()
                self.setimg('data.png', self.ui.graphicsView)
            except:
                print("Handling errors")

        else:
            try:
                self.max = None
                self.ui.graphicsView.scene().clear()
            except:
                pass

    def show_frame(self, isupdate=False):
        try:
            custom_frame = int(self.ui.lineEdit_3.text())
        except:
            custom_frame = None

        try:
            angel_a = int(self.ui.lineEdit_4.text())
            angel_b = int(self.ui.lineEdit_5.text())
        except:
            angel_a = 0
            angel_b = 90

        try:
            if custom_frame is None:
                custom_frame = self.max
            if custom_frame is not None:
                # print(custom_frame)
                DrawOneFrame(self.ans[2][1][self.ans[2][0].index1[custom_frame]],
                             self.ans[2][2][self.ans[2][0].index2[custom_frame]], save_path='', id='frame',
                             dpi=self.dpi, elev=angel_a, azim=angel_b)
                try:
                    self.setimg('frame.png', self.ui.graphicsView_4, use_scale=False)
                except:
                    print("3D pic error", file=sys.stderr)
            else:
                try:
                    self.ui.label_4.clear()
                    self.ui.graphicsView_4.scene().clear()
                except:
                    pass
        except:
            print("index error", file=sys.stderr)

        try:
            if custom_frame is not None and self.ui.lineEdit.text() is not None and self.ui.lineEdit_2.text() is not None and isupdate is False:
                try:
                    self.ffmpeg_frame_png(custom_frame, self.ui.lineEdit.text(), self.ui.lineEdit_2.text(),
                                          hit_method=cf.the_hit_method_for_gui)
                    if cf.gui_show_skeleton:
                        detect_pic('a.png')
                        detect_pic('b.png')
                except:
                    print("Image processing errors")

                self.setimg('a.png', self.ui.graphicsView_2)
                self.setimg('b.png', self.ui.graphicsView_3)
        except:
            pass

    def ffmpeg_frame_png(self, frame, path_a, path_b, hit_method=0):
        index1 = self.ans[2][0].index1
        index2 = self.ans[2][0].index2
        ia_after_hit = index1[frame]
        ib_after_hit = index2[frame]
        data_one = np.load(path_a)
        data_two = np.load(path_b)

        pva = PATH_ex(path_a)
        pvb = PATH_ex(path_b)

        if hit_method == 0:
            hita = findhit(data_one)
            hitb = findhit(data_two)
        elif hit_method == 1:
            # golfdb
            hita = findevent(pva)
            hitb = findevent(pvb)
        elif hit_method == 2:
            csv_p = f'{cf.PROJECT_ROOT}data/tag/tag.csv'
            hita = find_hit_by_ao(csv_p, path_a)[:2]
            hitb = find_hit_by_ao(csv_p, path_b)[:2]
        else:
            raise RuntimeError("hit_method setting error")

        ia = ia_after_hit + hita[0]
        ib = ib_after_hit + hitb[0]


        try:
            cmd_sa = f'ffmpeg -i {pva} -vf "select=eq(n\,{ia})" -vframes 1 a.png -y'
            cmd_sb = f'ffmpeg -i {pvb} -vf "select=eq(n\,{ib})" -vframes 1 b.png -y'
            os.system(cmd_sa)
            os.system(cmd_sb)
        except:
            print("Video frames out of specified range")
            print(hita, hitb)

    def setimg(self, path, object, use_scale=True):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        frame = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.ui.item = QGraphicsPixmapItem(pix)
        self.ui.item.setTransformationMode(Qt.SmoothTransformation)
        if use_scale:
            self.ui.item.setScale(min(object.height() / pix.height(), object.width() / pix.width()))
        else:
            self.ui.item.setScale(min(object.height() / pix.height(), object.width() / pix.width()) * 1.5)
        self.ui.scene = QGraphicsScene()
        self.ui.scene.addItem(self.ui.item)
        object.setScene(self.ui.scene)

    def setdtw(self):
        if self.ans is not None:
            try:
                dtw_ans = drawforDTW(self.ans[2][1], self.ans[2][2], if_save=True,
                                     dpi=self.dpi)  # res4
                # dtw_ans = drawforDTW(self.ans[2][1], self.ans[2][2], if_save=True, dpi=self.dpi)  # res4
                self.setimg('dtw.png', self.ui.graphicsView_5)
                self.ui.label_7.setText(str(dtw_ans))
            except:
                print("dtw error")
        else:
            try:
                self.ui.label_7.clear()
                self.ui.graphicsView_5.scene().clear()
            except:
                pass


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("bilibili_33.ico"), QtGui.QIcon.Active, QtGui.QIcon.On)
    widget.show()
    sys.exit(app.exec_())
