from typing import *
import h5py
import numpy as np
import sys
from ...entities import ARPES_Measurement







def load_data_from_ALBA_nxs_file(file_path:str, load_metadata:bool=True)->ARPES_Measurement:

    data:np.ndarray
    scales:List[np.ndarray]=[]
    scales_units:List[str]=[]
    scales_names:List[str]=[]
    
    # region ---> loadin h5 file
    h5_file = h5py.File(file_path, 'r')
    h5_data = h5_file['entry1/data']
    data_attributes = h5_data.attrs
    data_shape=h5_data['data'].shape
    dimensions_count=len(data_shape)
    # endregion

    # region ---> process dimensions
    for ai in range(dimensions_count):
        name=data_attributes["axes"][ai]
        scales.append(np.array(h5_data[name]))
        scales_names.append(name)
        scales_units.append("unknown")

    # endregion

    # region ---> process data
    if dimensions_count==2:
        data=np.array(h5_data['data'])
    elif dimensions_count==3:
        data=np.zeros(shape=data_shape)
        for i,frame in enumerate(h5_data['data']):
            data[i]=np.array(frame)
            prec=round(((i+1)/data_shape[0])*100)
            sys.stdout.write("\r")
            sys.stdout.write(f'loading h5 file {prec}%                     ')
            sys.stdout.flush()
    else:
        raise Exception(f"load_data_from_ALBA_nxs_file get file with dimensions_count={dimensions_count} | can only deal with 2 or 3  dimensions")
        
    # endregion

    # region ---> Renaming Scales
    for i,n in enumerate(scales_names):
        if n=="energies": scales_names[i]="Energy"
        elif n=="angles": scales_names[i]="Y-Scale"
        elif n=="defl_angles": scales_names[i]="Polar"

    # endregion

    result = ARPES_Measurement(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units , origin_path= file_path,load_metadata=load_metadata)
    return result









