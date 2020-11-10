# This is a sample Python script.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, QFileDialog,\
    QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit, QPushButton, QMessageBox

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
        self.entries, error = csv_parsing.parse_csv(self.file_path)

        if error:
            self.display_error("The csv file is malformed", error)

        names = [x.name + " " + x.surname for x in self.entries ]

        main_layout = QHBoxLayout()
        self.list_view = QListWidget()
        self.list_view.addItems(names)
        self.list_view.currentRowChanged.connect(self.list_index_changed)

        text_layout = QVBoxLayout()
        self.extra_info = QLabel()
        self.extra_info.setStyleSheet("font-weight: bold; color: black")
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)

        text_layout.addWidget(self.extra_info)
        text_layout.addWidget(self.copy_button)
        text_layout.addWidget(self.text_view)
        main_layout.addWidget(self.list_view,1)
        main_layout.addLayout(text_layout, 3)
        self.setLayout(main_layout)
        self.show()

    def list_index_changed(self, current):
        entry = self.entries[current]
        self.copy_button.setText("Copy to Clipboard")
        self.copy_button.setStyleSheet("color: black")
        email, error = csv_parsing.create_email(entry)

        if error:
            self.display_error("Could not create candidate email", error)
        self.text_view.setText(email)
        self.extra_info.setText(entry.job +
                                ", email: " + entry.email + ", Phone: " + entry.phone)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.text_view.toPlainText())
        self.copy_button.setStyleSheet("font-weight: bold; color: green")
        self.copy_button.setText("Copied to Clipboard!")

    def display_error(self, error, extra):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)

        msg.setWindowTitle("Error")

        msg.setDetailedText(extra)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


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

        #self.process_csv('C:\\Users\\Slavik\\PycharmProjects\\hr_office\\Export of candidates 09-11-2020.csv')
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
