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



        ########### General Menu Bar ###########
        self.infinity_lines_menu=self.menuBarTemplate.addMenu("inf lines",self)
        # ---- register menu actions
        self.infinity_lines_menu.addAction('change color horizontal',self.change_color_horizontal_inf_line)
        self.infinity_lines_menu.addAction('change color vertical',self.change_color_vertical_inf_line)
        self.infinity_lines_menu.addAction('find middle',self.locate_infinity_lines_in_middle)


    def on_rotation_slider_value_changed(self,value:float=None):
        self.rotation_slider_label.setText(str(value))
        old_rotation_angle=self.rotation_angle
        if value==0:
            self.infinity_line_horizontal.setMovable(True)
            self.infinity_line_vertical.setMovable(True)
            self.image_plot.getViewBox().setAspectLocked(lock=False)
        if old_rotation_angle == 0 and value !=0:
            self.infinity_line_horizontal.setMovable(False)
            self.infinity_line_vertical.setMovable(False)

            vb=self.image_plot.getViewBox()
            (xmin, xmax), (ymin, ymax) = vb.viewRange()
            w, h = vb.width(), vb.height()
            sx = w / (xmax - xmin)   # pixels per data unit (x)
            sy = h / (ymax - ymin)   # pixels per data unit (y)
            aspect = sx / sy
            # self.image_plot.getViewBox().setAspectLocked(lock=True,ratio=aspect)

        ####### create rotation transform ##########
        x_scale,y_scale = self.image_plot.x_scale,self.image_plot.y_scale
        rot_x,rot_y=(self.infinity_line_vertical.value(),self.infinity_line_horizontal.value()) 
        deg=value

        trans=QtGui.QTransform()
        min_x,max_x,min_y,max_y= x_scale.min() , x_scale.max() , y_scale.min() , y_scale.max()
        x_scale_length,y_scale_length = abs(x_scale[0]-x_scale[-1]) , abs(y_scale[0]-y_scale[-1])
        x_scale_pixel_size , y_scale_pixel_size = x_scale_length/len(x_scale) , y_scale_length/len(y_scale)




        ######################### Origin
        # trans.translate(rot_x,rot_y).scale(x_scale_pixel_size,y_scale_pixel_size)
        # trans.rotate(deg)
        # trans.translate(-Slicer_1D.find_nearest_index(x_scale,rot_x),-Slicer_1D.find_nearest_index(y_scale,rot_y))




        ######################### try 001
        # vb=self.image_plot.getViewBox()
        # (xmin, xmax), (ymin, ymax) = vb.viewRange()
        # w, h = vb.width(), vb.height()
        # sx = w / (xmax - xmin)   # pixels per data unit (x)
        # sy = h / (ymax - ymin)   # pixels per data unit (y)
        # aspect = sx / sy
        # trans.scale(1/sx,1/sy).scale(1/sx,1/sy).rotate(deg)

        ######################### try 002
        # self.image_plot.image_item.setRect(x_scale[0],y_scale[0],x_scale_length,y_scale_length)
        # self.image_plot.image_item.setRect(14,-23,2.5,46)
        # trans.reset()
        # trans.rotate(deg)


        ######################### try 003
        trans_matrix=np.array([[1,0,0],
                               [0,1,0],
                               [0,0,1]])
        scale_matrix=np.array([[x_scale_pixel_size,0                 ,0],
                               [0                 ,y_scale_pixel_size,0],
                               [0                 ,0                 ,1]])
        
        
        ts=trans_matrix*scale_matrix
        trans=QtGui.QTransform(
            ts[0][0], ts[0][1], ts[0][2],
            ts[1][0], ts[1][1], ts[1][2],
            ts[2][0], ts[2][1], ts[2][2]
            )



        ####### apply rotation transform ##########
        self.image_plot.image_item.setTransform(trans)
        self.rotation_angle=value




    def locate_infinity_lines_in_middle(self):
        x_mid = np.mean([self.image_plot.x_scale.min(),self.image_plot.x_scale.max()])
        y_mid = np.mean([self.image_plot.y_scale.min(),self.image_plot.y_scale.max()])
        self.infinity_line_horizontal.setPos(y_mid)
        self.infinity_line_vertical.setPos(x_mid)



    def change_color_horizontal_inf_line(self):
        color = QColorDialog.getColor()
        if color:
            self.infinity_line_horizontal.setPen(pg.mkPen(color, width=1))

    def change_color_vertical_inf_line(self):
        color = QColorDialog.getColor()
        if color:
            self.infinity_line_vertical.setPen(pg.mkPen(color, width=1))






def dump_tf(tf, name="tf"):
    print(
        name,
        " m11", tf.m11(), " m12", tf.m12(),
        " m21", tf.m21(), " m22", tf.m22(),
        " dx", tf.dx(),  " dy", tf.dy()
    )