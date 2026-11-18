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

from .lsv_data_extra import LSV_Data_Extra


STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data_Analysis(LSV_Data_Extra):
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
    ##################################################################################################
        ############################################################################        
    def plot(self,*args, **kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot=subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        Returns:
            line, ax: line and ax handlers
        
        '''
        if should_plot_be_made(*args):
            data = copy.deepcopy(self)
            options = plot_options(**kwargs)
            if self.is_MWE:
                options.set_title(f"{self.setup_data.name}#{self.setup_data._MWE_CH}")
            else:
                options.set_title(self.setup_data.name)
            #options.name = self.setup_data.name
            options.legend = self.legend(*args, **kwargs)
            #if options.legend == "_" :
            #        data_plot_kwargs["legend"] = data.setup_data.name
            #data
            data.norm(args)
            data.set_active_RE(args)
            options.x_data = data.E
            options.y_data = data.i
                    
            options.set_x_txt(data.E_label, data.E_unit)
            options.set_y_txt(data.i_label, data.i_unit) 
            return options.exe()
        else:
            return None,None
    
    

    def integrate(self, start_E:float, end_E:float, show_plot: bool = False, *args, **kwargs):
        """Integrate Current between the voltage limit using cumulative_simpson

        Args:
            start_E (float): potential where to get the current.
            end_E(float) 
            "show_plot" or "no_plot" to show or hide plot.
        Returns:
            [float]: charge
        """
        
        show_plot = True
        for arg in args:
            if "show_plot".casefold() == str(arg).casefold():
                show_plot = True
            if "no_plot".casefold() == str(arg).casefold():
                show_plot = False
                           
        data = copy.deepcopy(self)
        data.norm(args)
        data.set_active_RE(args)
        Q, d  =  data._integrate(  start_E, end_E, data.i, *args, **kwargs)
        
        return Q
        
   ##################################################################################################################
    def Tafel(self, lims=[-1,1], E_for_idl:float=float("nan") , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        
        data_plot,analyse_plot,fig = create_Tafel_data_analysis_plot('LSV',**kwargs)
        if data_plot is None:
            return QV()
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        lsv = copy.deepcopy(self)
        lsv_kwargs = kwargs
        lsv_kwargs["plot"] = data_plot

        plot_color2= []
        
        rot.append( math.sqrt(lsv.rotation))
        lsv_kwargs["legend"] = str(f"{float(lsv.rotation):.0f}")

        line,a = lsv.plot(*args,**lsv_kwargs)
        if line is None:
            return QV()
        lsv.set_active_RE(args)
        for arg in args:
            #if arg == "area":
            lsv.norm(arg)
        plot_color2.append(line.get_color())
        plot_color =line.get_color()
        #.get_color()
        #color = line.get_color()
        xmin = lsv.get_index_of_E(min(lims))
        xmax = lsv.get_index_of_E(max(lims))
           
        y_data=[] 
        print('AAAAAAAAAAAAAAAAA', float("nan"), E_for_idl,math.isnan( E_for_idl))
        if  not math.isnan( E_for_idl):
            
            i_dl = lsv.get_i_at_E(E_for_idl)
            y.append(lsv.get_i_at_E(E_for_idl))
            E.append(E_for_idl)
            
            y_data =(np.abs(diffusion_limit_corr(lsv.i,i_dl)))
          
        else:
            y_data = lsv.i 
        print('limits',xmin,xmax)
        print(lsv.E[xmin:xmax],y_data[xmin:xmax])
        
        Tafel_slope = Tafel(lsv.E[xmin:xmax],y_data[xmin:xmax],lsv.i_unit,lsv.i_label,plot_color,lsv.dir,lsv.E, y_data,plot=analyse_plot, x_label = "E vs "+ self.setup_data.getACTIVE_RE())
       
        y_values = np.array(y)
        if E_for_idl is not None:
            data_plot.plot(E,y_values, STYLE_POS_DL)
        data_plot.legend()
    
        return Tafel_slope
    
    