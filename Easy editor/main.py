from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter


class ImageProessor:
    def __init__(self):
        self.image = None
        self.directory = None
        self.filename = None
        self.save_dir = 'modified/'
        self.history = []
    def load_image(self, directory, filename):
        self.directory = directory
        self.filename = filename
        self.image = Image.open(os.path.join(directory, filename)) 
        self.history = [os.path.join(self.directory, self.filename)]

    def show_image(self, directory, filename):
        piximap_image = QPixmap(os.path.join(directory, filename))
        width = lb_image.width()
        height = lb_image.height()
        piximap_image = piximap_image.scaled(width, height, Qt.KeepAspectRatio)
        lb_image.setPixmap(piximap_image)

    def save_image(self):
        save_path = os.path.join(self.directory, self.save_dir)
        if not(os.path.exists(save_path) or os.path.isdir(save_path)):
            os.mkdir(save_path)
        base_filename, extentions = os.path.splitext(self.filename)
        verson = 1
        new_filename = base_filename + "_" + str(verson) + extentions
        new_filename = f"{base_filename}_{verson}{extentions}"
        while os.path.exists(os.path.join(save_path, new_filename)):
            verson += 1
            new_filename = f"{base_filename}_{verson}{extentions}"

        self.image.save(os.path.join(save_path, new_filename))
        self.history.append(os.path.join(save_path, new_filename))

        return new_filename
    
    def undo(self):
        if len(self.history) > 1:
            current_image_path = self.history.pop()

            if os.path.exists(current_image_path):
                #os.remove(current_image_path)
                print(f"Remove file: {current_image_path}")

            previous_image_path = self.history[-1]
            directory = os.path.dirname(previous_image_path)
            filename = os.path.basename(previous_image_path)
            self.image = Image.open(previous_image_path)
            self.show_image(directory, filename)


    def do_bw(self):
        self.image = self.image.convert('1')
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)

    def do_left(self):
        self.image = self.image.rotate(90, expand=True)
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)

    def do_right(self):
        self.image = self.image.rotate(-90, expand=True)
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)
        

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)


    def do_sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)

    def apply_filters(self, filter_type):
        if filter_type == 'blur':
            self.image = self.image.filter(ImageFilter.BLUR)
        elif filter_type == 'contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        elif filter_type == 'emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)
        elif filter_type =='detail':
            self.image = self.image.filter(ImageFilter.DETAIL)
        elif filter_type =='edge_enhance':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            
        new_filename = self.save_image()
        self.show_image(os.path.join(self.directory, self.save_dir), new_filename)

            

app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle("Easy Editor App")
main_win.resize(900, 600)
main_win.setWindowIcon(QIcon('icon.jfif'))

cb_filters = QComboBox()
cb_filters.addItems(['blur', 'contour', 'emboss', 'detail', 'edge_enhance'])
btn_apply_filter = QPushButton('Apply Filter')

lb_image = QLabel('')
lw_files = QListWidget() 

btn_folder = QPushButton("Folder")
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_mirror = QPushButton("Mirror")
btn_Sharpness = QPushButton("sharpness")
btn_BnW = QPushButton("B/W")
btn_undo = QPushButton("Undo")

layout_main = QHBoxLayout()


layout_left = QVBoxLayout()
layout_left.addWidget(btn_folder)
layout_left.addWidget(btn_undo)
layout_left.addWidget(lw_files)
layout_left.addWidget(cb_filters)
layout_left.addWidget(btn_apply_filter)

layout_right = QVBoxLayout()
layout_right.addWidget(lb_image)

layout_row = QHBoxLayout()
layout_row.addWidget(btn_left)
layout_row.addWidget(btn_right)
layout_row.addWidget(btn_mirror)
layout_row.addWidget(btn_Sharpness)
layout_row.addWidget(btn_BnW)

layout_right.addLayout(layout_row)

layout_main.addLayout(layout_left, stretch=1)
layout_main.addLayout(layout_right, stretch=4)
main_win.setLayout(layout_main)

def chooose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def show_filename_list():
    extenstions = [".jpg", ".jepg", ".png", ".bmp", ".svg", ".gif"]
    chooose_workdir()

    filenames = filter(os.listdir(workdir), extenstions)

    lw_files.clear()

    for filename in filenames:
        lw_files.addItem(filename)

image_processor = ImageProessor()

def show_chosen_image():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        image_processor.load_image(workdir, filename)
        image_processor.show_image(workdir, filename)

def apply_filter():
    selected_filter = cb_filters.currentText()
    image_processor.apply_filters(selected_filter)




btn_folder.clicked.connect(show_filename_list)
lw_files.currentRowChanged.connect(show_chosen_image)

btn_left.clicked.connect(image_processor.do_left)
btn_undo.clicked.connect(image_processor.undo)
btn_right.clicked.connect(image_processor.do_right)
btn_BnW.clicked.connect(image_processor.do_bw)
btn_mirror.clicked.connect(image_processor.do_mirror)
btn_Sharpness.clicked.connect( image_processor.do_sharpness)
btn_apply_filter.clicked.connect(apply_filter)

main_win.show()
app.exec()