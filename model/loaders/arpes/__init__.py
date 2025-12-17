from ...entities import ARPES_Measurement
from .alba_nxs_loader import load_data_from_ALBA_nxs_file
from .mn_lab_loader import load_data_from_MNlab_txt_file,load_data_from_MNlab_deflection_file,load_data_from_MNlab_h5_file






def load_ARPES_data(file_path:str)->ARPES_Measurement:
    file_path_lower=file_path.lower()
    if file_path_lower.endswith(r".txt"): return load_data_from_MNlab_txt_file(file_path)
    elif file_path_lower.endswith(r".h5"): return load_data_from_MNlab_h5_file(file_path)
    elif file_path_lower.endswith(r".zip"): return load_data_from_MNlab_deflection_file(file_path)
    elif file_path_lower.endswith(r".nxs"): return load_data_from_ALBA_nxs_file(file_path)
    elif file_path_lower.endswith(r".barpes"): return ARPES_Measurement.from_barpes_file(file_path)
    else : raise Exception(f"load_ARPES_data got unknown suffix from path: {file_path}")