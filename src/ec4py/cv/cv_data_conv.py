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


from .cv_data_base import CV_Data_Base


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


class CV_Data_Load(CV_Data_Base):
    """# Class to analyze a single CV data. 
      """


    def __init__(self,*args, **kwargs):
        #EC_Setup.__init__(self,*args, **kwargs)
        super().__init__(self, *args, **kwargs)
        # self.E=[]
  
  

    ######################################################################################################
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a CV

        Args:
            ec_data (EC_Data): the data that should be converted.
        """
        #print("Convert:",kwargs)
        
        #ch_E ="E"
        #for a in args:
        #    if a == "IR":
        #        ch_E = "E-IR"
        options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'IRCORR': None,
            'E' : "E",
            'i' : 'i'
        }
        options.update(kwargs)
        sel_channels = EC_Channels(*args,**kwargs)
        ir_comp =False
        r_comp=None
        vertex =[]
        try:
            data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
            data_i,q,u,dt_y = ec_data.get_channel(sel_channels.Current)
        except NameError as e:
            print(e)
            raise NameError(e)
            return
        
        try:
            comp = options.get("IRCORR",None)
            if comp is not None:
                
                ir_comp, data_IR = get_IR(ec_data,sel_channels,comp)
                vertex = find_vertex(data_E)
                r_comp = data_IR/data_i
                if ir_comp:
                    data_E = data_E - data_IR
                
        except NameError as e:
            print(e)
            raise NameError(e)
            return

        
        self.setup_data = copy.deepcopy(ec_data.setup_data)
        self.convert(ec_data.Time,data_E,data_i,vertex = vertex, **kwargs)
        self.IR_COMPENSATED = ir_comp
        self.R_COMP = r_comp
        E_title = "E"
        #if ir_comp: ###NOT NEEDED
        #    E_title ="E-iR"
        self.setup_data.select_MWE_CH(sel_channels.MWE_CH)   
        
        try:
            self.IR_COMPENSATED = ir_comp
            E_title = "E"
            #if ir_comp: ###NOT NEEDED
            #    E_title ="E-iR"
            if 'Ref.Electrode' in self.setup:
                self.E_label = f"{E_title} vs " + self.RE
                #print("aaaaa")
            else:
                self.E_label =f"{E_title}"
            if self.is_MWE:
                self.setup_data.select_MWE_CH(sel_channels.MWE_CH)
            

        except ValueError as e:
            if(self.is_MWE):
                print(e)
                print("select a current channel, such as i_0")
            else:
                print("no_data")
        
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return

    #####################################################################################################    
    def convert(self, time, Potential_V, Current_A, **kwargs):
        """Converts data to CV data

        Args:
            time (_type_): time
            E (_type_): potential
            i (_type_): current
            direction(str): direction
        """
        x= Potential_V
        y= Current_A

        #vertex =kwargs.get("vertex",None)
        #if vertex is None:
        #    vertex = find_vertex(x)
        #print("Convert", len(E))
        #print("SETP",self.setup)
        #Start_Delay, = extract_value_unit(self.setup_data._setup['Start_Delay'])
        #print("Start", self.setup['Start'])
        #print("V1", self.setup['V1'])
        V0, V0_str = extract_value_unit(self.setup['Start'])
        #print("V1", self.setup['V1'])
        V1, V1_str = extract_value_unit(self.setup['V1'])
        #print("V2", self.setup['V2'])
        V2, V2_str = extract_value_unit(self.setup['V2'])
        # print("CV", V0,V1,V2)
        options = plot_options(**kwargs)
        #print("CONVERTING",len(time), len(E), len(i))
        #try:
        #    y_smooth = int(options['y_smooth'])
        #    if(y_smooth > 0):
        #        y = savgol_filter(y, y_smooth, 1)
        #finally:
        #    pass
        positive_start = False
        if V0 == V1:
            positive_start = (V1 < V2)
        else:
            positive_start = V0 < V1
        #print("startDIR:", positive_start)

        y = options.smooth_y(y)

        self.xmin = x.min()
        self.xmax = x.max()

        #x_start = np.mean(x[0:3])
        #index_min = np.argmin(x)
        #index_max = np.argmax(x)

        #array of dx

        x_div = np.gradient(savgol_filter(x, 10, 1))
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        #print("ZERO:",zero_crossings)
        self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        #print(f"Rate: {self.rate_V_s}")
        #up_start =0
        #up_end = 0
        ## Number of vertext
        Two_vertex = len(zero_crossings)>1
        #print("MIN",x[zero_crossings[0]], np.min(x[0:zero_crossings[1]]))
        #print("argMIN",zero_crossings[0], np.argmin(x[0:zero_crossings[1]]))
        if not Two_vertex:  #if the CV consists of 2 LSV, there is only one zero crossing.
            zero_crossings = np.append(zero_crossings,len(x))
      
        if positive_start:
            zero_crossings[0] = np.argmax(x[0:zero_crossings[1]])
        else:
            zero_crossings[0] = np.argmin(x[0:zero_crossings[1]])
      
        self.E = self.make_E_axis()
        zero_crossings = np.append(zero_crossings, x.size)
        #print("ZERO:",len(zero_crossings),zero_crossings, "2x vertex", Two_vertex)

        x_u2=np.array([],dtype=np.float64)
        y_u2=np.array([],dtype=np.float64)
        x_n2=np.array([],dtype=np.float64)
        y_n2=np.array([],dtype=np.float64)

        if positive_start:
            x_u = x[0:zero_crossings[0]]
            y_u = y[0:zero_crossings[0]]
            x_n = np.flipud(x[zero_crossings[0]:zero_crossings[1]])
            y_n = np.flipud(y[zero_crossings[0]:zero_crossings[1]])
            if Two_vertex:
                x_u2 = x[zero_crossings[1]:zero_crossings[2]]
                y_u2 = y[zero_crossings[1]:zero_crossings[2]] 
                # print(zero_crossings)
                mask = x_u2<x_u.min()
                
                x_u2=np.array(x_u2[mask],dtype=np.float64)
                if len(y_u2)>=len(mask):
                    y_u2=np.array(y_u2[mask])
                x_u2 = np.asarray(x_u2,dtype=np.float64)        
                y_u2 = np.asarray(y_u2,dtype=np.float64)        

        else:
            #print("neg first sweep")
            x_n = np.flipud(x[0:zero_crossings[0]])
            y_n = np.flipud(y[0:zero_crossings[0]])
            x_u = x[zero_crossings[0]-1:zero_crossings[1]]
            y_u = y[zero_crossings[0]-1:zero_crossings[1]]
            if Two_vertex:
                x_n2 = np.flipud(x[zero_crossings[1]:zero_crossings[2]])
                y_n2 = np.flipud(y[zero_crossings[1]:zero_crossings[2]])
                mask = x_n2>x_n.max()
                x_n2=np.array(x_n2[mask],dtype=np.float64)
                y_n2=np.array(y_n2[mask],dtype=np.float64)

        #y_pos=np.interp(x_sweep, x_u, y_u)
        #y_neg=np.interp(x_sweep, x_n, y_n)
        y_pos=   self.interpolate(x_u, y_u)
        y_pos =  self.clean_up_edges(y_pos,0)
        
        if Two_vertex and positive_start:
            y_pos2 = self.interpolate(x_u2, y_u2)
            y_pos2 =  self.clean_up_edges(y_pos2,0)
            y_pos = y_pos + y_pos2
       
        y_neg=self.interpolate(x_n, y_n)
        y_neg = self.clean_up_edges(y_neg,0)

        if Two_vertex and not positive_start:
          #  print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
          #  print("x_n2",len(x_n2))
          #  print("y_n2",len(y_n2))
            y_neg2 = self.interpolate(x_n2, y_n2)
            y_neg2 = self.clean_up_edges(y_neg2,0)
            y_neg=y_neg+y_neg2
            #print("YNEG",y_neg[0])
            
        #print("YPOS",y_pos)        
        #print("YNEG",y_neg.size)
        #"""
        if positive_start or (not positive_start and Two_vertex):
            indexes = y_pos.nonzero()[0]
            if len(indexes)>0:
                max_arg= indexes.max()
                y_neg[max_arg]=y_pos[max_arg]    
                
        if not positive_start or (positive_start and Two_vertex):
            #c = a.nonzero()[0]
            mask =y_neg.nonzero()[0]
            min_arg= mask.min()
            #np.flatnonzero(y_neg).min()
            #print("BBB", min_arg,y_neg[min_arg],y_neg[min_arg+1],y_pos.nonzero()[0].min())
            y_pos[min_arg]=y_neg[min_arg]
        #"""    
        self.i_p = self.clean_up_edges(y_pos)
        self.i_n = self.clean_up_edges(y_neg)
        
