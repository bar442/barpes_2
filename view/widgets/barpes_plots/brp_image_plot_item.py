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
from model import Slicer_1D

class BarpesImagePlotItem(BarpesPlotItem):
    def __init__(self,data:np.ndarray=None,scales:List[np.ndarray]=None,scales_label:List[str]=None):
        super().__init__()
        ########### private properties variables ###########
        self._data:np.ndarray = None
        self._scales:List[np.ndarray] = None
        self._scales_labels:List[str] = None


        ########### UI Elements ###########
        #------------------------------
        self.image_item= pg.ImageItem()
        self.addItem(self.image_item)
        # self.image_item.setColorMap(pg.colormap.get('viridis'))
        # self.image_item.setColorMap(pg.colormap.get('oranges'))
        self.image_item.setColorMap(pg.colormap.get("Oranges", source='matplotlib', skipCache=False))
        # ---- image item transform
        self.image_item_transform=QtGui.QTransform()
        self.image_item.setTransform(self.image_item_transform)
        # ---- color bar
        self.color_bar = pg.ColorBarItem( interactive=True)
        self.color_bar.setImageItem(self.image_item,insert_in=self)




        ########### initials actions ###########
        self.setData(data,scales,scales_label)


    # region properties

    @property
    def data(self): 
        if self._data is None: 
            self._data=np.zeros(shape=(2,2))
        return self._data
    
    @property
    def scales(self): 
        if not self._scales: self._scales=[np.array(range(sh)) for sh in self.data.shape]
        return self._scales
    
    @property
    def scales_labels(self): 
        if not self._scales_labels: self._scales_labels=["" for sh in self.data.shape]
        return self._scales_labels

    @property
    def x_scale(self)->np.ndarray: return self.scales[0]
    @property
    def y_scale(self)->np.ndarray: return self.scales[1]

    def setData(self,data:np.ndarray=None,scales:List[np.ndarray]=None,scales_labels:List[str]=None, rescale_view:bool=False):
        if data is not None:self._data=data
        if scales:self._scales=scales
        if scales_labels:self._scales_labels=scales_labels

        if len(self.data.shape) != 2 : raise Exception("BarpesImageGraphicsLayoutWidget.data accept only 2D numpy array")
        if len(self.scales) != 2 : raise Exception("BarpesImageGraphicsLayoutWidget.scales accept only list of 2 numpy arrays")
        if len(self.scales_labels) != 2 : raise Exception("BarpesImageGraphicsLayoutWidget.scales accept only list of 2 str")
    
        self.image_item.setImage(self._data,autoLevels=True)
        self.image_item.setLevels(levels=(self._data.min(),self._data.max()), update=True)
        self.color_bar.setLevels(values=(self._data.min(),self._data.max()))
        #---- image transform
        self.image_item_transform=self.create_image_to_scale_and_position_transform()
        self.image_item.setTransform(self.image_item_transform)
        #---- set image view
        if rescale_view:
            x_scale,y_scale = self.x_scale , self.scales[1]
            min_x,max_x,min_y,max_y= x_scale.min() , x_scale.max() , y_scale.min() , y_scale.max()
            self.setXRange(min_x,max_x)
            self.setYRange(min_y,max_y)
        #---- set axis labels
        self.setLabel(axis='left', text=self.scales_labels[1])
        self.setLabel(axis='bottom', text=self.scales_labels[0])


    # endregion


    # region image transformations

    def create_image_to_scale_transform(self)->QtGui.QTransform:
        trans=QtGui.QTransform()
        x_scale,y_scale = self.scales[0] , self.scales[1]
        x_scale_length,y_scale_length = abs(x_scale[0]-x_scale[-1]) , abs(y_scale[0]-y_scale[-1])
        x_scale_pixel_size , y_scale_pixel_size = x_scale_length/len(x_scale) , y_scale_length/len(y_scale)

        trans.scale(x_scale_pixel_size,y_scale_pixel_size)
        return trans        

    def create_image_to_scale_and_position_transform(self)->QtGui.QTransform:
        trans=QtGui.QTransform()
        x_scale,y_scale = self.scales[0] , self.scales[1]
        min_x,max_x,min_y,max_y= x_scale.min() , x_scale.max() , y_scale.min() , y_scale.max()
        x_scale_length,y_scale_length = abs(x_scale[0]-x_scale[-1]) , abs(y_scale[0]-y_scale[-1])
        x_scale_pixel_size , y_scale_pixel_size = x_scale_length/len(x_scale) , y_scale_length/len(y_scale)

        trans.translate(min_x,min_y).scale(x_scale_pixel_size,y_scale_pixel_size)
        return trans

    def create_image_rotation_transform(self,deg:float,rot_x:float=0,rot_y:float=0,size=10):
        x_scale,y_scale = self.x_scale,self.y_scale

        theta=np.deg2rad(deg)
        # self.vb.setAspectLocked(True,1)
        trans=QtGui.QTransform()
        trans.translate(rot_x,rot_y)
        trans.rotate(deg)
        nx,ny=(x_scale.shape[0],y_scale.shape[0])
        px,py=(size/nx,size/ny)
        trans.scale(px,py)
        trans.translate(-Slicer_1D.find_nearest_index(x_scale,rot_x),-Slicer_1D.find_nearest_index(y_scale,rot_y))
        
        return trans

    # endregion