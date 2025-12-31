from typing import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import  QWidget,QLabel,QVBoxLayout,QGridLayout,QSlider,QPushButton,QGraphicsRotation
from PyQt5.QtWidgets import  QColorDialog,QPushButton,QComboBox,QInputDialog,QLineEdit,QMessageBox
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import uuid
import scipy as sc
import scipy.optimize as opt
from PyQt5.QtWidgets import QMenuBar ,QMenu
from ..widgets import BarpesGraphicsLayoutWidget,BarpesPlotItem
from ..view_services import show_widget,QMenuBarTemplate



class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        ########### private properties variables ###########


        ########### general layout ###########
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.graphics_layout=BarpesGraphicsLayoutWidget()
        self.layout.addWidget(self.graphics_layout,2,2)

        ########### Main Plot ###########
        self.main_plot:BarpesPlotItem=self.graphics_layout.addBarpesPlot(row=2,col=1)

        ########### General Menu Bar ###########
        self.menuBarTemplate:QMenuBarTemplate = QMenuBarTemplate(self)
        self.menuBarTemplate.append(self.graphics_layout.menuBarTemplate)