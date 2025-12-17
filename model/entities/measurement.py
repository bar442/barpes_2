from typing import *
import numpy as np
import scipy.optimize as opt
import pathlib
import json
import os
from collections.abc import MutableMapping
import h5py


class Measurement():
    def __init__(self,data:np.ndarray,scales:List[np.ndarray],scales_names:List[str]=None , scales_units:List[str]=None , origin_path:str=None , load_metadata:bool=True):
        self.data=data
        self.dimensions_count=len(data.shape)
        self.origin_path=origin_path

        self.scales=scales
        for i,sc in enumerate(self.scales):
            if self.data.shape[i] != sc.shape[0]:
                raise Exception(f"There is a size mismath scale with index {i}")
            
        
        self.scales_names=scales_names if scales_names else [ f"scale_{i}" for i in range(self.dimensions_count)]
        if len(scales_names)!=self.dimensions_count : raise Exception(f"There is a size between scales_names and dimensions_count")


        self.scales_units=scales_units if scales_units else [ f"" for i in range(self.dimensions_count)]
        if len(scales_units)!=self.dimensions_count : raise Exception(f"There is a size between scales_units and dimensions_count")

        if self.origin_path and load_metadata:
            self.metadata:MeasurementMetadata=MeasurementMetadata.from_measurement_file(self.origin_path)
        else:
            self.metadata:MeasurementMetadata=MeasurementMetadata()

    @classmethod
    def _copy(cls,value:'Measurement'):
        new_inctance = cls(
            data=value.data.copy(),
            scales=[sc.copy() for sc in value.scales],
            scales_units=[su for su in value.scales_units],
            scales_names=[sn for sn in value.scales_names],
            origin_path=value.origin_path,
        )
        return new_inctance
    def copy(self): return self._copy(self)
    
    # region barpes file types mechanism

    def save_to_barpes_file(self,file_path:str=None,metadata_file_path:str=None):
        if not file_path and self.origin_path:
            file_path = str(pathlib.Path(self.origin_path).with_suffix("")) + ".barpes.json"
            
        with h5py.File(file_path, "w") as f:
            # group (like a folder)
            #------------------------> measurement data & metadata
            measurement_group = f.create_group("measurement_001")
            data = measurement_group.create_dataset("data", data=self.data, compression="gzip")
            if self.metadata is None : self.metadata=MeasurementMetadata()
            for k, v in self.metadata.items():
                measurement_group.attrs[k] = v

            
            #------------------------> scales
            scales_group=measurement_group.create_group("scales")
            scales_group.attrs["scales_count"]=len(self.scales)
            # datasets (arrays)
            for i in range(scales_group.attrs["scales_count"]):
                scl = self.scales[i]
                if len(scl)==0 or len(scl)==1 :scl =np.empty((0,), dtype=np.float64)
                scale=scales_group.create_dataset(f"scale_{i}", data=scl, compression="gzip")
                scale.attrs["scale_name"]=self.scales_names[i]
                scale.attrs["scale_unit"]=self.scales_units[i]


        if not metadata_file_path:
            metadata_file_path=MeasurementMetadata._metadata_file_path_from_origin_file_path(file_path)
        self.metadata.save_metadata_file(metadata_file_path=metadata_file_path)

    @classmethod
    def from_barpes_file(cls,file_path:str):
        with h5py.File(file_path, "r") as f:

            #------------------------> measurement data & metadata
            data = np.array(f["measurement_001/data"])
            metadata_object = f["measurement_001"].attrs

            #------------------------> scales
            scales_group=f["measurement_001/scales"]
            scales_count=scales_group.attrs["scales_count"]
            scales = [np.array(scales_group[f"scale_{i}"]) for i in range(scales_count)]
            scales_names = [scales_group[f"scale_{i}"].attrs["scale_name"] for i in range(scales_count)]
            scales_units = [scales_group[f"scale_{i}"].attrs["scale_unit"] for i in range(scales_count)]
            for i in range(scales_count):
                if scales[i].shape[0]==0:scales[i]=np.array([None])


            return cls(data=data,scales=scales,scales_names=scales_names , scales_units=scales_units , origin_path=file_path , load_metadata=True)

    # endregion

    # region Measurement Transformation

    @classmethod
    def _swap_indices_data(cls,self:'Measurement',i:int,j:int):
        data=self.data.swapaxes(i,j)
        
        scales=self.scales.copy()
        scales[i],scales[j]=scales[j],scales[i]
        
        scales_units=self.scales_units.copy()
        scales_units[i],scales_units[j]=scales_units[j],scales_units[i]
        
        scales_names=self.scales_names.copy()
        scales_names[i],scales_names[j]=scales_names[j],scales_names[i]
        
        result = cls(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units,origin_file=self.origin_file,load_metadata=False)
        result.metadata=self.metadata
        return result
    def swap_indices_data(self,i:int,j:int):return self._swap_indices_data(self,i,j)

    @staticmethod
    def _sum_np_array_to_index(arr,index):
        summed_arr=arr.swapaxes(0,index)
        while len(summed_arr.shape)>1:
            summed_arr = np.sum(summed_arr, axis=1)
        return summed_arr


    # endregion



class MeasurementMetadata(MutableMapping):
    def __init__(self,json_object:Dict=None,metadata_file_path:str=None):
        self._metadata =json_object if json_object else {}
        self.metadata_file_path:str=metadata_file_path

    def __getitem__(self, key):
        return self._metadata[key]

    def __setitem__(self, key, value):
        self._metadata[key] = value

    def __delitem__(self, key):
        del self._metadata[key]

    def __iter__(self):
        return iter(self._metadata)

    def __len__(self):
        return len(self._metadata)
    
    @staticmethod
    def _metadata_file_path_from_origin_file_path(data_file_path:str):
        return str(pathlib.Path(data_file_path).with_suffix("")) + ".barpes.json"
    
    @classmethod
    def from_metadata_file(cls,metadata_file_path:str)->'MeasurementMetadata':
        if os.path.isfile(metadata_file_path):
            with open(metadata_file_path, "r", encoding="utf-8") as f:
                metadata_object = json.load(f)
            return MeasurementMetadata(json_object=metadata_object,metadata_file_path=metadata_file_path)
        else :
            return MeasurementMetadata(json_object={},metadata_file_path=metadata_file_path)
        
    @classmethod
    def from_measurement_file(cls,measurement_file_path:str)->'MeasurementMetadata':
        metadata_file_path=cls._metadata_file_path_from_origin_file_path(measurement_file_path)
        return cls.from_metadata_file(metadata_file_path=metadata_file_path)
    
    def save_metadata_file(self,metadata_file_path:str=None):
        if not metadata_file_path and self.metadata_file_path:
            metadata_file_path = self.metadata_file_path 

        with open(metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False, indent=2)


