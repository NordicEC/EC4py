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


class CV_Data_Base(Voltammetry):
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
        self.i_p=np.array([], dtype=np.float64)
        self.i_n=np.array([], dtype=np.float64)
 
    #########################################  
    
    def __repr__(self):
        """Get the name of the data file.
        """
        return f"CV_Data('{self.setup_data.fileName}')"
    
       
    def __add__(self, other: Self|LSV_Data|QV|float|str|list)-> Self:
        """_summary_

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Data: returns a copy of the inital dataset. 
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.add(other)
        return new_cv   
    
    def __sub__(self, other: Self|LSV_Data|QV|float|str|list) -> Self:
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.sub(other)
        return new_cv
    
    def __mul__(self, other: Self|float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() #copy.deepcopy(self)
        new_cv.mul(other)
        return new_cv
    #############################################################################
    def __truediv__(self, other: Self|LSV_Data|QV|float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.div(other)
        return new_cv
    #############################################################################   
    #####################################################################################################
    def add(self, other: Self|LSV_Data|QV|float|str|list[float|QV]):
        """_summary_

        Args:
            other (CV_Data): Add something to the current of the CV_Data.

        Raises:
            ValueError: _description_
            TypeError: _description_
        """
        if isinstance(other, CV_Data_Base):
            self.i_p = np.asarray(self.i_p + other.i_p,dtype=np.float64)
            self.i_n = np.asarray(self.i_n + other.i_n,dtype=np.float64)
        elif isinstance(other, LSV_Data):
            self.i_p = np.asarray(self.i_p + other.i,dtype=np.float64)
            self.i_n = np.asarray(self.i_n + other.i,dtype=np.float64)
        elif isinstance(other, QV):
            self.i_p = np.asarray(self.i_p + other.value,dtype=np.float64)
            self.i_n = np.asarray(self.i_n + other.value,dtype=np.float64)
        elif isinstance(other, str):
            self.i_p = np.asarray(self.i_p + float(other),dtype=np.float64)
            self.i_n = np.asarray(self.i_n + float(other),dtype=np.float64)
        elif isinstance(other, list):
            if len(other) == 2:
                self.i_p = np.asarray(self.i_p + float(other[0]),dtype=np.float64)
                self.i_n = np.asarray(self.i_n + float(other[1]),dtype=np.float64)
            else:
                raise ValueError("List must have length 2")
        elif isinstance(other, numbers.Real) or isinstance(other, int):
            self.i_p = np.asarray(self.i_p + other,dtype=np.float64)
            self.i_n = np.asarray(self.i_n + other,dtype=np.float64)
        else:
            raise TypeError("Unsupported type for subtraction")
        

    #####################################################################################################   
    
    
    def sub(self, other: Self|LSV_Data|QV|str|list|float) -> None:
        if isinstance(other, CV_Data_Base):
            self.i_p = np.asarray(self.i_p - other.i_p,dtype=np.float64)
            self.i_n = np.asarray(self.i_n - other.i_n,dtype=np.float64)
        elif isinstance(other, LSV_Data):
            self.i_p = np.asarray(self.i_p - other.i,dtype=np.float64)
            self.i_n = np.asarray(self.i_n - other.i,dtype=np.float64)
        elif isinstance(other, QV):
            self.i_p = np.asarray(self.i_p - other.value,dtype=np.float64)
            self.i_n = np.asarray(self.i_n - other.value,dtype=np.float64)
        elif isinstance(other, str):
            self.i_p = np.asarray(self.i_p - float(other),dtype=np.float64)
            self.i_n = np.asarray(self.i_n - float(other),dtype=np.float64)
        elif isinstance(other, list):
            if len(other) == 2:
                self.i_p = np.asarray(self.i_p - float(other[0]),dtype=np.float64)
                self.i_n = np.asarray(self.i_n - float(other[1]),dtype=np.float64)
            else:
                raise ValueError("List must have length 2")
        elif isinstance(other, numbers.Real) or isinstance(other, int):
           # print("AAA",other)
            self.i_p = np.asarray(self.i_p - other,dtype=np.float64)
            self.i_n = np.asarray(self.i_n - other,dtype=np.float64)
        else:
            raise TypeError("Unsupported type for subtraction")
        
    #############################################################################
    
    def mul(self, mul_factor:Self|LSV_Data|float|QV):
        """divide the current by a factor.
        Args:
            div_factor (float): div the current dataset with the factor.
        """
        if isinstance(mul_factor, CV_Data_Base):
            self.i_p = np.asarray(self.i_p * mul_factor.i_p,dtype=np.float64)
            self.i_n = np.asarray(self.i_n * mul_factor.i_n,dtype=np.float64)
        elif isinstance(mul_factor, LSV_Data):
            self.i_p = np.asarray(self.i_p * mul_factor.i,dtype=np.float64)
            self.i_n = np.asarray(self.i_n * mul_factor.i,dtype=np.float64)
            
        else:
            self.i_p = np.asarray(self.i_p * float(mul_factor),dtype=np.float64)
            self.i_n = np.asarray(self.i_n * float(mul_factor),dtype=np.float64)
    
    def div(self, div_factor:Self | LSV_Data | QV | float):
        """divide the current by a factor.
        Args:
            div_factor (float): div the current dataset with the factor.
        """
       
        if isinstance(div_factor, CV_Data_Base):
            self.i_p = np.asarray(self.i_p / div_factor.i_p,dtype=np.float64)
            self.i_n = np.asarray(self.i_n / div_factor.i_n,dtype=np.float64)
        elif isinstance(div_factor, LSV_Data):
            self.i_p = np.asarray(self.i_p / div_factor.i,dtype=np.float64)
            self.i_n = np.asarray(self.i_n / div_factor.i,dtype=np.float64)
        else:
            self.i_p = np.asarray(self.i_p / float(div_factor),dtype=np.float64)
            self.i_n = np.asarray(self.i_n / float(div_factor),dtype=np.float64)
                
    #############################################################################
    
  
