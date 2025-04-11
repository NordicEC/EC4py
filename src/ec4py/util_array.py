""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x, ANALYSE_PLOT, DATA_PLOT,NO_PLOT





class EC_Array_class:
    """
    Class for handling arrays of data. 
    
    This class is used to handle arrays of data and perform operations on them.
    """
    def __init__(self):
        self.datas= []
        
    def __len__(self):
        return len(self.datas)
    
    def __getitem__(self, index):
        return self.datas[index]    
    
    def __setitem__(self, index, value):    
        self.datas[index] = value   
        
    def __delitem__(self, index):
        del self.datas[index]   
        
    def __iter__(self):
        return iter(self.datas)
    
    def __contains__(self, item):
        return item in self.datas   
    
    def __str__(self):
        return "string rep of class to be made"
    
    def __repr__(self):
        delimiter = "','"
        r =delimiter.join([x.setup_data.fileName for x in self.datas])
        return f"{self.__class__.__name__}([{r}])"
    
    def pop(self,index):
        """_summary_
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range
        """
        self.datas.pop(index)
        
    def append(self, item):
        """_summary_
        Append an item to the array.
        """
        self.datas.append(item)
        
        



