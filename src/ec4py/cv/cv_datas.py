""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
# import math
# import numpy as np
from __future__ import annotations
from typing import Self, SupportsIndex, overload

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


from .cv_datas_analysis import CV_Datas_Analysis
    
# import pandas as pd
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas(CV_Datas_Analysis):
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
        
        super().__init__(*args, **kwargs)
        
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
    
        

 
  
      
    #############################################################################

    @overload
    def __getitem__(self, i: SupportsIndex| str, /) -> CV_Data: ...
    
    @overload
    def __getitem__(self, s: slice| list[str], /) -> CV_Datas: ...
    
    def __getitem__(self,  index_or_str: SupportsIndex|slice | int | list[str] | str) -> CV_Datas|CV_Data: 
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
    
    
    