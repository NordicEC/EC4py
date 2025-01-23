""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data
from .ec_data_util import EC_Channels

from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV

from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig, Legend

class EIS_Data(EC_Setup):

    def __init__(self,*args, **kwargs):
        EC_Setup.__init__(self,*args, **kwargs)
        self.freq=[]
        self.Z=[]
        self.Z_unit=""
        self.Z_label=""
        self.angle=[]
       
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]), *args, **kwargs)
    
    
    def conv(self,ec_data ,*args, **kwargs):
        sel_channels = EC_Channels(*args,**kwargs)

        try:
            self.setup_data = copy.deepcopy(ec_data.setup_data)
            data_f,q,u = ec_data.get_channel("Frequency")
            data_E,q,u = ec_data.get_channel(sel_channels.Voltage)
            data_i,q,u = ec_data.get_channel(sel_channels.Current)
            data_Z,self.Z_label,self.Z_unit = ec_data.get_channel(sel_channels.Impedance)
            data_Phase,q,u = ec_data.get_channel(sel_channels.Phase)
            self.Z = data_Z
            self.freq = data_f
            self.Phase =data_Phase
        except NameError as e:
            print(e)
            raise NameError(e)
            return

        return
    
    

        
    
    def nq(self,*args, **kwargs):
        
        data = copy.deepcopy(self)
        r = data.norm( args, data.Z)
        if r is not None:
            data.Z= r[0]
        kwargs["style"]="o"
        options = plot_options(kwargs)
        # print(options.get_legend(),self.legend(**kwargs))
        
        options.set_title(data.setup_data.name)
        options.name = data.setup_data.name
        options.legend = data.legend(*args, **kwargs)
        
        Z_re = data.Z*np.cos(data.Phase)
        Z_im = data.Z*np.sin(data.Phase)
        
        options.x_data=  Z_re
        options.y_data= -Z_im 
        
        # options.set_x_txt("E vs "+ data.setup_data.getACTIVE_RE(), data.E_unit)
        x_label = data.Z_label.replace("Z","Z_re")
        y_label = data.Z_label.replace("Z","-Z_im")
        options.set_x_txt(x_label, data.Z_unit)
        options.set_y_txt(y_label,data.Z_unit) 
        
        # print(options.get_legend())
        line, ax = options.exe()
        fix_plot_Xrange(ax, **kwargs)
        fix_plot_Yrange(ax, **kwargs)
            
        return line,ax 
    
    def bode(self,*args, **kwargs):
        
        data = copy.deepcopy(self)
        BODE_op= {"bode_Z": None,"bode_phase": None}
        BODE_op.update(kwargs)
        
        plot_Z = BODE_op["bode_Z"]
        plot_phase = BODE_op["bode_phase"]
        fig = None
     
        bode_f = plot_options(kwargs)
        bode_phase = plot_options(kwargs)

        if BODE_op["bode_Z"] is None and BODE_op["bode_phase"] is None:
            fig = make_plot_2x("Bode Plot",True)
            plot_Z = fig.plots[0]
            plot_Z.set_xscale("log")
            lims_x ={"left": None,"right": None}
            lims_x.update(kwargs)
            #plot_Z.set_xlim(lims_x)
            plot_phase = fig.plots[1]
            plot_phase.set_xscale("log") 
            bode_f_args=dict()
            bode_f_args["plot"]=plot_Z
            bode_f_args["xscale"]="log"
            bode_f_args["style"]="o"
            
            bode_f = plot_options(bode_f_args )
            bode_f.set_x_txt("Freq", "Hz")
            bode_f.set_y_txt("Z", "Ohm")
            
            bode_A_args=dict()
            
            bode_A_args["plot"]=plot_phase
            bode_A_args["xscale"]="log"
            bode_A_args["style"]="o"
            bode_phase = plot_options(bode_A_args )
            bode_phase.set_x_txt("Freq", "Hz")
            bode_phase.set_y_txt("Phase", "rad")
            
            
            # bode_f.set_y_txt(data.i_label, data.i_unit)  
        
        
        # print(options.get_legend(),self.legend(**kwargs))
        
        bode_f.set_title(data.setup_data.name)
        bode_f.name = data.setup_data.name
        bode_f.x_data = data.freq
        bode_f.y_data = data.Z

        # bode_f.legend = data.legend(*args, **kwargs)
        
        bode_phase.x_data = data.freq
        bode_phase.y_data = data.Phase
  
        line,ax0= bode_f.exe()
        line,ax1 = bode_phase.exe()
        fix_plot_Xrange(ax0, **kwargs)
        fix_plot_Xrange(ax1, **kwargs)
        return plot_Z,plot_phase
    
    def norm(self, norm_to:str|tuple, Impedance):
        
        norm_factor = self.get_norm_factors(norm_to)
        Impedance_shifted = None
        if norm_factor is not None:
            Impedance_shifted = Impedance.copy()
            Impedance_shifted = Impedance / float(norm_factor)
        #norm_factor_inv = norm_factor ** -1
            qv = QV(1, self.Z_unit, self.Z_label) / norm_factor
            self.Z_unit = qv.unit
            self.Z_label = qv.quantity
            # print("aaaa-shifting",self.i_unit)
        return Impedance_shifted, qv
            
        
def fix_plot_Xrange(ax,*args, **kwargs):
    if ax is not None:
        r_lim = None
        l_lim = None
        [l_lim,r_lim] = kwargs.get("xlim",[None, None])
        r_lim= kwargs.get("right",r_lim)
        l_lim= kwargs.get("left",l_lim)
        ax.set_xlim(l_lim,r_lim)
        
    return

def fix_plot_Yrange(ax,*args, **kwargs):
    if ax is not None:
        t_lim = None
        b_lim = None
        [b_lim,t_lim] = kwargs.get("ylim",[None, None])
        b_lim= kwargs.get("bottom",b_lim)
        t_lim= kwargs.get("top",t_lim)
        ax.set_ylim(b_lim,t_lim)
         
    return



    