"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from .ec_data_base      import EC_Data_Base
from .ec_data_util      import EC_Channels



__all__ = ["EC_Data_Base", 
           "EC_Channels",
            ]