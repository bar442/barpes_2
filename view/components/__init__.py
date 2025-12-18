from tkinter import Scale
from typing import *
from unicodedata import name
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


class DataViewer1D(QWidget):
    def __init__(self):
        super().__init__()

        ########### general layout ###########
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.graphics_layout=pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graphics_layout,2,2)

        ########### Main Plot ###########
        self.main_plot:pg.PlotItem=self.graphics_layout.addPlot(row=2,col=1)
        self.main_plot.setLabel(axis='left', text="self.y_scale_name")
        self.main_plot.setLabel(axis='bottom', text="self.x_scale_name")
        ########### Main Curve ###########
        self.main_curve=pg.PlotCurveItem(pen=pg.mkPen("red", width=1))
        # self.main_curve=self.main_plot.plot(pen=pg.mkPen((90, 0, 163), width=1))
        self.main_curve.setData(x=np.array([1,2,3,4,5,6]),y=np.array([1,2,3,4,5,6]))
        self.main_plot.addItem(self.main_curve)
        # self.graphics_layout.ci.layout.setRowMaximumHeight(1, 150)