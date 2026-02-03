
from typing import *
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import  QWidget,QDoubleSpinBox,QSpinBox,QGridLayout , QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtWidgets import  QColorDialog,QPushButton,QComboBox,QInputDialog,QLineEdit,QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSizePolicy
from model import Slicer_1D
import math
from .labeled_inputs import *


class _SlicedIndexControl(QWidget):
    def __init__(self,txt:str=None):
        super().__init__()
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

class Slicer_1D_Widget(Slicer_1D,QWidget):
    def __init__(self, data, scale_axises = None, scales_labels = None, viewed_index = 0, slice_indices = None, integration_widths = None):
        super().__init__(data, scale_axises, scales_labels, viewed_index, slice_indices, integration_widths)

        ########### general layout ###########
        self.layout:QVBoxLayout= QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)


        ########### UI elements ###########
        #----- curve
        self.curve=pg.PlotCurveItem(pen=pg.mkPen("red", width=1))
        #----- infinity line
        self.infinity_line = pg.InfiniteLine(movable=True, angle=0, label='v={value:0.2f}',pen=pg.mkPen((250, 91, 5),width=1),labelOpts={'movable': True})
        self.infinity_line.sigPositionChanged.connect(self._on_infinity_line_value_changed)

        #----- Viewed Index
        self.viewed_index_l_combobox=Labeled_ComboBox(pre_txt="Viewed :")
        self.viewed_index_l_combobox.combobox.addItems([f"{i} - {v}" for i,v in enumerate(self._scales_labels)])
        self.viewed_index_l_combobox.combobox.currentIndexChanged(self.setViewedIndex)
        # self.normalization_combobox.currentTextChanged.connect(self.setNormalizationMode)

        #----- Sliced Indices
        self.sliced_indices_controls:List[_SlicedIndexControl]=[]
        for i , scl in enumerate(self._scales):
            slc_ctrl = _SlicedIndexControl(self._scales_labels[i])
            self.sliced_indices_controls.append(slc_ctrl)
            slc_ctrl.spinbox_index.valueChanged.connect(lambda :self._on_slice_index_spinbox_value_changed(axis_index=i))
            slc_ctrl.spinbox_value.valueChanged.connect(lambda :self._on_slice_value_spinbox_value_changed(axis_index=i))
            slc_ctrl.spinbox_integration.valueChanged.connect(lambda :self._on_integration_spinbox_value_changed(axis_index=i))

        # ------- normalization options
        self.normalization_combobox=QComboBox()
        self.normalization_combobox.addItems(self._normalization_options)
        self.normalization_combobox.currentTextChanged.connect(self.setNormalizationMode)

        # ------- color button
        self.curve_color_button=QPushButton()
        self.curve_color_button.setFixedSize(20, 20)
        self.curve_color_button.setStyleSheet("background-color: red; color: white;")
        self.curve_color_button.clicked.connect(lambda :self.set_curve_color())



        # ------- event subscription for self data elements
        self.subscribe_to_redraw_needed(self._set_ui_elements_values)
        self.subscribe_to_viewed_index_changed(self._set_ui_elements_layout)

        # ------- Initial Actions
        self._set_ui_elements_layout()
        self._set_ui_elements_values()

    # region Setter functions

    def set_curve_color(self,color=None):
        if color is None:
            color_obj = QColorDialog.getColor()
            color =color_obj.name() if color_obj else None
        if color:
            self.curve.setPen(pg.mkPen(color, width=1))
            self.curve_color_button.setStyleSheet(f"background-color: {color}; color: white;")

    # endregion


    # region UI Elements Handling
    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            elif item.layout() is not None:
                Slicer_1D_Widget.clear_layout(item.layout())

    def _set_ui_elements_values(self):
        #--- curve data
        self.curve.setData(x=self.xs,y=self.ys)
        #--- Sliced Indices
        for i,slc_ctrl in enumerate(self.sliced_indices_controls):
            if slc_ctrl.spinbox_index.value() != self._slice_indices[i]:slc_ctrl.spinbox_index.setValue(self._slice_indices[i])
            if slc_ctrl.spinbox_value.value() != self.getSliceValue(i):slc_ctrl.spinbox_value.setValue(self.getSliceValue(i))
            if slc_ctrl.spinbox_integration.value() != self._integration_widths[i]:slc_ctrl.spinbox_integration.setValue(self._integration_widths[i])
        #--- normalization mode
        if self.normalization_combobox.currentText != self._normalization_mode: self.normalization_combobox.setCurrentText(self._normalization_mode)

                
    def _set_ui_elements_layout(self):
        self.clear_layout()
        #--- color button
        self.layout.addWidget(self.curve_color_button)
        #--- Viewed index
        self.layout.addWidget(self.viewed_index_l_combobox)
        #--- Sliced Controllers
        for i,slc_ctrl in enumerate(self.sliced_indices_controls):
            if i != self._viewed_index:
                self.layout.addWidget(slc_ctrl)
        #--- normalization options
        self.layout.addWidget(self.normalization_combobox)



    # def _setUIElements(self):
    #     #----- Sliced Indices
    #     self.clear_layout()

    def _on_infinity_line_value_changed(self):
        value=self.infinity_line.value()
        slice_value = self.getSliceValue()
        if value != slice_value:
            self.setSliceValue(value)

    def _on_slice_index_spinbox_value_changed(self,axis_index:int):
        new_value = self.sliced_indices_controls[axis_index].spinbox_index.value()
        old_value = self._slice_indices[axis_index]
        if new_value != old_value:
            self.setSliceIndex(axis_index=axis_index,value=int(new_value))

    def _on_slice_value_spinbox_value_changed(self,axis_index:int):
        new_slice_index=self.find_nearest_index(self._scales[axis_index],self.sliced_indices_controls[axis_index].spinbox_value.value())
        old_slice_index=self._slice_indices[axis_index]
        if new_slice_index != old_slice_index:
            self.setSliceIndex(axis_index=axis_index,value=int(new_slice_index))

    def _on_integration_spinbox_value_changed(self,axis_index:int):
        new_value = self.sliced_indices_controls[axis_index].spinbox_integration.value()
        old_value=self._integration_widths[axis_index]
        if new_value != old_value:
            self.setIntegrationWidth(axis_index=axis_index,value=int(new_value))


    # endregion