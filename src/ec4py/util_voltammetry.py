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
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x, ANALYSE_PLOT, DATA_PLOT


OFFSET_AT_E_MIN ="offset_at_emin"
OFFSET_AT_E_MAX ="offset_at_emax"
OFFSET_LINE ="line"

POS = "pos"
NEG = "neg"
AVG = "avg"
DIF = "dif"

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"
STYLE_AVG_DL = "go"
STYLE_DIF_DL = "go"


STYLE_POS_L = "b-"
STYLE_NEG_L = "r-"
STYLE_AVG_L = "g-"
STYLE_DIF_L = "g-"


class Voltammetry(EC_Setup):
    def __init__(self,*args, **kwargs):
        super().__init__(args,kwargs)
        self.E=[]
        
        self.E_label = "E" # Potential label
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
        self.dir ="Direction"
        
        self.E_axis.update(kwargs)
        self.E = self.make_E_axis()
        self.E_shifted_by = None
    
    
    
    def copy_from(self, source:Voltammetry):
        """Voltammetry copy from source voltammetry

        Args:
            source (Voltammetry): Any voltammetry class
        """
        self.E              = source.E
        self.E_label        = source.E_label
        self.E_unit         = source.E_unit
        self.E_axis         = source.E_axis
        self.E_shifted_by   = source.E_shifted_by
        self.xmin = source.xmin
        self.xmax = source.xmax
        self.i_label = source.i_label
        self.i_unit = source.i_unit
        EC_Setup.copy_from(self,source)
        
    
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
        index = int(0)
        for x in self.E:
            if x >= E:
                break
            else:
                index = index + 1
        return index
    
####################################################################################################    
    def _get_E_at_i(self, current, i_threashold,*args, **kwargs):
        
        options = {"tolerance": 0.0,
                   "show_plot": False,
                   "plot": None
                   }
        options.update(kwargs)
        
        #get indexes where 
        smaller_than = np.argwhere(current < i_threashold-options["tolerance"])
        larger_than = np.argwhere(current > i_threashold+options["tolerance"])
        start = 0
        end =len(current)
        if(len(smaller_than)!=0):
            start = np.max(smaller_than)
        if(len(larger_than)!=0):
            end  = np.min(larger_than)
        
        E_fit = self.E[start:end+1]
        i_fit = current[start:end+1]
        k,m = np.polyfit(i_fit, E_fit, 1)
        p =options["plot"]
        if p is not None:
            p.plot(E_fit,i_fit,".",[m+k*i_threashold],[i_threashold],"ro")
        
        return m+k*i_threashold

    #####################################################################################################    
    def _smooth(self, current, smooth_width:int):
        try:
            smoothed_current = savgol_filter(current, smooth_width+1, 1)
        finally:
            return smoothed_current
    
    def interpolate(self, E_data, y_data ):
        return np.interp(self.E, E_data, y_data)
    
    def _offset(self, offset:float):
        return np.ones(self.E)*offset
    
    def _line(self, k:float, m:float):
        """Generate a line y=k*E+m

        Args:
            k (float): slope
            m (float): offset

        Returns:
            NDArray: slope
        """
        return self.E*k+ m
    
    def _direction(self,*args, **kwargs):
        direction = ""
        for arg in args:
            # print(arg)
            test = str(arg).casefold()
            if test == POS.casefold():
                direction = POS  
            if test == NEG.casefold():
                direction = NEG   
            if test == AVG.casefold():
                direction = AVG 
            if test == DIF.casefold():
                direction = DIF 
        direction = kwargs.get("dir",direction)
        return direction
    
    def _integrate(self, start_E:float, end_E:float,current:list(float), *args, **kwargs):
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
        
        # (current[imin:(imax+1)]).copy()
       
        loc_i = (current[imin:imax+1]).copy()
        loc_i[np.isnan(loc_i)] = 0
        loc_E = self.E[imin:imax+1]
        offset = np.zeros(len(loc_i))
        #for arg in args:
        #    print(arg) 
        for arg in args:
            a = str(arg).casefold()
            if a == "offset_at_emin".casefold():
                # print("OFFSET at MIN")
                offset =np.ones(len(loc_i))*loc_i[0]
            if a == "offset_at_emax".casefold():
                offset =np.ones(len(loc_i))*loc_i[len(loc_i)-1]
            if a == "line".casefold():
                k = (loc_i[len(loc_i)-1]-loc_i[0])/ (end_E-start_E)
                m = loc_i[0]-k*start_E
                offset = k*loc_E+m
                
        array_Q = integrate.cumulative_simpson(loc_i-offset, x=loc_E, initial=0) / float(self.rate)        
        
        Q_unit =self.i_unit.replace("A","C")
        #yn= np.concatenate(i_p,i_n,axis=0)
        
        # y = [max(np.max(i_p),np.max(i_n)), min(np.min(i_p),np.min(i_n))]
        
        y = [np.max(loc_i), np.min(loc_i)]
        x1 = [self.E[imin],self.E[imin]]
        x2 = [self.E[imax+1],self.E[imax+1]] 
        ax = kwargs.get("plot",None) 
        if ax is not None:
            ax.plot(x1,y,'r',x2,y,'r')
            ax.fill_between(loc_E,loc_i,offset, color='C0',alpha=0.2)
        """  
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
        return loc_Q, [loc_E,loc_i,array_Q, offset ] 
    
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
    
    def set_active_RE(self,shift_to:str|tuple, current: list=None):
        """_summary_

        Args:
            shift_to (str | tuple): Name of new reference potential
            current (list, optional): list like array of data points. Defaults to None.

        Returns:
            _tuple_: shifted potential, and shifted data. or NONE
        """
        end_norm_factor = None
        # print("argeLIST", type(norm_to))
        # print(shift_to)
        last_Active_RE = self.setup_data.getACTIVE_RE()
        end_norm_factor = EC_Setup.set_active_RE(self, shift_to)
        
        self.E_label = "E vs "+ self.setup_data.getACTIVE_RE()      
        if end_norm_factor is not None:
            if  self.E_shifted_by == end_norm_factor.value :  
                pass #potential is already shifted.
            else:
                if self.E_shifted_by is None :
                    # self.E = self.E - end_norm_factor.value
                    self.E_label = end_norm_factor.quantity
                    self.E_unit = end_norm_factor.unit
                    self.E_shifted_by = end_norm_factor.value
                # print("SHIFT:",end_norm_factor)
                else:
                    #shift back to original.
                    # self.E = self.E + self.E_shifted_by
                    self.E_label = "E vs "+ self.RE
                    self.E_unit = self.E_unit = "V" 
                    self.E_shifted_by = None   
            #self.E = self.E + end_norm_factor.value
            # self.E_label = end_norm_factor.quantity
            # self.E_unit = end_norm_factor.unit
                #print("SHIFT:",end_norm_factor,self.E_label)
                if current is not None:
                    if isinstance(current, list) or isinstance(current, tuple):
                        i_shifted = current.copy()
                        for i in range(len(current)):
                            # print("HEJ-shifting",i)
                            i_shifted[i] = self._shift_Current_Array(current[i],end_norm_factor.value)
                    else:
                        i_shifted = self._shift_Current_Array(current,end_norm_factor.value)
                return end_norm_factor.value, i_shifted
        return None
    
    

    
    
    def norm(self, norm_to:str|tuple, current:list):
        """norm_factor = QV(1,)
        if isinstance(norm_to, tuple):
            for arg in norm_to:
                x = self.get_norm_factor(arg)
                if x is not None:   
                    norm_factor = norm_factor * (x)
        else:        
            norm_factor = self.get_norm_factor(norm_to)
        #print(norm_factor)"""
        norm_factor = self.get_norm_factors(norm_to)
        i_shifted = None
        qv = QV(0,"","")
        if norm_factor is not None:
            i_shifted = current.copy()
            if isinstance(current, list):
                i_shifted = current.copy()
                for i in range(len(current)):
                    # print("aaaa-shifting",i)
                    
                    i_shifted[i] = current[i] / float(norm_factor)
            else:
                i_shifted = current / float(norm_factor)
        #norm_factor_inv = norm_factor ** -1
            qv = QV(1, self.i_unit, self.i_label) / norm_factor
            self.i_unit = qv.unit
            self.i_label = qv.quantity
            # print("aaaa-shifting",self.i_unit)
        return i_shifted, qv
    
    
    def _shift_Current_Array(self, array, shift_Voltage):
        """_summary_

        Args:
            array (_type_): _description_
            shift_Voltage (_type_): _description_

        Returns:
            _type_: a copy of the array
        """
        if shift_Voltage is None:
            return array
        self.get_index_of_E(float(shift_Voltage))
        shift_index = self.get_index_of_E(shift_Voltage) - self.get_index_of_E(0)
        if shift_index is None:
            return array
        temp = array.copy()*np.nan
        # max_index = len(array)-1
        # print("shift_arrray",shift_index)
        if shift_index == 0:
            return array
        for i in range(0,len(array)):
            n= i + shift_index
            if n>=0 and n< len(array):
                temp[i]=array[n]
        return temp
    
    
    
    @EC_Setup.RE.setter
    def RE(self, reference_electrode_name:str):
        self.set_RE(reference_electrode_name)
        
    def set_RE(self, reference_electrode_name:str):
        self.setup_data._RE =str(reference_electrode_name)
        # print("FDFDAF")
        return
        
    def update_E_label(self,shift_to):
        if self.E_shifted_by is None :
            self.E_label = shift_to.quantity
            self.E_unit = shift_to.unit
                # print("SHIFT:",end_norm_factor)
        else:
            #shift back to original.
            self.E = self.E + self.E_shifted_by
            self.E_label = "E vs "+ self.RE
            self.E_unit = self.E_unit = "V"   
    
    def get_point_color(self):
        point_color ="bo"
        if self.dir == POS:
            point_color=STYLE_POS_DL
        elif self.dir == NEG:
            point_color = STYLE_NEG_DL
        elif self.dir == AVG:
            point_color = STYLE_AVG_DL
        elif self.dir == DIF:
            point_color = STYLE_DIF_DL
        
        return point_color
            
    def get_line_color(self):
        point_color ="b-"
        if self.dir == POS:
            point_color=STYLE_POS_L
        elif self.dir == NEG:
            point_color = STYLE_NEG_L
        elif self.dir == AVG:
            point_color = STYLE_AVG_L
        elif self.dir == DIF:
            point_color = STYLE_DIF_L
        
        return point_color
            



def create_Levich_data_analysis_plot(data_plot_title:str="data",*args, **kwargs):           
    Tafel_op= {"data_plot": None,ANALYSE_PLOT: None}
    Tafel_op.update(kwargs)
    data_plot = Tafel_op["data_plot"]
    analyse_plot = Tafel_op[ANALYSE_PLOT]
    fig = None
    if Tafel_op["data_plot"] is None and Tafel_op[ANALYSE_PLOT] is None:
        fig = make_plot_2x("Levich Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text(data_plot_title)
        analyse_plot.title.set_text('Levich Plot')
    return data_plot,analyse_plot,fig

def create_KouLev_data_analysis_plot(data_plot_title:str="data",*args, **kwargs):           
    Tafel_op= {"data_plot": None,ANALYSE_PLOT: None}
    Tafel_op.update(kwargs)
    data_plot = Tafel_op["data_plot"]
    analyse_plot = Tafel_op[ANALYSE_PLOT]
    fig = None
    if Tafel_op["data_plot"] is None and Tafel_op[ANALYSE_PLOT] is None:
        fig = make_plot_2x("KouLev Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text(data_plot_title)
        analyse_plot.title.set_text('KouLev Plot')
    return data_plot,analyse_plot,fig          
            
def create_Tafel_data_analysis_plot(data_plot_title:str="data",*args, **kwargs):           
    Tafel_op= {"data_plot": None,ANALYSE_PLOT: None}
    Tafel_op.update(kwargs)
    data_plot = Tafel_op["data_plot"]
    analyse_plot = Tafel_op[ANALYSE_PLOT]
    fig = None
    if Tafel_op["data_plot"] is None and Tafel_op[ANALYSE_PLOT] is None:
        fig = make_plot_2x("Tafel Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text(data_plot_title)
        analyse_plot.title.set_text('Tafel Plot')
    return data_plot,analyse_plot,fig

def create_RanSev_data_analysis_plot(data_plot_title:str="data",*args, **kwargs):           
    Tafel_op= {"data_plot": None,"analyse_plot": None}
    Tafel_op.update(kwargs)
    data_plot = Tafel_op["data_plot"]
    analyse_plot = Tafel_op["analyse_plot"]
    fig = None
    if Tafel_op["data_plot"] is None and Tafel_op["analyse_plot"] is None:
        fig = make_plot_2x("RanSev Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text(data_plot_title)
        analyse_plot.title.set_text('RanSev Plot')
    return data_plot,analyse_plot,fig

def create_Rate_data_analysis_plot(data_plot_title:str="data",*args, **kwargs):           
    op= {"data_plot": None,"analyse_plot": None}
    op.update(kwargs)
    data_plot = op["data_plot"]
    analyse_plot = op["analyse_plot"]
    if op["data_plot"] is None and op["analyse_plot"] is None:
        fig = make_plot_2x("Rate Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text(data_plot_title)
        analyse_plot.title.set_text('Rate Plot')
    return data_plot,analyse_plot,fig