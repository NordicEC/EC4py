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

from .lsv_data_base import LSV_Data_Base

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data_Load(LSV_Data_Base):
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
   
    #####################################################################################################
    ######################################################################################################
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a LSV

        Args:
            ec_data (EC_Data): the data that should be converted.
        """
        #print("Convert:",kwargs)
        
        ch_E ="E"
        for a in args:
            if a == "IR":
                ch_E = "E-IR"
        options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'IR': 0
        }
        options.update(kwargs)
        sel_channels = EC_Channels(*args,**kwargs)
        try:
            #print("CONVERTING_AAA",len(ec_data.Time), len(ec_data.E), len(ec_data.i))
            self.setup_data = copy.deepcopy(ec_data.setup_data)
            self.convert(ec_data.Time,ec_data.E,ec_data.i,**kwargs)
            self._log = ec_data._log.copy()
            self.log('converter to LSV')

        except ValueError:
            print("no_data")
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return

    #####################################################################################################    
    def convert(self, time, E, i, V0= None, V1 = None, Rate_V_s_ = None, **kwargs):
        """Converts data to a voltammogram, i.e. resampling the data to a evently spaced E.

        Args:
            time (_type_): time
            E (_type_): potential
            i (_type_): current
            direction(str): direction
        """
        x= E
        y= i
        #print("V0:", V0,V1)
        if V0 is None:
            V0, V0_str = extract_value_unit(self.setup['Start'])

        if V1 is None:
            V1, V1_str = extract_value_unit(self.setup['V1'])

        options = plot_options(**kwargs)

        positive_start = False
        positive_start = V0 < V1
        #print("startDIR:", positive_start,V0,V1)

        y = options.smooth_y(y)

        self.xmin = x.min()
        self.xmax = x.max()
        #array of dx
        if(len(x)>10):
            x_div = np.gradient(savgol_filter(x, 10, 1))
        else:
            x_div = np.gradient(x)
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        #print("ZERO:",zero_crossings)
        if Rate_V_s_ is None:
            self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        else:
            self.rate_V_s = Rate_V_s_
        #print(f"Rate: {self.rate_V_s}")
        if(len(zero_crossings)==0):
            zero_crossings =[len(time)-1]
            #print("APPEN DING")
        #E_max = self.E_axis["E_max"]
        #E_min = self.E_axis["E_min"]
        #dE_range = int((E_max - E_min)*1000)
        #x_sweep = np.linspace(E_min, E_max, dE_range) 
        #self.E = x_sweep
        #print("zero_crossings",zero_crossings)
        if positive_start:
            x_sub = x[0:zero_crossings[0]+1]
            y_sub = y[0:zero_crossings[0]+1]
        else:
            x_sub = np.flipud(x[0:zero_crossings[0]+1])
            y_sub = np.flipud(y[0:zero_crossings[0]+1])
        # print(x_sub)
        # print("y\n",y_sub)
        # print("E\n",self.E)
        y_pos = self.interpolate(x_sub, y_sub)
        # print("y_pos",y_pos)
        #y_pos=np.interp(x_sweep, x_sub, y_sub)
        self.i = self.clean_up_edges(y_pos)
        # print("i_pos",self.i)
        

