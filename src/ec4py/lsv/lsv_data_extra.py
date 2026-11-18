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

from .lsv_data_convert import LSV_Data_Load


STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data_Extra(LSV_Data_Load):
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
    def smooth(self, smooth_width:int):
        try:
            self.i = self._smooth(self.i, smooth_width)    
        finally:
            return


    #####################################################################################################
   ######################################################################################### 
    def copy_from(self,source):

        Voltammetry.copy_from(self,source)
        if isinstance(source, LSV_Data_Load):
            self.i = copy.deepcopy(source.i)



    def norm(self, norm_to:str| tuple):
        """Normalize lsv current

        Args:
            norm_to (str): _description_
        """
        
        r,qv = Voltammetry._norm_list(self, norm_to,[self.i] )
        #print("CCCC",r)
        #print("CCCC",qv)
                #n = Voltammetry.norm(self, norm_to,self.i_n )
        
        if r is not None:
            v= r[0]
            #print("AAAAAAA",v)
            #print("BBBBBBB",v)
            if v is not None:
                self.i = v
        return 
        
    
    
    def set_active_RE(self,shift_to:str|tuple = ""):
        #end_norm_factor = None
        # print("argeLIST", type(norm_to))
        if shift_to is not "":
            a = Voltammetry._set_active_RE(self,shift_to, [self.i])
            if a is not None:
                a,b = a
                self.i = b[0]
                # print("pot_shift",a, "REEE",self.E_label)
        return 
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero and adjust the rest of the current.

        Args:
            E (float): potential where to set the current to zero.
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.set_active_RE(args)
        current = new_lsv.get_i_at_E(E,*args,**kwargs)
        self.sub(current)
    
    ####################################################################################################
    def get_index_of_E(self, E:float):
        index = 0
        
        for x in self.E:
            if x > E:
                break
            else:
                index = index + 1
        return min(index,len(self.E)-1)
    
    ########################################################################################################
    def get_i_at_E(self, E:float, *args,**kwargs):
        """Get the current at a specific voltage. The current can be normalized. 

        Args:
            E (float): potential where to get the current. 
        Returns:
             Quantity_Value_Unit: The current, units and label.
        """
        lsv = copy.deepcopy(self)
        lsv.norm(args)
        lsv.set_active_RE(args)  
        smooth_length = kwargs.get("y_smooth",None)
        if smooth_length is not None:
            lsv.smooth(smooth_length)
        
        index = self.get_index_of_E(E) 
        return QV(lsv.i[index],lsv.i_unit,lsv.i_label)
    ###########################################################################################

    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
             (Quantity_Value_Unit | None): _description_
        """
        
        index1 = self.get_index_of_E(E1)
        index2 = self.get_index_of_E(E2)
        index_max=max(index1,index2)
        index_min=min(index1,index2)
        #print(index_min,index_max)
        index_of_max=index_min
        max_i =-1e100
        for index in range(index_min,index_max):
            if max_i<self.i[index] and not np.isnan(self.i[index]) :
                index_of_max = index
                max_i =self.i[index]
        if max_i > -1e100:    
            index_E = index_of_max
            #index_E = self.i[index_min:index_max].argmax()
            #print("index",index_E,"E", self.E[index_E])
            return QV(self.E[index_E],self.E_unit,self.E_label)
        else:
            return None
    ###########################################################################################

    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of minimum current in a range.

        Args:
            E1 (float): Start potential
            E2 (float): End potential

        Returns:
           (Quantity_Value_Unit | None): The voltage of min, or None, if not found
        """
                
        index1 = self.get_index_of_E(E1)
        index2 = self.get_index_of_E(E2)
        index_max=max(index1,index2)
        index_min=min(index1,index2)
        #print(index_min,index_max)
        index_of_min=index_min
        min_i =1e100
        for index in range(index_min,index_max):
            if self.i[index]<min_i and not np.isnan(self.i[index]) :
                index_of_min = index
                min_i =self.i[index]
        if min_i < 1e100:    
            index_E = index_of_min
            #index_E = self.i[index_min:index_max].argmax()
            #print("index",index_E,"E", self.E[index_E])
            return QV(self.E[index_E],self.E_unit,self.E_label)
        else:
            return None
    
    ##################################################################################################
    
        
    def export_DataFrame(self):
        size = [len(Voltammetry().E),2]
        m = np.zeros(size)
        col_names= list("E")
        #print(m.shape,len(self.datas))
        m[:,0]=Voltammetry().E
        
        
            #print(x,self.datas[x].i.shape)
        m[:,1] = self.i
        col_names.append(f"{self.i_label}_{self.name} / {self.i_unit}")
        #print(col_names)
        df = pd.DataFrame.from_records(m,columns=col_names)
        return df