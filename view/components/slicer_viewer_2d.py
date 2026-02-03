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
from ..widgets import BarpesGraphicsLayoutWidget,BarpesPlotItem,BarpesImagePlotItem
from ..view_services import show_widget,QMenuBarTemplate
from .data_viewer_image import DataViewer_Image
from ..widgets import Slicer_2D_Widget
from model import Measurement,Slicer_2D

class SlicerViewer2D(DataViewer_Image):
    def __init__(self , slicer_widget:Slicer_2D_Widget):
        super().__init__()
        ########### private properties variables ###########


        ########### Slicer Widget  ###########
        self.slicer_widget:Slicer_2D_Widget=slicer_widget
        self.layout.addWidget(self.slicer_widget,1,2)
        self.slicer_widget.subscribe_to_redraw_needed(self._on_slicer_redraw)
        self.slicer_widget.subscribe_to_viewed_indices_changed(self._on_slicer_redraw)


    def _on_slicer_redraw(self , slicer:Slicer_2D_Widget=None):
        if slicer is None:slicer=self.slicer_widget
        self.image_plot.setData(data=slicer.image,scales=slicer.viewed_scales,scales_labels=slicer.viewed_scales_labels)


    # region Initializers

    @classmethod
    def from_measurement(cls:'SlicerViewer2D' , mes:Measurement):
        slc_widget = Slicer_2D_Widget(data=mes.data,scale_axises=mes.scales , scales_labels=mes.scales_names)
        slc_viewer = cls(slc_widget)
        return slc_viewer



    # endregion