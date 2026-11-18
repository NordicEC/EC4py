""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations

from typing import Self
import copy

import numpy as np
import pandas as pd
from ..method_util.util_voltammetry import Voltammetry
from ..util import Quantity_Value_Unit as QV

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data_Base(Voltammetry):
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
   
   
    #############################################################################
    def __add__(self, other: Self|QV|float) -> Self:
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Data: returns a copy of the inital dataset. 
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.add(other)
        return new_lsv
    #############################################################################
    def __sub__(self, other: Self|QV|float):
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Data: returns a copy of the inital dataset. 
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.sub(other)
        return new_lsv
    #############################################################################
    def __mul__(self, other: Self|QV|float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.mul(other)
        return new_lsv
    
    #############################################################################
    def __truediv__(self, other:Self|QV|float):
        """ 

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.div(other)
        return new_lsv
   
    #####################################################################################################
    def __eq__(self, other:Self) -> bool:
        if not isinstance(other, LSV_Data_Base):
            return False
        
        
        equal = Voltammetry.__eq__(self,other)
        print('volt',equal)
        equal = equal and np.array_equal(self.i, other.i,True)
        #print('iarray', equal)
        print('current',equal)
        equal = equal and self.rate_V_s == other.rate_V_s
     
        return equal


    



    def add(self, addData: Self|QV|float) -> None:
        """Add a LSV_Data or a number to the current data"""
        if isinstance(addData, LSV_Data_Base):    
            self.log(f"add dataset{addData.name}")
            self.i = np.asarray(self.i+addData.i,dtype = np.float64)
        else: 
            number = float(addData)
            self.log(f"add {number}")
            self.i = np.asarray(self.i + number,dtype = np.float64)
        #print("ADD",self.i,addData.i)
        #raise TypeError("Addition is only possible with LSV_Data or number")

  #############################################################################   
    def sub(self, subData: Self|QV|float) -> None:
        """Add a LSV_Data or a number to the current data"""
        if isinstance(subData, LSV_Data_Base):    
            self.log(f"add dataset{subData.name}")
            self.i = np.asarray(self.i,dtype = np.float64) - np.asarray(subData.i,dtype = np.float64)
        else:
            number = float(subData)
            self.log(f"sub {number}")
            self.i = np.asarray(self.i - number,dtype = np.float64)
    #############################################################################    
    def mul(self, factor:Self|QV|float):
        """Multiply the current by a factor

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        if isinstance(factor,LSV_Data_Base):
            self.log(f"mul dataset{factor.name}")
            self.i = np.asarray(self.i * factor.i,dtype=np.float64)
        else:

            self.log(f"mul {factor}")
            self.i = np.asarray(self.i * float(factor),dtype=np.float64)
        #else:
        #    raise TypeError("Multiplication is only possible with a number")    
 #############################################################################    
    def div(self, factor:Self|QV|float):
        """Divide the current by a factor

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        if isinstance(factor,LSV_Data_Base):
            self.log(f"div dataset{factor.name}")
            self.i = np.asarray(self.i / factor.i,dtype=np.float64)
        else:
            self.log(f"div {factor}")
            self.i = np.asarray(self.i / float(factor),dtype=np.float64)

        #   raise TypeError("Division is only possible with a number")
         
    
    
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