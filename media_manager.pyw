"""A GUI implementation of a media manager"""
import sys
from PyQt5 import QtWidgets, QtGui
import os
import shutil
# imported for use of background colour
from PyQt5.QtCore import Qt

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """ Creates the GUI interface"""
        # initialize the image to be placed at the top of window
        self.banner_img = QtWidgets.QLabel(self)
        # define the location of the image
        self.banner_img.setPixmap(QtGui.QPixmap("Media-Manager.png"))


        # set up the line edit widget for directory entry
        self.dir_label = QtWidgets.QLabel("Directory (Paste exact location of unsorted files eg. C:\\Users\\Michael\\Downloads)")
        self.dir_entry = QtWidgets.QLineEdit()

        # set up the extension and folder labels
        self.ext_label = QtWidgets.QLabel("Extension (eg. MP3 or DOCX)")
        self.folder_label = QtWidgets.QLabel("Folder (eg. My Music, My Documents)")

        # set up the entry section for the extension and folders
        self.ext_entry = []
        self.folder_entry = []

        # add a sort row
        self.ext_entry.append(QtWidgets.QLineEdit())
        self.folder_entry.append(QtWidgets.QLineEdit())

        # set the directory entry section
        d_sect = QtWidgets.QHBoxLayout()
        d_sect.addWidget(self.dir_label)
        d_sect.addWidget(self.dir_entry)

        # create a button to add more entries for extensions and folders
        self.add_entry_button = QtWidgets.QPushButton("ADD SORT ROW")

        # create a button to remove entry rows
        # self.remove_entry_button = QtWidgets.QPushButton("REMOVE SORT ROW")


        # set the media management section
        self.manage_files = QtWidgets.QGridLayout()
        self.manage_files.setSpacing(5)
        self.manage_files.addWidget(self.ext_label, 1, 0)
        self.manage_files.addWidget(self.folder_label, 1, 1)
        self.manage_files.addWidget(self.add_entry_button, 1, 2)
        # self.manage_files.addWidget(self.remove_entry_button,1,3)
        for ext_entry in self.ext_entry:
            self.manage_files.addWidget(ext_entry, 2 ,0)
        for folder_entry in self.folder_entry:
            self.manage_files.addWidget(folder_entry, 2, 1)

        # row and column numbers are specified here so when the user
        # chooses to create a new entry it doesn't add on to the previous ones
        self.start_row = 3
        self.start_column = 0

        # manage_files.addWidget(self.ext_entry,2,0)
        # manage_files.addWidget(self.folder_entry,2,1)

        # create a button to start the sorting process
        self.sort_button = QtWidgets.QPushButton("GO!")
        self.button_section = QtWidgets.QHBoxLayout()
        self.button_section.addStretch(2)
        self.button_section.addWidget(self.sort_button)

        # set actions for clicking of buttons
        self.sort_button.clicked.connect(self.sort)
        self.add_entry_button.clicked.connect(self.add_entry)
        # self.remove_entry_button.clicked.connect(self.remove_entry)

        # setting the layout of the window
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.banner_img)
        v_box.addLayout(d_sect)
        v_box.addLayout(self.manage_files)
        v_box.addLayout(self.button_section)
        self.setLayout(v_box)

        # give the app an icon
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # setting the background colour
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(self.p)
        # set a title for the Window
        self.setWindowTitle("Media Manager")
        # make the window show maximized
        self.show()
        # start the application

    def sort(self):
        """ Sorts the files in the folder based on their extensions """
        extensions = []
        folders = []
        for extension in self.ext_entry:
            extension = extension.text()
            if extension == '':
                continue
            extension = '.' + extension
            extension = extension.lower()
            extensions.append(extension)
        for folder in self.folder_entry:
            if folder.text == "":
                continue
            folders.append(folder.text())
        src_dir = self.dir_entry.text()
        dst_dir = []
        for folder in folders:
            dir = src_dir + '\\' + folder
            dst_dir.append(dir)
            # create the destination directory if it doesn't already exist
            if not os.path.exists(dir):
                os.makedirs(dir)

        # move all files with the user-defined extensions to the user-specified folder
        for i in range(len(extensions)):
            for filename in os.listdir(src_dir):
                if filename.endswith(extensions[i]):
                    file_path = os.path.join(src_dir, filename)
                    check_path = os.path.join(dst_dir[i], filename)
                    if os.path.isfile(check_path):
                        continue
                    shutil.move(file_path, dst_dir[i])

    def add_entry(self):
        """ Adds another sort field to the GUI interface """
        self.ext_entry.append(QtWidgets.QLineEdit())
        self.folder_entry.append(QtWidgets.QLineEdit())
        self.manage_files.addWidget(self.ext_entry[-1],self.start_row,self.start_column)
        self.manage_files.addWidget(self.folder_entry[-1],self.start_row,self.start_column+1)
        self.start_row += 1


# initialize the app
APP = QtWidgets.QApplication(sys.argv)
WINDOW = Window()
sys.exit(APP.exec_())
