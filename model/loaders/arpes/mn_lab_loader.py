from typing import *
import h5py
import numpy as np
import sys
from ...entities import ARPES_Measurement
import re
import erlab
# import erlab.interactive as eri


def _extract_substring(text:str,regex:str)->str:
    match_object = re.search(regex, text)
    if match_object == None:
        return None
    else:
        return match_object.group()
    

def load_data_from_MNlab_txt_file(file_path:str)->ARPES_Measurement:
    data:np.ndarray
    scales:List[np.ndarray]=[None,None,None]
    scales_units:List[str]=["","",""]
    scales_names:List[str]=["","",""]
    
    
    # region ---> spliting the text file to it most general areas
    gnrl_info_txt,region_txt,info_txt,run_mode_txt=[],[],[],[]
    data_txt:Dict[str,List[str]]={}
    t_stdo:List[str]
    with open(file_path) as file:
        for line in file:
            if line.startswith("[Info]"):t_stdo=gnrl_info_txt
            elif line.startswith("[Region 1]"):t_stdo=region_txt
            elif line.startswith("[Info 1]"):t_stdo=info_txt
            elif line.startswith("[Run Mode Information 1]"):t_stdo=run_mode_txt
            elif line.startswith("[Data 1"):
                key=line.rstrip().removesuffix(r'\n')
                data_txt[key]=[]
                t_stdo=data_txt[key]
                continue
            elif not line.strip():continue
            t_stdo.append(line)
    # endregion
    
    # region ---> process dimensions
    for line in region_txt:
        if line.startswith("Dimension") and isinstance(line,str):
            dimension_index=int(line.split(" ")[1])
            if dimension_index < 1 or  3<dimension_index:
                raise Exception(f"dimension index is out of range: index = {dimension_index}")
            dimension_index -= 1
            
            tag,value=line.split('=')
            arg_name=tag.split(" ")[2]
            if arg_name=='name':
                scales_names[dimension_index]=str(value).removesuffix(r'\n')
                scales_units[dimension_index]=_extract_substring(str(value),"(?<=\[).*(?=\])")
            elif arg_name=='scale':scales[dimension_index]=np.array([float(v) for v in value.split(" ")])
            elif arg_name=='size':continue
            else:
                raise Exception("unrecognized dimension value") 
    if scales[2] is None:
        del scales[2]
        del scales_units[2]
        del scales_names[2]
    # endregion
    
    # region ---> process data 
    data=np.zeros(shape=[len(scl) for scl in scales])
    dimensions_count=len(data.shape)
    
    for k,frame_cuple in enumerate( data_txt.items()):
        frame_key,frame_table=frame_cuple
        data_rows=[line for line in frame_table if isinstance(line,str)]
        for i,line in enumerate(data_rows):
            col_entries=[v for v in line.strip().rstrip().split("  ")][1:]
            for j,val in enumerate(col_entries):
                if dimensions_count == 3:
                    data[i,j,k]=float(val)
                elif dimensions_count == 2:
                    data[i,j]=float(val)
                else :
                    raise Exception(f"load_data_from_MNlab_txt_file get file with dimensions_count={dimensions_count} | can only deal with 2 or 3  dimensions")

    
    # endregion
    
    return ARPES_Measurement(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units, origin_path= file_path)


def load_data_from_MNlab_h5_file(file_path:str)->ARPES_Measurement:
    data:np.ndarray
    scales:List[np.ndarray]=[None,None,None]
    scales_units:List[str]=["","",""]
    scales_names:List[str]=["","",""]
    
    # region ---> loadin h5 file
    h5_file = h5py.File(file_path, 'r')
    h5_data = h5_file['Electron Analyzer/Image Data']
    data_attributes = h5_data.attrs
    data_shape=h5_data.shape
    is_3d_data=len(data_shape)==3
    # endregion
    
    # region ---> process dimensions
    axis_indexes=[0,1,2] if is_3d_data else [0,1]
    for ai in axis_indexes:
        start_value,step_size=data_attributes[f'Axis{str(ai)}.Scale']
        dim_size=data_shape[ai]
        scale=np.linspace(start_value,start_value+dim_size*step_size,dim_size)
        # if ai ==2 :
        #     scale.reverse()
        name=data_attributes[f'Axis{str(ai)}.Description']
        unit=data_attributes[f'Axis{str(ai)}.Units']
        scales[ai]=scale
        scales_names[ai]=name
        scales_units[ai]=unit
        
    if not is_3d_data:
        del scales[2]
        del scales_units[2]
        del scales_names[2]
    # endregion
    
    # region ---> process data
    dimensions_count=len(data_shape)
    if dimensions_count==3:
        # data=np.array(h5_data)
        data=np.zeros(shape=data_shape)
        print("                                            ")
        for i,frame in enumerate(h5_data):
            data[i]=frame
            prec=round(((i+1)/data_shape[0])*100)
            sys.stdout.write("\r")
            sys.stdout.write(f'loading h5 file {prec}%                     ')
            sys.stdout.flush()
        # data=np.swapaxes(data,0,2)
        # data=np.swapaxes(data,1,2)
        data=np.flip(data,axis=0)
        
    elif dimensions_count==2:
        data=np.array(h5_data)
    else :
        raise Exception(f"load_data_from_MNlab_h5_file get file with dimensions_count={dimensions_count} | can only deal with 2 or 3  dimensions")
        
    # endregion
    
    return ARPES_Measurement(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units, origin_path= file_path)
    







def load_data_from_MNlab_deflection_file(file_path:str)->ARPES_Measurement:
    loader = erlab.io.loaders["da30"]
    xdata=loader.load(file_path)

    scales_names=xdata.dims # ('beta', 'alpha', 'eV') temporary we shell rewrite them=
    scales_names=["Point [Â°]","Y-Scale [deg]","Kinetic Energy [eV]"] # wanted
    scales_units=["","",""]

    scales:List[np.ndarray]=[xdata.coords["beta"].to_numpy(),xdata.coords["alpha"].to_numpy(),xdata.coords["eV"].to_numpy()]

    data=xdata.to_numpy()


    return ARPES_Measurement(data=data,scales=scales,scales_names=scales_names,scales_units=scales_units , origin_path= file_path)






































