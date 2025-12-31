from typing import *
import numpy as np
from ..entities import Measurement
import math


class Slicer_1D():
    def __init__(self,data:np.ndarray , 
                scale_axises:List[np.ndarray]=None ,
                scales_labels:List[str]=None,
                viewed_index:int=0 ,slice_indices:List[int] = None,
                integration_widths:List[int] = None ):
        # -----------> data elements
        self._data:np.ndarray=data
        self._scales:List[np.ndarray]=scale_axises if scale_axises else [np.array(range(scl_size)) for scl_size in self._data.shape]
        self._scales_labels:List[str]=scales_labels if scales_labels else ["" for scl_size in self._data.shape]


        # -----------> conceptional elements
        self._ys:np.ndarray=None
        self._viewed_index:int=viewed_index
        self._slice_indices:List[int] = slice_indices if slice_indices else [0 for i in range(len(self._data.shape))]
        self._integration_widths:List[int] = integration_widths if integration_widths else [0 for i in range(len(self._data.shape))]
        self._normalization_options:List[str]=["no normalization","area normalization","height normalization"]
        self._normalization_mode:str = "no normalization"

        # -----------> Events & Subscriptions 
        self._subscribers_to_redraw_needed:List[Callable[[Slicer_1D], None]]=[]
        self._subscribers_to_viewed_index_changed:List[Callable[[Slicer_1D], None]]=[]


    # region Main Properties

    @property
    def xs(self)->np.ndarray:
        return self._scales[self._viewed_index]

    @property
    def ys(self)->np.ndarray:
        slicer_list = []
        for dim_i in range(self._data.shape):
            if dim_i == self._viewed_index:
                slicer_list.append(slice(None))
            else:
                start_j= self._slice_indices[dim_i] - int(math.floor(self._integration_widths[dim_i]/2))
                finish_j= self._slice_indices[dim_i] + int(math.floor(self._integration_widths[dim_i]/2))
                if start_j < 0: start_j=0
                if finish_j > self._data.shape[dim_i] : finish_j=self._data.shape[dim_i]-1
                slicer_list.append(slice(start_j,finish_j))
        result = np.sum(self._data[(sl for sl in slicer_list)], axis=dim_i)

        if self._normalization_mode == "area normalization":
            result = result/result.sum()  
        elif self._normalization_mode == "height normalization":
            result = result/result.max()  

        return result

    # endregion



    # region getter functions
    def get_xs(self): return self.xs
    def get_ys(self): return self.ys

    @staticmethod
    def find_nearest_index(arr:np.ndarray,v:float): return int((np.abs(np.asarray(arr) - v)).argmin())

    def getSliceValue(self,axis_index:int)->float:
        return self._scales[axis_index][self._slice_indices[axis_index]] 
    
    def getAllSliceValues(self)->List[float]:
        return [self.getSliceValue(i) for i in range(len(self._data.shape))]
    
    
    # endregion

    # region Setter functions
    def setViewedIndex(self,value:int):
        if self._viewed_index != value:
            self._viewed_index=value
            self.emit_viewed_index_changed()
            self.emit_redraw_needed()


    def setSliceIndex(self,axis_index:int,value:int):
        ai=axis_index
        if axis_index > len(self._scales):raise Exception("axis_index out of range")
        if value > len(self._scales[ai]):raise Exception("value out of range")
        if self._slice_indices[ai] == value: return

        self._slice_indices[ai] = value
        self.emit_redraw_needed()

    def setAllSliceIndices(self,values:List[int]):
        for ai,v in enumerate(values):
            if ai > len(self._scales):raise Exception("axis_index out of range")
            if v > len(self._scales[ai]):raise Exception("value out of range")
        self._slice_indices=values
        self.emit_redraw_needed()

    def setSliceValue(self,axis_index:int,value:float , drop_value_change_emission:bool=False):
        if axis_index > len(self._scales):raise Exception("axis_index out of range")
        value_index =  self.find_nearest_index(self._scales[axis_index],value)
        if value_index != self._slice_indices[axis_index]:
            self._slice_indices[axis_index]=value
            if not drop_value_change_emission:
                self.emit_redraw_needed()

    def setAllSliceValues(self,values:List[float] , drop_value_change_emission:bool=False):
        for ai,v in enumerate(values):
            if ai > len(self._scales):raise Exception("axis_index out of range")
            self.setSliceValue(axis_index=ai,value=v,drop_value_change_emission=True)
        if not drop_value_change_emission:
            self.emit_redraw_needed()

    def setIntegrationWidth(self,axis_index:int,value:int):
        if axis_index > len(self._scales):raise Exception("axis_index out of range")
        if value != self._integration_widths[axis_index]:
            self._integration_widths[axis_index]=value
            self.emit_redraw_needed()

    def setAllIntegrationWidths(self,values:List[int]):
        for ai,v in enumerate(values):
            if ai > len(self._scales):raise Exception("axis_index out of range")

        self._integration_widths=values
        self.emit_redraw_needed()

    def setNormalizationMode(self,mode:str):
        if mode != self._normalization_mode and mode in self._normalization_options:
            self._normalization_mode = mode
            self.emit_redraw_needed()

    # endregion

    # region Events & Subscriptions 

    def emit_redraw_needed(self):
        for f in self._subscribers_to_redraw_needed:
            f(self)
    def subscribe_to_redraw_needed(self,func:Callable[['Slicer_1D'], None]):
        self._subscribers_to_redraw_needed.append(func)

    def emit_viewed_index_changed(self):
        for f in self._subscribers_to_viewed_index_changed:
            f(self)
    def subscribe_to_viewed_index_changed(self,func:Callable[['Slicer_1D'], None]):
        self._subscribers_to_viewed_index_changed.append(func)

    # endregion





