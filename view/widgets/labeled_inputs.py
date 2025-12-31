from typing import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import  QWidget,QLabel,QVBoxLayout,QHBoxLayout,QGridLayout,QSlider,QPushButton,QGraphicsRotation
from PyQt5.QtWidgets import  QTableWidget,QTableWidgetItem,QSpinBox,QListWidget
from PyQt5.QtWidgets import  QColorDialog,QPushButton,QComboBox,QInputDialog,QLineEdit,QMessageBox ,QDoubleSpinBox 
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QMenuBar ,QMenu
from PyQt5.QtWidgets import QFileDialog


class Labeled_SpinBox(QWidget):
    def __init__(self, pre_txt:str=None,post_txt:str=None , vertical:bool=False , action_button:bool=False):
        super().__init__()

        ########### general layout ###########
        self.layout=QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(self.layout)

        ########### widgets ###########
        self.pre_label=QLabel()
        self.post_label=QLabel()
        self.spinbox=QSpinBox()
        self.button=QPushButton()
        # ---
        self.layout.addWidget(self.pre_label)
        self.layout.addWidget(self.spinbox)
        self.layout.addWidget(self.post_label)
        if action_button:
            self.layout.addWidget(self.button)

        ########### initialization ###########
        if pre_txt:self.pre_label.setText(pre_txt)
        if post_txt:self.post_label.setText(post_txt)


class Labeled_DoubleSpinBox(QWidget):
    def __init__(self, pre_txt:str=None,post_txt:str=None , vertical:bool=False , action_button:bool=False):
        super().__init__()

        ########### general layout ###########
        self.layout=QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(self.layout)

        ########### widgets ###########
        self.pre_label=QLabel()
        self.post_label=QLabel()
        self.spinbox=QDoubleSpinBox()
        self.button=QPushButton()
        # ---
        self.layout.addWidget(self.pre_label)
        self.layout.addWidget(self.spinbox)
        self.layout.addWidget(self.post_label)
        if action_button:
            self.layout.addWidget(self.button)

        ########### initialization ###########
        if pre_txt:self.pre_label.setText(pre_txt)
        if post_txt:self.post_label.setText(post_txt)


class Labeled_LineEdit(QWidget):
    def __init__(self, pre_txt:str=None,post_txt:str=None , vertical:bool=False , action_button:bool=False):
        super().__init__()

        ########### general layout ###########
        self.layout=QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(self.layout)

        ########### widgets ###########
        self.pre_label=QLabel()
        self.post_label=QLabel()
        self.line_edit=QLineEdit()
        self.button=QPushButton()
        # ---
        self.layout.addWidget(self.pre_label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.post_label)
        if action_button:
            self.layout.addWidget(self.button)

        ########### initialization ###########
        if pre_txt:self.pre_label.setText(pre_txt)
        if post_txt:self.post_label.setText(post_txt)


class Labeled_List(QWidget):
    def __init__(self, pre_txt:str=None,post_txt:str=None , vertical:bool=False , action_button:bool=False):
        super().__init__()

        ########### general layout ###########
        self.layout=QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(self.layout)

        ########### widgets ###########
        self.pre_label=QLabel()
        self.post_label=QLabel()
        self.list=QListWidget()
        self.button=QPushButton()
        # ---
        self.layout.addWidget(self.pre_label)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.post_label)
        if action_button:
            self.layout.addWidget(self.button)

        ########### initialization ###########
        if pre_txt:self.pre_label.setText(pre_txt)
        if post_txt:self.post_label.setText(post_txt)


class Labeled_ComboBox(QWidget):
    def __init__(self, pre_txt:str=None,post_txt:str=None , vertical:bool=False , action_button:bool=False):
        super().__init__()

        ########### general layout ###########
        self.layout=QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(self.layout)

        ########### widgets ###########
        self.pre_label=QLabel()
        self.post_label=QLabel()
        self.combobox=QComboBox()
        self.button=QPushButton()
        # ---
        self.layout.addWidget(self.pre_label)
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.post_label)
        if action_button:
            self.layout.addWidget(self.button)

        ########### initialization ###########
        if pre_txt:self.pre_label.setText(pre_txt)
        if post_txt:self.post_label.setText(post_txt)







