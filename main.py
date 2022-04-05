import sys
import os
import send2trash
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.my_layout = QGridLayout(widget)
        self.setCentralWidget(widget)
        self.setLayout(self.my_layout)
        self.img_index = 0
        self.lbl_img = QLabel(self)
        self.img_list = ['']
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)
        file_name = ''
        pixmap = QPixmap(file_name)
        self.lbl_img.setPixmap(pixmap)
        self.setMenu()
        self.setButton()
        self.setWindowTitle('Dataset Filter')
        self.my_layout.addWidget(self.lbl_img, 1, 1)
        self.show()

    def setButton(self):
        prev_btn = QPushButton('Prev', self)
        prev_btn.resize(prev_btn.sizeHint())
        prev_btn.clicked.connect(self.btnPrev_clicked)
        self.my_layout.addWidget(prev_btn, 2, 0)

        del_btn = QPushButton('Del', self)
        del_btn.resize(del_btn.sizeHint())
        del_btn.clicked.connect(self.btnDel_clicked)
        self.my_layout.addWidget(del_btn, 2, 1)

        next_btn = QPushButton('Next', self)
        next_btn.resize(next_btn.sizeHint())
        next_btn.clicked.connect(self.btnNext_clicked)
        self.my_layout.addWidget(next_btn, 2, 2)

    def setMenu(self):
        menubar = self.menuBar()
        selectFolder = QAction('File', self)
        selectFolder.triggered.connect(self.getFileList)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(selectFolder)
        filemenu.addAction(exitAction)
        # self.my_layout.addWidget(filemenu, 0, 0)

    def getFileList(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Directory")
        file_list = os.listdir(fname)
        file_list_jpg = [os.path.join(fname, file) for file in file_list if
                         file.endswith(".jpg") or file.endswith(".png")]
        print(file_list_jpg)
        self.img_list = file_list_jpg
        pixmap = QPixmap(self.img_list[0])
        pixmap.scaledToWidth(800)
        pixmap.scaledToHeight(800)
        self.lbl_img.setPixmap(pixmap)
        self.repaint()

    def btnNext_clicked(self):
        self.img_index += 1
        pixmap = QPixmap(self.img_list[self.img_index])
        self.lbl_img.setPixmap(pixmap)
        self.repaint()

    def btnDel_clicked(self):
        head, tail = self.img_list[self.img_index].rsplit("\\", 1)
        label_dir = os.path.join(head, "label")
        img_dir = os.path.join(head, "image")
        label_file, _ = tail.split(".")
        label_file = label_file + ".txt"
        label_file = os.path.join(label_dir, label_file)
        img_file, kind = tail.split(".")
        if kind == "jpg":
            img_file = img_file + ".jpg"
        elif kind == "png":
            img_file = img_file + ".png"
        else:
            print("지정하지 않은 포멧")

        img_file = os.path.join(img_dir, img_file)
        pixmap = QPixmap(self.img_list[self.img_index + 1])
        self.lbl_img.setPixmap(pixmap)
        print("레이블링 이미지 파일:", self.img_list[self.img_index])

        os.remove(self.img_list.pop(self.img_index))
        print("레이블링 이미지 제거 성공")
        os.remove(label_file)
        print("레이블 제거 성공")
        os.remove(img_file)
        print("이미지 제거 성공")

    def btnPrev_clicked(self):
        self.img_index -= 1
        pixmap = QPixmap(self.img_list[self.img_index])
        self.lbl_img.setPixmap(pixmap)
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
