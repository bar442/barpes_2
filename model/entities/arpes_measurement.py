from typing import *
import numpy as np
import scipy.optimize as opt
import pathlib
import json
import os
from .measurement import Measurement , MeasurementMetadata



class ARPES_Measurement(Measurement):

    _Ef_key="fermi_energy"
    @property
    def Ef(self)->float: return self.metadata[self._Ef_key] if self._Ef_key in self.metadata.keys() else None
    @Ef.setter
    def Ef(self,value:float):self.metadata[self._Ef_key]=value

    _y_scale_correction_key="Y_scale_correction"
    @property
    def y_scale_correction(self)->float: return self.metadata[self._y_scale_correction_key] if self._y_scale_correction_key in self.metadata.keys() else None
    @y_scale_correction.setter
    def y_scale_correction(self,value:float):self.metadata[self._y_scale_correction_key]=value

    _hv_key="photon_energy"
    @property
    def photon_energy(self)->float: return self.metadata[self._hv_key] if self._hv_key in self.metadata.keys() else None
    @photon_energy.setter
    def photon_energy(self,value:float):self.metadata[self._hv_key]=value
    @property
    def hv(self)->float: return self.metadata[self._hv_key] if self._hv_key in self.metadata.keys() else None
    @photon_energy.setter
    def hv(self,value:float):self.metadata[self._hv_key]=value


    # region getter functions

    def get_energy_scale_index(self)->int:
        for i,name in enumerate(self.scales_names):
            if "Energy" in name or "energ" in name:
                return i
        raise Exception("cannot find Energy scale index")

    def get_emmission_angle_scale_index(self)->int:
        for i,name in enumerate(self.scales_names):
            if "Y-Scale" in name:
                return i
        raise Exception("cannot find emmission angle scale index")
    

    # endregion
