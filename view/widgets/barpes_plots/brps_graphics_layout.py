from typing import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import  QWidget,QLabel,QVBoxLayout,QGridLayout,QSlider,QPushButton,QGraphicsRotation,QColorDialog,QMenu,QFileDialog
from PyQt5.QtWidgets import  QGraphicsView,QGraphicsScene,QGraphicsProxyWidget ,QInputDialog,QLineEdit
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QMenuBar ,QMenu
from pyqtgraph.Qt import QtGui
from ..labels_group import PQ_LabelsGroup,PQ_LabelsGroup_Controller
from ...view_services import show_widget , QMenuBarTemplate
from .brp_plot_item import BarpesPlotItem
from .brp_image_plot_item import BarpesImagePlotItem

class BarpesGraphicsLayoutWidget(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None, show=False, size=None, title=None, **kargs):
        super().__init__(parent, show, size, title, **kargs)

        #------------------------------

        ########### design & colors ###########
        self.setBackground('white')


        ########### General Menu Bar ###########
        self.menuBarTemplate:QMenuBarTemplate = QMenuBarTemplate(self)
        #------
        self.menu_plots=self.menuBarTemplate.addMenu("plots")

    def addBarpesPlot(self,row:int,col:int)->BarpesPlotItem:
        result = BarpesPlotItem()
        self.ci.addItem(result, row, col, rowspan=1, colspan=1)
        # QMenuBarTemplate.add_template_to_a_menu(self.menuBarTemplate,result.menuBarTemplate)
        QMenuBarTemplate.add_template_to_a_menu(self.menu_plots,result.menuBarTemplate)
        return result
    
    def addBarpesImagePlot(self,row:int,col:int)->BarpesImagePlotItem:
        result = BarpesImagePlotItem()
        self.ci.addItem(result, row, col, rowspan=1, colspan=1)
        # QMenuBarTemplate.add_template_to_a_menu(self.menuBarTemplate,result.menuBarTemplate)
        QMenuBarTemplate.add_template_to_a_menu(self.menu_plots,result.menuBarTemplate)
        return result