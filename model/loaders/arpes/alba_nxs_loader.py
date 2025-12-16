from typing import *
import h5py
import numpy as np
import sys
from ...entities import ARPES_Measurement







def load_data_from_ALBA_nxs_file(file_path:str, load_metadata:bool=True)->ARPES_Measurement:

    data:np.ndarray
    scales:List[np.ndarray]=[None,None,None]
    scales_units:List[str]=["","",""]
    scales_names:List[str]=["","",""]
    
    # region ---> loadin h5 file
    h5_file = h5py.File(file_path, 'r')
    h5_data = h5_file['entry1/data']
    data_attributes = h5_data.attrs
    data_shape=h5_data['data'].shape
    is_3d_data=len(data_shape)==3
    # endregion

    # region ---> process dimensions
    axis_indexes=[0,1,2] if is_3d_data else [0,1]
    for ai in axis_indexes:
        # name=data_attributes["axes"][ai].decode("utf-8")
        name=data_attributes["axes"][ai]
        # name=str(data_attributes["axes"][ai])
        unit="unknown"
        scales[ai]=np.array(h5_data[name])
        scales_names[ai]=name
        scales_units[ai]=unit
        
    if not is_3d_data:
        scales[2]=np.array([None])
        scales_names[2]=""
    # endregion

    # region ---> process data
    if is_3d_data:
        # data=np.array(h5_data)
        data=np.zeros(shape=data_shape)
        print("                                            ")
        # for i in range(data_shape[0]):
        #     for j in range(data_shape[1]):
        #         for k in range(data_shape[2]):
        #             data[i]=float(h5_data['data'][i][j][k])
        #     prec=round(((i+1)/data_shape[0])*100)
        #     sys.stdout.write("\r")
        #     sys.stdout.write(f'loading h5 file {prec}%                     ')
        #     sys.stdout.flush()
        for i,frame in enumerate(h5_data['data']):
            data[i]=np.array(frame)
            prec=round(((i+1)/data_shape[0])*100)
            sys.stdout.write("\r")
            sys.stdout.write(f'loading h5 file {prec}%                     ')
            sys.stdout.flush()
        # data=np.flip(data,axis=0)
        
    else:
        data=np.expand_dims(h5_data['data'],axis=2)
        
    # endregion

    # region ---> Renaming Scales
    if is_3d_data:
        for i,n in enumerate(scales_names):
            if n=="energies": scales_names[i]="Energy"
            elif n=="angles": scales_names[i]="Y-Scale"
            elif n=="defl_angles": scales_names[i]="Polar"
    else:
        for i,n in enumerate(scales_names):
            if n=="energies": scales_names[i]="Energy"
            elif n=="angles": scales_names[i]="Y-Scale"
    # endregion

    result = ARPES_Measurement(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units , origin_path= file_path,load_metadata=load_metadata)
    return result
