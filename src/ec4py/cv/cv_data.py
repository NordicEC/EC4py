""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
from typing import Self
import numbers
import math
import numpy as np
# from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from ..ec_data.ec_data import EC_Data
from ..ec_util import EC_Channels

from .cv_data_analysis import CV_Data_Analysis


from ..lsv.lsv_data import LSV_Data
from ..util import Quantity_Value_Unit as QV


from ..util import extract_value_unit     
from ..util import Quantity_Value_Unit as QV
from ..method_util.util_voltammetry import Voltammetry,create_Tafel_data_analysis_plot,POS,NEG,AVG,DIF,find_vertex
#from .method_util.util_voltammetry import OFFSET_AT_E_MIN, OFFSET_AT_E_MAX, OFFSET_LINE

from ..method_util.util_data import get_IR
from ..util_graph import plot_options, saveFig, should_plot_be_made,ANALYSE_PLOT,DATA_PLOT
#from .analysis import diffusion_limit_corr

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"


class CV_Data(CV_Data_Analysis):
    """# Class to analyze a single CV data. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.
    
    ### iR- Correction
    - add keyword IRCORR = "R" for using the real-part of the impedance
    - add keyword IRCORR = "Rmed" for using the median real-part of the impedance
    - add keyword IRCORR = "Z" for using the absolute impedance
    - add keyword IRCORR = "Zmed" for using the median absolute impedance
    - add keyword IRCORR = 1.0 for manual ir compensation
    
    ### Analysis: 
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "in" where n is a number to select another current channel, ex. "i2"
    "pn" where n is a number to select another potentiostat group, ex. "P2"
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """


    def __init__(self,*args, **kwargs):
        #EC_Setup.__init__(self,*args, **kwargs)
        super().__init__(*args, **kwargs)
        # self.E=[]
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]), *args, **kwargs)
    #########################################  
    
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero and adjust the rest of the current.

        Args:
            E (float): potential where to set the current to zero.
        """
        new_data = copy.deepcopy(self)
        new_data.set_active_RE(args)
        current = new_data.get_i_at_E(E,*args,**kwargs)
        self.sub(current)
    
     
    def smooth(self, smooth_width:int):
        try:
            self.i_p = self._smooth(self.i_p,smooth_width)
            self.i_n = self._smooth(self.i_n,smooth_width)      
        finally:
            return

     
   ######################################################################################### 
    def norm(self, norm_to:str|tuple):
        """Normalise the current to certain factors. 

        Args:
            norm_to (str | tuple): _description_
        """
        r = Voltammetry._norm_list(self, norm_to,[self.i_p,self.i_n ] )
        #n = Voltammetry.norm(self, norm_to,self.i_n )
        if r is not None:
            v= r[0]
            self.i_p = np.asarray(v[0],dtype=np.float64)
            self.i_n = np.asarray(v[1],dtype=np.float64)
            
        return
    ###############################
    ###under deve
    '''
    def set_active_RE(self,shift_to:str|tuple = ""):
        # end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        a = self._set_active_RE(shift_to, [self.i_p, self.i_n])
        if a is not None:
            a,b = a
            self.i_p = np.asarray(b[0],dtype=np.float64)
            self.i_n = np.asarray(b[1],dtype=np.float64)
            # print("pot_shift",a, "REEE",self.E_label)
        return 
    '''
 