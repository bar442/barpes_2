import pyqtgraph as pg
from typing import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import  QWidget,QLabel,QVBoxLayout,QGridLayout,QSlider,QPushButton,QGraphicsRotation,QColorDialog,QInputDialog,QMenu,QDoubleSpinBox


class PQ_LabelsGroup():
    def __init__(self):
        self.labels:List[pg.TextItem]=[]
        self.labels_spacing:float=17
        self.parent_plot:pg.PlotItem=None
        
    def add_label(self,txt:str,color="green"):
        if len(self.labels)==0:pos=QtCore.QPointF(50, 0)
        else:
            bl=self.labels[len(self.labels)-1]
            pos=QtCore.QPointF(bl.pos().x(),bl.pos().y()+self.labels_spacing)
        new_bl=pg.TextItem(txt, anchor=(0,0),color=color)
        new_bl.setPos(pos)
        self.labels.append(new_bl)
        if self.parent_plot: new_bl.setParentItem(self.parent_plot)

    def _set_positions_by_lead(self):
        if len(self.labels)<2:return
        last_pos=self.labels[0].pos()
        for lbl in self.labels[1:]:
            lbl.setPos(QtCore.QPointF(last_pos.x(),last_pos.y() + self.labels_spacing))
            last_pos=lbl.pos()
            
    def move_horizontally(self,step_size:float):
        if len(self.labels)<1:return
        lead_label=self.labels[0]
        lead_pos=lead_label.pos()
        lead_label.setPos(QtCore.QPointF(lead_pos.x() + step_size ,lead_pos.y()))
        self._set_positions_by_lead()
            
    def move_vertically(self,step_size:float):
        if len(self.labels)<1:return
        lead_label=self.labels[0]
        lead_pos=lead_label.pos()
        lead_label.setPos(QtCore.QPointF(lead_pos.x() ,lead_pos.y() - step_size))
        self._set_positions_by_lead()

    def add_to_plot(self,plot:pg.PlotItem):
        self.parent_plot=plot
        for pl in self.labels:
            pl.setParentItem(self.parent_plot)

    def clear(self):
        if self.parent_plot:
            for pl in self.labels:
                pl.setParentItem(None)
        self.labels.clear()
        



class PQ_LabelsGroup_Controller(QWidget):

    def __init__(self, labels_group:PQ_LabelsGroup):
        super().__init__() 
        self.labels_group:PQ_LabelsGroup=labels_group

        ########### general layout ###########
        self.layout=QGridLayout()
        self.setLayout(self.layout)

        ########### horizontal movement control ###########
        _horizontal_movement_row=1
        self.horizontal_movement_label=QLabel("horizontal movement: ")
        self.horizontal_movement_step_size_input=QDoubleSpinBox()
        self.horizontal_movement_step_size_input.setMinimum(-360)
        self.horizontal_movement_to_positive_button=QPushButton(text=">>")
        self.horizontal_movement_to_positive_button.clicked.connect(lambda :self.labels_group.move_horizontally(self.horizontal_movement_step_size_input.value()))
        self.horizontal_movement_to_negative_button=QPushButton(text="<<")
        self.horizontal_movement_to_negative_button.clicked.connect(lambda :self.labels_group.move_horizontally(-self.horizontal_movement_step_size_input.value()))
        self.layout.addWidget(self.horizontal_movement_label,_horizontal_movement_row,0)
        self.layout.addWidget(self.horizontal_movement_to_negative_button,_horizontal_movement_row,1)
        self.layout.addWidget(self.horizontal_movement_step_size_input,_horizontal_movement_row,2)
        self.layout.addWidget(self.horizontal_movement_to_positive_button,_horizontal_movement_row,3)
        

        ########### vertical movement control ###########
        _vertical_movement_row=2
        self.vertical_movement_label=QLabel("vertical movement: ")
        self.vertical_movement_step_size_input=QDoubleSpinBox()
        self.vertical_movement_step_size_input.setMinimum(-360)
        self.vertical_movement_to_positive_button=QPushButton(text=">>")
        self.vertical_movement_to_positive_button.clicked.connect(lambda :self.labels_group.move_vertically(self.vertical_movement_step_size_input.value()))
        self.vertical_movement_to_negative_button=QPushButton(text="<<")
        self.vertical_movement_to_negative_button.clicked.connect(lambda :self.labels_group.move_vertically(-self.vertical_movement_step_size_input.value()))
        self.layout.addWidget(self.vertical_movement_label,_vertical_movement_row,0)
        self.layout.addWidget(self.vertical_movement_to_negative_button,_vertical_movement_row,1)
        self.layout.addWidget(self.vertical_movement_step_size_input,_vertical_movement_row,2)
        self.layout.addWidget(self.vertical_movement_to_positive_button,_vertical_movement_row,3)