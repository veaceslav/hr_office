# This is a sample Python script.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, QFileDialog, QHBoxLayout, QListWidget, QTextEdit

from PyQt5.QtGui import QIcon
import sys
import csv_parsing
from pathlib import Path
import pprint


class MainWidget(QWidget):
    def __init__(self, filepath):
        super().__init__()
        self.file_path = filepath
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.entries = csv_parsing.parse_csv(self.file_path)

        names = [x.name + " " + x.surname  for x in self.entries ]
        pprint.pprint(self.entries)
        pprint.pprint(names)

        main_layout = QHBoxLayout()
        self.list_view = QListWidget()
        self.list_view.addItems(names)

        self.list_view.currentRowChanged.connect(self.list_index_changed)
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        main_layout.addWidget(self.list_view,1)
        main_layout.addWidget(self.text_view, 3)
        self.setLayout(main_layout)
        self.show()

    def list_index_changed(self, current):
        print("current changed" + str(current))
        self.text_view.setText(csv_parsing.create_email(self.entries[current]))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textLabel = QLabel("Please use File->Open to select the downloaded csv file from HR Office \n")
        self.setCentralWidget(self.textLabel)
        self.statusBar()

        openFile = QAction(QIcon(), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        #self.process_csv('/home/veaceslav/git/Hr_Office/Export of candidates 09-11-2020.csv')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 550, 450)
        self.setWindowTitle('Classmarker Generator')
        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, filter="*.csv")

        if fname[0]:
            self.process_csv(fname[0])

    def process_csv(self,file_path):
        self.widget = MainWidget(file_path)
        self.setCentralWidget(self.widget)
        self.widget.show()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
