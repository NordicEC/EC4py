""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
# import math
# import numpy as np
from __future__ import annotations
from typing import Self
import numbers

from ..ec_data.ec_data import EC_Data
from ..method_util.ec_datas_util import EC_Datas_base,check_paths

from .cv_data import CV_Data,STYLE_POS_DL,STYLE_NEG_DL, POS, NEG 
from ..util import Quantity_Value_Unit as QV

from pathlib import Path
import copy
# from .util import Quantity_Value_Unit as QV
from ..util_graph import plot_options,saveFig
from ..util_graph import LEGEND, should_plot_be_made, update_plot_kwargs, ENUM_plotKW, ANALYSE_PLOT, DATA_PLOT

# from .analysis_levich import Levich
from ..analysis.analysis_ran_sev   import ran_sev
from ..analysis.analysis_rate   import sweep_rate_analysis


from ..method_util.util_voltammetry import Voltammetry,create_Tafel_data_analysis_plot,create_RanSev_data_analysis_plot
from ..method_util.util_voltammetry import create_Rate_data_analysis_plot,create_Levich_data_analysis_plot,create_KouLev_data_analysis_plot
from ..lsv.lsv_datas import LSV_Datas
from ..lsv.lsv_data import LSV_Data
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # Gives Pylance/Pyright full autocomplete without circular imports
    _Analysis = object
else:
    from .cv_datas_analysis import CV_Datas_Anlysis
    _Analysis = CV_Datas_Anlysis
    
# import pandas as pd
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas(EC_Datas_base,_Analysis):
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
    def __init__(self,paths:list[Path]|Path = [],*args, **kwargs):
        
        EC_Datas_base().__init__(self,*args, **kwargs)

        self.datas:list[CV_Data] =[]

        
        if paths is not None:
            path_list = check_paths(paths)
            # paths = args[0]
            """
            if not isinstance(paths,list ):
                path_list = [paths]
            #if isinstance(paths,Path ):
            #    path_list = [paths]
            else:
                path_list = paths
            """
            self.datas = [CV_Data() for i in range(len(path_list))]
            index=0
            for path in path_list:
                ec = EC_Data(path)
                #print([x for x in args])
                try:
                    
                    self.datas[index].conv(ec,*args,**kwargs)
                finally:
                    index=index+1 
            #print(index)
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
    
    def __truediv__(self, other: float):
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
        if isinstance(other, (CV_Datas,list,LSV_Datas)):
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
        if isinstance(other, (CV_Datas, LSV_Datas, list)):
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
                
    def mul(self,other):
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
                cv.mul(other)
            
    def div(self,other:Self | LSV_Datas| list[CV_Data] |list[LSV_Data] | list[QV] | list[float] | CV_Data | LSV_Data | QV | float):
        """divide the current by a number.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, (CV_Datas,LSV_Datas, list)):
            if len(other) == len(self.datas):
                for i in range(len(self.datas)):
                    temp = other[i]
                    if isinstance(temp,(QV,numbers.Real,CV_Data,LSV_Data,LSV_Data)):
                        self.datas[i].div(temp) 
                    #if:
                    #    self.datas[i].div(temp) 

            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.div(other)   
        
    
    def append(self,item : Self | CV_Data):
        """append

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(item, (CV_Datas,CV_Data)):
            self._append(item)
        #elif isinstance(item, Self):
        #    for cv in item:
        #        self.datas.append(cv)
    
    #def pop(self,index):
    #    self.datas.pop(index)
    
  
      
    #############################################################################
    def __getitem__(self,  index_or_str: slice | int | list[str] | str) -> CV_Datas|CV_Data: 
        return EC_Datas_base.__getitem__(self,index_or_str) # type: ignore

  #  def __repr__(self):
        """CV Datas
        """
   #     delimiter = "','"
    #    r =delimiter.join([x.setup_data.fileName for x in self.datas])
     #   return f"{CV_Datas}(['{r}'])"
    
        
    '''
    def append(self,item : Self | CV_Data):
        """append

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(item, CV_Data):
            self.datas.append(item)
        elif isinstance(item, CV_Datas):
            for cv in item:
                self.datas.append(cv)
    '''
    #def pop(self,index):
    #    self.datas.pop(index)
    
    
    
    
    def bg_corr(self, bg_cv: CV_Datas|CV_Data|Path) -> Self:
        """Background correct the data by subtracting the bg_cv. 

        Args:
            bg_cv (CV_Datas, CV_Data or Path):
        
        Returns:
            CV_Data: copy of the data.
        
        """
        if isinstance(bg_cv, CV_Datas):
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

  #  def pot_shift(self,shift_to:str|tuple|None = None):
  ##      """Shift the potential to another defined reference potential.
#
 #       Args:
  #          shift_to (str | tuple, optional): RHE or SHE. Defaults to None.
   #     """
   #     for cv in self.datas:
    #        cv.pot_shift(shift_to)
    



