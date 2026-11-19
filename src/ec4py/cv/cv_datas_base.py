""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
# import math
# import numpy as np
from __future__ import annotations
from typing import Self, SupportsIndex, overload

import numbers

from ..ec_data import EC_Data
from ..method_util.ec_datas_util import EC_Datas_base,check_paths

from .cv_data import CV_Data,STYLE_POS_DL,STYLE_NEG_DL, POS, NEG 

from ..util import Quantity_Value_Unit as QV

from pathlib import Path
import copy

from ..lsv import LSV_Data, LSV_Datas




class CV_Datas_Base(EC_Datas_base):
    """# Class to analyze CV datas. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.

    ### Analysis:
    - .Levich() - plot data    
    - .KouLev() - Koutechy-Levich analysis    
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """
    def __init__(self,*args, **kwargs):
        
        EC_Datas_base().__init__(self,*args, **kwargs)

        self.datas:list[CV_Data] =[]

        
       
    #############################################################################
    
  #  def __repr__(self):
        """CV Datas
        """
   #     delimiter = "','"
    #    r =delimiter.join([x.setup_data.fileName for x in self.datas])
     #   return f"{CV_Datas}(['{r}'])"
    
        

        ########################################
    
    def __setitem__(self, item_index:int, new_CV:CV_Data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_CV
    #############################################################################
    
    def __add__(self, other: Self | LSV_Datas| list[CV_Data]|list[LSV_Data]|list[QV]|list[float] | CV_Data | LSV_Data | QV | float):
        """add

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.add(other)
        return new_CVs
    
    def __sub__(self, other: Self  | LSV_Datas| list[CV_Data]|list[LSV_Data]|list[QV]|list[float] | CV_Data | LSV_Data | QV | float):
        """sub

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.sub(other)
        return new_CVs
    
    def __mul__(self, other: float):
        """multiply

        Args:
            other (float): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.mul(other)
        return new_CVs
    
    def __truediv__(self, other: Self | LSV_Datas| list[CV_Data] |list[LSV_Data] | list[QV] | list[float] | CV_Data | LSV_Data | QV | float):
        """divide

        Args:
            other (float): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.div(other)
        return new_CVs

    #def __len__(self):
    #    return len(self.datas)

    #############################################################################
    
    
    def add(self,other: Self | LSV_Datas| list[CV_Data]|list[LSV_Data]|list[QV]|list[float] | CV_Data | LSV_Data | QV | float):
        """add

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, (CV_Datas_Base,list,LSV_Datas)):
            #print('Qa',type(other))
            if len(other) == len(self):
                for i in range(len(self.datas)):
                    item = other[i]
                    if isinstance(item,(CV_Data | LSV_Data | QV | numbers.Real)):
                        #print('QER',item,'a',type(item))
                        self.datas[i].add(item)
            
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.add(other)  
        ##########################################        
    def sub(self,other: Self | LSV_Datas| list[CV_Data] |list[LSV_Data] | list[QV] | list[float] | CV_Data | LSV_Data | QV | float):
        """sub
        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, (CV_Datas_Base, LSV_Datas, list)):
            if len(other) == len(self.datas):
                for i in range(len(self.datas)):
                    item = other[i]
                    if isinstance(item,(CV_Data | LSV_Data | QV | numbers.Real)):
                        self.datas[i].sub(item)
            else:
                raise ValueError('The data sets are not of the same length.')
            
        else:
            for cv in self.datas:
                cv.sub(other)
                
    def mul(self,other:Self | LSV_Datas| list[CV_Data] |list[LSV_Data] | list[QV] | list[float] | CV_Data | LSV_Data | QV | float):
        """multiply the current by a number or a list of numbers.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].mul(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                if isinstance(other,(CV_Data , LSV_Data , QV , float, int)):
                    cv.mul(other)
            
    def div(self,other:Self | LSV_Datas| list[CV_Data] |list[LSV_Data] | list[QV] | list[float] | CV_Data | LSV_Data | QV | float):
        """divide the current by a number.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, (CV_Datas_Base ,LSV_Datas, list)):
            if len(other) == len(self.datas):
                for i in range(len(self.datas)):
                    temp = other[i]
                    if isinstance(temp,(QV,numbers.Real,CV_Data,LSV_Data,LSV_Data)):
                        self.datas[i].div(temp) 
                    #if:
                    #    self.datas[i].div(temp) 

            else:
                raise ValueError('The data sets are not of the same length.')
        elif isinstance(other, (CV_Data , LSV_Data , QV , float )):
            for cv in self.datas:
                cv.div(other)   
        
    
    def append(self,item : Self | CV_Data):
        """append

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(item, (CV_Datas_Base,CV_Data)):
            self._append(item)
        #elif isinstance(item, Self):
        #    for cv in item:
        #        self.datas.append(cv)
    
    #def pop(self,index):
    #    self.datas.pop(index)
    
  
      
    #############################################################################

    @overload
    def __getitem__(self, i: SupportsIndex| str, /) -> CV_Data: ...
    
    @overload
    def __getitem__(self, s: slice| list[str], /) -> Self: ...
    
    def __getitem__(self,  index_or_str: SupportsIndex|slice | int | list[str] | str) -> Self|CV_Data: 
        return EC_Datas_base.__getitem__(self,index_or_str) # type: ignore

    
    
    
    
    def bg_corr(self, bg_cv: Self|CV_Data|Path) -> Self:
        """Background correct the data by subtracting the bg_cv. 

        Args:
            bg_cv (CV_Datas, CV_Data or Path):
        
        Returns:
            CV_Data: copy of the data.
        
        """
        if isinstance(bg_cv, CV_Datas_Base):
            if len(bg_cv.datas) == len(self.datas):
                for i in range(len(self.datas)):
                    self.datas[i].sub(bg_cv.datas[i])
            else:
                raise ValueError('The data sets are not of the same length.')

        else:         
            if isinstance(bg_cv, CV_Data):
                corr_cv =bg_cv    
            else:
                corr_cv =CV_Data(bg_cv)
                #print(bg_cv)
            for cv in self.datas:
                cv.sub(corr_cv)
        return copy.deepcopy(self)


