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


class BarpesPlotItem(pg.PlotItem):
    def __init__(self, parent = None, name = None, labels = None, title = None, viewBox = None, axisItems = None, enableMenu = True, **kwargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kwargs)

        #------------------------------
        self._curve_plots:Dict[str,pg.PlotCurveItem]={}
        self._scatter_plots:Dict[str,pg.ScatterPlotItem]={}
        self._infinity_lines:List[pg.InfiniteLine]=[]
        # self._image_items:Dict[str,pg.ImageItem]={}


        ########### Label Group ###########
        self.label_group:PQ_LabelsGroup=PQ_LabelsGroup()
        self.label_group.add_to_plot(self)

        ########### General Menu Bar ###########
        self._menuBarTemplateWidget=QWidget()
        self.menuBarTemplate:QMenuBarTemplate = QMenuBarTemplate(self._menuBarTemplateWidget)
        #------
        self.menu_appearance=self.menuBarTemplate.addMenu("appearance")
        self.menu_appearance.addAction('Set Title',lambda :self.setTitleWitDialog())
        self.menu_appearance.addAction('Remove all curves',self.remove_all_curve_plots)
        self.menu_appearance.addAction('Remove all scatters',self.remove_all_scatter_plots)
        #------
        self.menu_labels=self.menu_appearance.addMenu("Labels")
        self.menu_labels.addAction('Add Label',lambda :self.add_label(txt=None,color=None))
        self.menu_labels.addAction('show controller',lambda :self.show_label_controller())
        self.menu_labels.addAction('Clear All Labels',lambda :self.label_group.clear())
        #------
        self.menu_infinity_lines=self.menuBarTemplate.addMenu("infinity lines")
        self.menu_infinity_lines.addAction('Add horizontal infinity line',self.add_horizontal_infinity_line)
        self.menu_infinity_lines.addAction('Add vertical infinity line',self.add_vertical_infinity_line)
        self.menu_infinity_lines.addAction('Remove All Extra infinity lines',self.remove_all_infinity_lines)






    def add_curve_plot(self,xs:np.ndarray,ys:np.ndarray,key:str=None,color="pink",line_width:int=1,curve_plot:pg.PlotCurveItem=None)->pg.PlotCurveItem:
        collection,result = self._curve_plots ,pg.PlotCurveItem(pen=pg.mkPen(color, width=line_width))
        if curve_plot : result=curve_plot
        auto_key_label="curve_plot"

        if key is None or not isinstance(key,str) or key in collection.keys():
            keys_counter=1
            key=f"{auto_key_label}_{str(keys_counter).zfill(4)}"
            while key in collection.keys():
                keys_counter=keys_counter+1
                key=f"{auto_key_label}_{str(keys_counter).zfill(4)}"

        collection[key]=result
        self.addItem(result)
        if xs is not None and ys is not None :
            result.setData(x=xs,y=ys)
        return result
    

    def add_scatter_plot(self,xs:np.ndarray=None,ys:np.ndarray=None,color="green",symbol ='t',size=10)->pg.ScatterPlotItem:
        collection,result = self._scatter_plots ,pg.ScatterPlotItem(size=size,brush=color,symbol =symbol)
        auto_key_label="scatter_plot"

        if key is None or not isinstance(key,str) or key in collection.keys():
            keys_counter=1
            key=f"{auto_key_label}_{str(keys_counter).zfill(4)}"
            while key in collection.keys():
                keys_counter=keys_counter+1
                key=f"{auto_key_label}_{str(keys_counter).zfill(4)}"

        collection[key]=result
        self.addItem(result)
        if xs is not None and ys is not None :
            result.setData(x=xs,y=ys)
        return result
    

    def remove_all_curve_plots(self):
        for p in self._curve_plots:
            self.removeItem(p)
        self._curve_plots.clear()

    def remove_all_scatter_plots(self):
        for p in self._scatter_plots:
            self.removeItem(p)
        self._scatter_plots.clear()


    def setTitleWitDialog(self,value:str=None):
        if value is None:
            text,flag =QInputDialog.getText(None,"Change Title Dialog" ,"Enter new title: ",QLineEdit.Normal,self.titleLabel.text)
            if flag: value=text
        if value is not None:
            self.setTitle(value)


    # region extra infinity lines

    def add_horizontal_infinity_line(self):
        horazontal_line = pg.InfiniteLine(movable=True, angle=0, label='y={value:0.2f}',pen=pg.mkPen((250, 91, 5),width=1) , labelOpts={'position':0.1, 'color': "blue", 'fill': (200,200,200,50), 'movable': True})
        self.addItem(horazontal_line)
        self._infinity_lines.append(horazontal_line)
        
        view_center = self.getViewBox().viewRect().center()
        cx,cy = view_center.x(),view_center.y()
        horazontal_line.setValue(cy)

    def add_vertical_infinity_line(self):
        vertical_line = pg.InfiniteLine(movable=True, angle=90, label='y={value:0.2f}',pen=pg.mkPen((250, 91, 5),width=1) , labelOpts={'position':0.1, 'color': "blue", 'fill': (200,200,200,50), 'movable': True})
        self.addItem(vertical_line)
        self._infinity_lines.append(vertical_line)

        view_center = self.getViewBox().viewRect().center()
        cx,cy = view_center.x(),view_center.y()
        vertical_line.setValue(cx)

    def remove_all_infinity_lines(self):
        for il in self._infinity_lines:
            self.removeItem(il)

    # endregion


    # region labels 

    def add_label(self,txt:str,color="green"):
        if not txt:
            text,flag =QInputDialog.getText(None,"Add a new label" ,"Label: ",QLineEdit.Normal)
            if flag: txt=text
        if color is None:
            color_obj = QColorDialog.getColor()
            color =color_obj.name() if color_obj else None

        if txt and color:
            self.label_group.add_label(txt=txt,color=color)  
    
    def show_label_controller(self)->PQ_LabelsGroup_Controller:
        contl = PQ_LabelsGroup_Controller(self.label_group)
        show_widget(contl)
        return PQ_LabelsGroup_Controller

    # endregion




















































