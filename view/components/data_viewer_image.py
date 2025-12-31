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
from model import Slicer_1D


class DataViewer_Image(QWidget):
    def __init__(self):
        super().__init__()
        ########### private properties variables ###########


        ########### general layout ###########
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.graphics_layout=BarpesGraphicsLayoutWidget()
        self.layout.addWidget(self.graphics_layout,2,2)

        ########### Main Plot ###########
        self.image_plot:BarpesImagePlotItem=self.graphics_layout.addBarpesImagePlot(row=2,col=1)

        ########### General Menu Bar ###########
        self.menuBarTemplate:QMenuBarTemplate = QMenuBarTemplate(self)
        self.menuBarTemplate.append(self.graphics_layout.menuBarTemplate)
        #------
        self.menuBarTemplate.addAction("open rotation tool",self.open_rotation_tool)


    def open_rotation_tool(self):
        rot_tool=ImageRotationTool()
        rot_tool.image_plot.setData(data=self.image_plot.data,scales=self.image_plot.scales,scales_labels=self.image_plot.scales_labels)
        show_widget(rot_tool,"Rotation Tool")






class ImageRotationTool(DataViewer_Image):
    def __init__(self):
        super().__init__()
        ########### private properties variables ###########

        # self.layout.addWidget(QSlider(),2,1)
        ########### Rotation Slider ###########
        # ---- needed variables
        self.rotation_angle=0
        # ---- layout
        self.rotation_slider_widget=QWidget()
        self.rotation_slider_layout=QVBoxLayout()
        self.rotation_slider_widget.setLayout(self.rotation_slider_layout)
        self.layout.addWidget(self.rotation_slider_widget,2,1)
        # ---- label
        self.rotation_slider_label=QLabel("0")
        self.rotation_slider_layout.addWidget(self.rotation_slider_label)
        # ---- slider
        self.rotation_slider=QSlider()
        self.rotation_slider.setMinimum(-180)
        self.rotation_slider.setMaximum(180)
        self.rotation_slider.setSingleStep(1)
        self.rotation_slider.valueChanged.connect(self.on_rotation_slider_value_changed)
        self.rotation_slider_layout.addWidget(self.rotation_slider)
        # ---- reset button
        self.rotation_reset_button=QPushButton(text="reset")
        self.rotation_reset_button.pressed.connect(lambda :self.rotation_slider.setValue(0))
        self.rotation_slider_layout.addWidget(self.rotation_reset_button)
        # ---- register menu actions
        # self.image_plot.getMenu().addAction('Toggle Rotation Tool',self.toggleRotationSlider)
        # ---- set initial state
        self.rotation_slider_widget.setMaximumWidth(60)
        # self.rotation_slider_widget.hide()



        ########### Infinity Lines ###########
        self.infinity_line_vertical = pg.InfiniteLine(movable=True, angle=90, label='x={value:0.2f}',pen=pg.mkPen((250, 91, 5),width=1), labelOpts={'position':0.1, 'color': (250, 91, 5), 'fill': (200,200,200,50), 'movable': True})
        self.infinity_line_horizontal = pg.InfiniteLine(movable=True, angle=0, label='y={value:0.2f}',pen=pg.mkPen((250, 91, 5),width=1) , labelOpts={'position':0.1, 'color': (250, 91, 5), 'fill': (200,200,200,50), 'movable': True})
        self.image_plot.addItem(self.infinity_line_vertical)
        self.image_plot.addItem(self.infinity_line_horizontal)

    def on_rotation_slider_value_changed(self,value:float=None):
        self.rotation_slider_label.setText(str(value))
        if value==0:
            self.infinity_line_horizontal.setMovable(True)
            self.infinity_line_vertical.setMovable(True)
        else:
            self.infinity_line_horizontal.setMovable(False)
            self.infinity_line_vertical.setMovable(False)

        ####### create rotation transform ##########
        x_scale,y_scale = self.image_plot.x_scale,self.image_plot.y_scale
        rot_x,rot_y=(self.infinity_line_vertical.value(),self.infinity_line_horizontal.value()) 
        deg=value

        trans=QtGui.QTransform()
        min_x,max_x,min_y,max_y= x_scale.min() , x_scale.max() , y_scale.min() , y_scale.max()
        x_scale_length,y_scale_length = abs(x_scale[0]-x_scale[-1]) , abs(y_scale[0]-y_scale[-1])
        x_scale_pixel_size , y_scale_pixel_size = x_scale_length/len(x_scale) , y_scale_length/len(y_scale)

        trans.translate(rot_x,rot_y).scale(x_scale_pixel_size,y_scale_pixel_size)
        trans.rotate(deg)
        trans.translate(-Slicer_1D.find_nearest_index(x_scale,rot_x),-Slicer_1D.find_nearest_index(y_scale,rot_y))

        ####### apply rotation transform ##########
        self.image_plot.image_item.setTransform(trans)
        self.rotation_angle=value






    def on_rotation_slider_value_changed_old(self,value:float=None):
        self.rotation_slider_label.setText(str(value))
        if value==0:
            x_scale,y_scale = self.image_plot.x_scale,self.image_plot.y_scale

            trans=self.image_plot.create_image_to_scale_and_position_transform()
            self.image_plot.image_item.setTransform(trans)
            self.infinity_line_horizontal.setMovable(True)
            self.infinity_line_vertical.setMovable(True)
            buffer=abs(x_scale.max()-x_scale.min())*0.1
            self.image_plot.setYRange(y_scale.min(),y_scale.max())
            self.image_plot.setXRange(x_scale.min()-buffer,x_scale.max()+buffer)
            
        else:
            x_rot,y_rot=(self.infinity_line_vertical.value(),self.infinity_line_horizontal.value())
            size=10
            trans=self.image_plot.create_image_rotation_transform(value,rot_x=x_rot,rot_y=y_rot,size=size)
            self.infinity_line_horizontal.setMovable(False)
            self.infinity_line_vertical.setMovable(False)
            self.image_plot.image_item.setTransform(trans)
            if self.rotation_angle==0:
                buffer=size*0.6
                self.image_plot.setYRange(y_rot-1,y_rot+1)
                self.image_plot.setXRange(x_rot-buffer,x_rot+buffer)
            
        self.rotation_angle=value