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

from .cv_data_extra import CV_Data_Extra


from ..lsv.lsv_data import LSV_Data
from ..util import Quantity_Value_Unit as QV


from ..util import extract_value_unit     
from ..util import Quantity_Value_Unit as QV
from ..method_util.util_voltammetry import Voltammetry,create_Tafel_data_analysis_plot,POS,NEG,AVG,DIF,find_vertex

from ..method_util.util_data import get_IR
from ..util_graph import plot_options, saveFig, should_plot_be_made,ANALYSE_PLOT,DATA_PLOT

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"


class CV_Data_Analysis(CV_Data_Extra):
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
    
    
    ############################################################################        
    def plot(self,*args,**kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot=subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        
        Returns:
            line, ax: description
        '''
        if should_plot_be_made(*args,**kwargs):
            dir = Voltammetry()._direction(*args,**kwargs)
            if dir == POS or dir == NEG or dir == AVG or dir == DIF:
                lsv = self.get_sweep(dir)
                return lsv.plot(*args,**kwargs)
            
            data = copy.deepcopy(self)
            options = plot_options(**kwargs)
            options.options["dir"]=dir
            #print("AAAAAAAAAAAAAAAAAAAAAAA")
            #print(options.get_y_smooth())
            # print(options.get_legend(),self.legend(**kwargs))
            #print(options.get_title())
            if self.is_MWE:
                options.set_title(f"{self.setup_data.name}#{self.setup_data._MWE_CH}")
            else:
                options.set_title(self.setup_data.name)
                
            options.name = data.setup_data.name
            options.legend = data.legend(*args, **kwargs)
            # print("AAAA",data.legend(*args, **kwargs))
            
            data.norm(args)
            # print(args)
            data.set_active_RE(args)
            options.x_data = data.E
            if(options.get_dir() == POS.casefold()):  
                options.y_data = data.i_p
            
            elif(options.get_dir() == NEG.casefold()):  
                options.y_data = data.i_n
                
            else:
                options.x_data=np.concatenate((data.E, data.E), axis=None)
                options.y_data=np.concatenate((data.i_p, data.i_n), axis=None)  
            
            # options.set_x_txt("E vs "+ data.setup_data.getACTIVE_RE(), data.E_unit)
            options.set_x_txt(data.E_label, data.E_unit)
            options.set_y_txt(data.i_label, data.i_unit) 
            
           
            return options.exe()
        else:
            return None,None
    
    ########################################################################################################
    ###########################################################################################

    def integrate(self, start_E:float, end_E:float, *args, **kwargs):
        """Integrate Current between the voltage limit using cumulative_simpson

        Args:
            start_E (float): potential where to get the current.
            end_E(float) 
            optional args:
                "all", "pos", "neg" - for the direction
                "line": to make a line between i(end_E) and i(start_E), and the integrate between the i(E) and the line.
                "offset_at_emax": Subtracting the value i(E_min) from the i(E) and then integrate.
                "offset_at_emin": Subtracting the value i(E_max) from the i(E) and then integrate.
        Returns:
            [float]: charge
        """
        dir = "all"
        show_plot = True
        for arg in args:
            if "show_plot".casefold() == str(arg).casefold():
                show_plot = True
            if "no_plot".casefold() == str(arg).casefold():
                show_plot = False
            
            if POS.casefold() == str(arg).casefold():
                kwargs["dir"] =POS
            if NEG.casefold() == str(arg).casefold():
                kwargs["dir"] =NEG
                           
        data = copy.deepcopy(self)
  
        
        if kwargs.get("plot",None) is None:
            #line, ax = options.exe()
            
            line, ax = data.plot(*args, **kwargs)
            kwargs["plot"]=ax
            
        data.norm(args)
        data.set_active_RE(args)
        dir = kwargs.get("dir", "all")
        Q_p =QV()
        Q_n =QV()
        if dir != NEG:   
            Q_p, d_p  =  data._integrate(  start_E, end_E, data.i_p, *args, **kwargs)
        if dir != POS:
            Q_n, d_n  =  data._integrate(  start_E, end_E, data.i_n, *args, **kwargs)

        
        #Q_unit =self.i_unit.replace("A","C")
        #yn= np.concatenate(i_p,i_n,axis=0)      
        
        if dir == POS:
            return Q_p#[Q_p[end]-Q_p[0],Q_unit] 
        elif dir == NEG:
            return  Q_n #[Q_n[end]-Q_n[0],Q_unit]
        else:
            return [Q_p, Q_n] #[Q_p[end]-Q_p[0] ,Q_unit, Q_n[end]-Q_n[0],Q_unit]
        
        
   ##################################################################################################################
    def Tafel(self, lims=[-1,1], E_for_idl:float=float('nan') , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        
        data_plot,analyse_plot,fig = create_Tafel_data_analysis_plot("CV", **kwargs)   
        Tafel_kwargs = kwargs.copy()
        Tafel_kwargs[DATA_PLOT]=data_plot
        Tafel_kwargs[ANALYSE_PLOT]=analyse_plot
        dir = self._direction(*args,**kwargs)

        # rot=[]
        # y = []
        # E = []
        #Epot=-0.5
        # y_axis_title =""
        
        Tafel_pos = QV()
        Tafel_neg = QV()
        
        if(dir ==""):
            lsv_pos =self.get_sweep(POS,False)
            Tafel_pos = lsv_pos.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
            lsv_neg =self.get_sweep(NEG,False)
            Tafel_neg = lsv_neg.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        elif(dir == POS):
            lsv_pos =self.get_sweep(POS,True)
            Tafel_pos = lsv_pos.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        elif(dir == NEG):
            lsv_neg =self.get_sweep(NEG,True)
            Tafel_neg = lsv_neg.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        
        if fig is not None:
            saveFig(fig,**kwargs)

        return Tafel_pos, Tafel_neg
    
