""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations

import copy
import math

import numpy as np
import pandas as pd
# from scipy import integrate
from scipy.signal import savgol_filter

from ..analysis.analysis_levich import diffusion_limit_corr
from ..analysis.analysis_tafel import Tafel
from ..ec_data.ec_data import EC_Data
from ..ec_util.ec_data_util import EC_Channels
from ..method_util.util_voltammetry import Voltammetry, create_Tafel_data_analysis_plot  # pyright: ignore[reportAttributeAccessIssue]
from ..util import Quantity_Value_Unit as QV
from ..util import extract_value_unit
from ..util_graph import plot_options, should_plot_be_made


from .lsv_data_analysis import LSV_Data_Analysis
STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data(LSV_Data_Analysis):
    """# Class to analyze a single LS data, linear sweep. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.
    
    ### Analysis: 
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """


    def __init__(self,*args, **kwargs):
        super().__init__()
        self.i=np.array([], dtype=np.float64)
       # self.i_label = "i"
       # self.i_unit = "A"
       # print(self.i_label)
        self.rate_V_s = 1

        """max voltage"""
        #self.E_max = 2.5 
        #self.E_min = -2.5
        """min voltage"""
        ##self.name="CV" name is given in the setup.
        self.xmin = -2.5
        self.xmax = 2.5
        if not args:
            self.log(type(self).__name__)
            return
        else:
            #print(kwargs)
            if str(type(args[0]).__name__)=='LSV_Data':
                #print('recreate')
                self.setup_data = copy.deepcopy(args[0].setup_data)
                self.E = np.asarray(copy.deepcopy(args[0].E),dtype=np.float64)
                self.i = np.asarray(copy.deepcopy(args[0].i),dtype=np.float64)
                self.copy_from(args[0])
               

            else:
            #else:
                self.conv(EC_Data(args[0]),*args, **kwargs)
  
   
   