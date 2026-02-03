
from typing import *
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import  QWidget,QDoubleSpinBox,QSpinBox,QGridLayout , QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtWidgets import  QColorDialog,QPushButton,QComboBox,QInputDialog,QLineEdit,QMessageBox,QSizePolicy
from PyQt5.QtGui import QColor
from model import Slicer_2D
import math
from .labeled_inputs import *

class _SlicedIndexControl_2D(QWidget):
    def __init__(self,slicer:Slicer_2D,scale_index:int,txt:str=None):
        super().__init__()
        ########### private properties ###########
        self.slicer:Slicer_2D=slicer
        self.scale_index:int=scale_index
        self.scale=self.slicer._scales[self.scale_index]

        ########### general layout ###########
        self.layout:QHBoxLayout= QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        #---
        self.label=QLabel()
        self.layout.addWidget(self.label)
        if txt:self.label.setText(txt)
        self.label.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #---
        self.spinbox_index=QSpinBox()
        self.layout.addWidget(self.spinbox_index)
        self.spinbox_index.setPrefix("Index = ")
        self.spinbox_index.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #---
        self.spinbox_value=QDoubleSpinBox()
        self.layout.addWidget(self.spinbox_value)
        self.spinbox_value.setPrefix("Value = ")
        self.spinbox_value.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #---
        self.spinbox_integration=QDoubleSpinBox()
        self.layout.addWidget(self.spinbox_integration)
        self.spinbox_integration.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.spinbox_integration.setPrefix("Integration = ")
        self.spinbox_integration.setSingleStep(1)
        self.spinbox_integration.setRange(0,2147483647)


        self.spinbox_index.valueChanged.connect(self._on_slice_index_spinbox_value_changed)
        self.spinbox_value.valueChanged.connect(self._on_slice_value_spinbox_value_changed)
        self.spinbox_integration.valueChanged.connect(self._on_integration_spinbox_value_changed)
        self.spinbox_index.setMaximum(len(self.scale)-1)
        self.spinbox_index.setMinimum(0)
        self.spinbox_value.setMaximum(self.scale.max())
        self.spinbox_value.setMinimum(self.scale.min())
        self.spinbox_value.setSingleStep((self.scale.max()-self.scale.min())/200)
        self.spinbox_integration.setMaximum(len(self.scale))
        self.spinbox_integration.setMinimum(0)
        self.spinbox_integration.setSingleStep(2)


        self.spinbox_index.valueChanged.connect(lambda :print(f"axis_index= {self.scale_index}"))


    def _on_slice_index_spinbox_value_changed(self):
        axis_index=self.scale_index
        new_value = self.spinbox_index.value()
        old_value = self.slicer._slice_indices[axis_index]
        if new_value != old_value:
            self.slicer.setSliceIndex(axis_index=axis_index,value=int(new_value))

    def _on_slice_value_spinbox_value_changed(self):
        axis_index=self.scale_index
        new_slice_index=Slicer_2D.find_nearest_index(self.slicer._scales[axis_index],self.spinbox_value.value())
        old_slice_index=self.slicer._slice_indices[axis_index]
        if new_slice_index != old_slice_index:
            self.slicer.setSliceIndex(axis_index=axis_index,value=int(new_slice_index))

    def _on_integration_spinbox_value_changed(self):
        axis_index=self.scale_index
        new_value = self.spinbox_integration.value()
        old_value=self.slicer._integration_widths[axis_index]
        if new_value != old_value:
            self.slicer.setIntegrationWidth(axis_index=axis_index,value=int(new_value))



class Slicer_2D_Widget(Slicer_2D,QWidget):
    def __init__(self, data, scale_axises = None, scales_labels = None, viewed_index_0 = 0, viewed_index_1 = 1, slice_indices = None, integration_widths = None):
        QWidget.__init__(self)
        Slicer_2D.__init__(self,data, scale_axises, scales_labels, viewed_index_0,viewed_index_1, slice_indices, integration_widths)
        ########### general layout ###########
        self.layout:QHBoxLayout= QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)


        ########### UI elements ###########

        #----- Viewed Index 0 
        self.viewed_index_0_combobox=Labeled_ComboBox(pre_txt="X :")
        self.viewed_index_0_combobox.combobox.addItems([f"{i} - {v}" for i,v in enumerate(self._scales_labels)])
        self.viewed_index_0_combobox.combobox.currentIndexChanged.connect(self.setViewedIndex_0)
        # self.normalization_combobox.currentTextChanged.connect(self.setNormalizationMode)
        #----- Viewed Index 0 shift
        self.viewed_index_0_shift_labeled_spinbox=Labeled_DoubleSpinBox(pre_txt="+")
        self.viewed_index_0_shift_labeled_spinbox.spinbox.valueChanged.connect(lambda v:self.setShift(self._viewed_index_0,v))
        self.viewed_index_0_shift_labeled_spinbox.spinbox.setMaximum(np.inf)
        self.viewed_index_0_shift_labeled_spinbox.spinbox.setMinimum(-np.inf)


        #----- Viewed Index 1
        self.viewed_index_1_combobox=Labeled_ComboBox(pre_txt="Y :")
        self.viewed_index_1_combobox.combobox.addItems([f"{i} - {v}" for i,v in enumerate(self._scales_labels)])
        self.viewed_index_1_combobox.combobox.currentIndexChanged.connect(self.setViewedIndex_1)
        #----- Viewed Index 1 shift
        self.viewed_index_1_shift_labeled_spinbox=Labeled_DoubleSpinBox(pre_txt="+")
        self.viewed_index_1_shift_labeled_spinbox.spinbox.valueChanged.connect(lambda v:self.setShift(self._viewed_index_1,v))
        self.viewed_index_1_shift_labeled_spinbox.spinbox.setMaximum(np.inf)
        self.viewed_index_1_shift_labeled_spinbox.spinbox.setMinimum(-np.inf)

        
        #----- Sliced Indices
        self.sliced_indices_controls:List[_SlicedIndexControl_2D]=[]
        for i , scl in enumerate(self._scales):
            slc_ctrl = _SlicedIndexControl_2D(slicer=self,scale_index=int(i),txt = self._scales_labels[i])
            self.sliced_indices_controls.append(slc_ctrl)




        # ------- normalization options
        self.normalization_combobox=QComboBox()
        self.normalization_combobox.addItems(self._normalization_options)
        self.normalization_combobox.currentTextChanged.connect(self.setNormalizationMode)

        # ------- event subscription for self data elements
        self.subscribe_to_redraw_needed(lambda _:self._set_ui_elements_values())
        self.subscribe_to_viewed_indices_changed(lambda _:self._set_ui_elements_layout())

        # ------- Initial Actions
        self._set_ui_elements_layout()
        self._set_ui_elements_values()




    # region UI Elements Handling

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            elif item.layout() is not None:
                Slicer_2D_Widget.clear_layout(item.layout())

    # def clear_layout(self):
    #     self.layout.removeWidget()

    def _set_ui_elements_values(self):
        #--- Viewed Indices
        self.viewed_index_0_combobox.combobox.setCurrentIndex(self._viewed_index_0)
        self.viewed_index_1_combobox.combobox.setCurrentIndex(self._viewed_index_1)
        #--- Sliced Indices
        for i,slc_ctrl in enumerate(self.sliced_indices_controls):
            if slc_ctrl.spinbox_index.value() != self._slice_indices[i]:slc_ctrl.spinbox_index.setValue(self._slice_indices[i])
            if slc_ctrl.spinbox_value.value() != self.getSliceValue(i):slc_ctrl.spinbox_value.setValue(self.getSliceValue(i))
            if slc_ctrl.spinbox_integration.value() != self._integration_widths[i]:slc_ctrl.spinbox_integration.setValue(self._integration_widths[i])
        #--- normalization mode
        if self.normalization_combobox.currentText != self._normalization_mode: self.normalization_combobox.setCurrentText(self._normalization_mode)

                
    def _set_ui_elements_layout(self):
        self.clear_layout(self.layout)
        #--- Viewed index
        self.layout.addWidget(self.viewed_index_0_combobox)
        self.layout.addWidget(self.viewed_index_0_shift_labeled_spinbox)
        self.layout.addWidget(self.viewed_index_1_combobox)
        self.layout.addWidget(self.viewed_index_1_shift_labeled_spinbox)
        self.viewed_index_0_shift_labeled_spinbox.spinbox.setSingleStep(abs(self.viewed_scale_0[0] - self.viewed_scale_0[-1])/50)
        self.viewed_index_1_shift_labeled_spinbox.spinbox.setSingleStep(abs(self.viewed_scale_1[0] - self.viewed_scale_1[-1])/50)

        #--- Sliced Controllers
        for i,slc_ctrl in enumerate(self.sliced_indices_controls):
            if (i != self._viewed_index_0) and (i != self._viewed_index_1):
                self.layout.addWidget(slc_ctrl)
        #--- normalization options
        self.layout.addWidget(self.normalization_combobox)




    # endregion