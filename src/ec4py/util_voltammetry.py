""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV







class Voltammetry(EC_Setup):
    def __init__(self,*args, **kwargs):
        super().__init__(args,kwargs)
        self.E=[]
        self.E_label = "E"
        self.E_unit = "V"
        #self.rate_V_s = 1
        self.i_label = "i"
        self.i_unit = "A"

        self.E_axis = {
                    "E_min" : -2.5,
                    "E_max" :  2.5 
                    }
        self.xmin = -2.5 # View range
        self.xmax = 2.5  # view renage
        self.E_axis.update(kwargs)
        self.E = self.make_E_axis()
        
    #############################################################################
    def make_E_axis(self, Emin = None, Emax = None):
        if Emin is not None:
            self.E_axis["E_min"] = Emin
        if Emax is not None:
            self.E_axis["E_max"] = Emax
        maxE = self.E_axis["E_max"]
        minE = self.E_axis["E_min"]    
        dE_range = int((maxE - minE)*1000)
        E_sweep = np.linspace(minE, maxE, dE_range+1)
        return E_sweep

####################################################################################################
    def get_index_of_E(self, E:float):
        if E is None:
            return None
        index = 0
        for x in self.E:
            if x >= E:
                break
            else:
                index = index + 1
        return index
    
    def interpolate(self, E_data, y_data ):
        return np.interp(self.E, E_data, y_data)
    
    def _integrate(self, start_E:float, end_E:float,current:list(float), dir:str = "all", show_plot: bool = False, *args, **kwargs):
        """Integrate Current between the voltage limit using cumulative_simpson

        Args:
            start_E (float): potential where to get the current.
            end_E(float) 
            dir (str): direction, "pos,neg or all"
        Returns:
            [float]: charge
        """
        index1 = self.get_index_of_E(start_E)
        index2 = self.get_index_of_E(end_E)
        imax = max(index1,index2)
        imin = min(index1,index2)
        #print("INDEX",index1,index2)
        #try:
        (current[imin:(imax+1)]).copy()
        loc_i = (current[imin:imax+1]).copy()
        loc_i[np.isnan(loc_i)] = 0
        loc_E = self.E[imin:imax+1]

        array_Q = integrate.cumulative_simpson(loc_i, x=loc_E, initial=0) / float(self.rate)        
        
        Q_unit =self.i_unit.replace("A","C")
        #yn= np.concatenate(i_p,i_n,axis=0)
        
        # y = [max(np.max(i_p),np.max(i_n)), min(np.min(i_p),np.min(i_n))]
        """
        y = [np.max(loc_i), np.min(loc_i)]
        x1 = [self.E[imin],self.E[imin]]
        x2 = [self.E[imax+1],self.E[imax+1]]  
        cv_kwargs = kwargs  
        if show_plot:
            cv_kwargs["dir"] = dir
            line, ax = self.plot(**cv_kwargs)
            ax.plot(x1,y,'r',x2,y,'r')
            if dir != "neg":
                ax.fill_between(self.E[imin:imax+1],i_p,color='C0',alpha=0.2)
            if dir != "pos":
                ax.fill_between(self.E[imin:imax+1],i_n,color='C1',alpha=0.2)
        """    
        #except ValueError as e:
        #    print("the integration did not work on this dataset")
        #    return None
        end = len(array_Q)-1
        loc_Q = QV(array_Q[end]-array_Q[0],Q_unit,"Q")        
        #print(Q_p)
        return loc_Q, [loc_E,loc_i,array_Q ] 
    
    def clean_up_edges(self, current):
        for i in range(1,current.size):
            if current[i-1] == current[i]:
                current[i-1] = math.nan
            else :
                break
            
        for i in range(current.size-2,0,-1):
            if current[i] == current[i+1]:
                current[i+1] = math.nan
            else :
                break
        return current
    
    def pot_shift(self,shift_to:str|tuple):
        end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        if isinstance(shift_to, tuple):
           
            for item in shift_to:
                # print("ITTTT",item)
                shift_factor = self.get_pot_offset(item)
                if shift_factor:
                    end_norm_factor=  shift_factor
                    break
        else:
            shift_factor = self.get_pot_offset(shift_to)
            #print(norm_factor)
            if shift_factor:
                end_norm_factor = shift_factor
                
        if end_norm_factor is not None:
            self.E = self.E + end_norm_factor.value
            self.E_label = end_norm_factor.quantity
            self.E_unit = end_norm_factor.unit
            # print("SHIFT:",end_norm_factor)
        return 
        
    