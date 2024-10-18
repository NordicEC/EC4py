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

from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x
from .analysis_tafel import Tafel
from .analysis_levich import diffusion_limit_corr

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data(EC_Setup):
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
        self.E=[]
        self.i=[]
        self.i_label = "i"
        self.i_unit = "A"
        self.dir =""
        self.rate_V_s = 1

        """max voltage""" 
        self.E_min = -2.5
        """min voltage"""
        ##self.name="CV" name is given in the setup.
        self.xmin = -2.5
        self.xmax = 2.5
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]),**kwargs)
    #############################################################################   
    def sub(self, subData: LSV_Data) -> None:
        try:
            self.i = self.i-subData.i
            
        finally:
            return
    #############################################################################
    def __mul__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.i = new_lsv.i * other
        return new_lsv
    #############################################################################
    def __div__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        
        new_lsv.i = new_lsv.i / other
        return new_lsv
    #############################################################################    
    def div(self, div_factor:float):
        """_summary_

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        try:
            self.i = self.i / div_factor
             
        finally:
            return
    #############################################################################
    def __add__(self, other: LSV_Data):
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Data: returns a copy of the inital dataset. 
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.i = new_lsv.i + other.i
         
        return new_lsv
    #############################################################################
    def __sub__(self, other: LSV_Data):
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Data: returns a copy of the inital dataset. 
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.i = (new_lsv.i - other.i).copy()
         
        return new_lsv
    
    #####################################################################################################
    def add(self, subData: LSV_Data):
        try:
            self.i = self.i+subData.i
        finally:
            pass
        return

    #####################################################################################################    
    def smooth(self, smooth_width:int):
        try:
            self.i = savgol_filter(self.i, smooth_width, 1)    
        finally:
            return


    #####################################################################################################
    def set_area(self, value,unit):
        self.setup_data._area = value
        self.setup_data._area_unit = unit

    ######################################################################################################
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a LSV

        Args:
            ec_data (EC_Data): the data that should be converted.
        """
        #print("Convert:",kwargs)
        
        ch_E ="E"
        for a in args:
            if a == "IR":
                ch_E = "E-IR"
        options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'IR': 0
        }
        options.update(kwargs)
        
        try:
            #print("CONVERTING_AAA",len(ec_data.Time), len(ec_data.E), len(ec_data.i))
            self.setup_data = copy.deepcopy(ec_data.setup_data)
            self.convert(ec_data.Time,ec_data.E,ec_data.i,**kwargs)

        except ValueError:
            print("no_data")
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return

    #####################################################################################################    
    def convert(self, time, E, i, V0= None, V1 = None, Rate_V_s_ = None, **kwargs):
        """Converts data to a voltammogram, i.e. resampling the data to a evently spaced E.

        Args:
            time (_type_): time
            E (_type_): potential
            i (_type_): current
            direction(str): direction
        """
        x= E
        y= i

        if V0 is None:
            V0, V0_str = extract_value_unit(self.setup['Start'])

        if V1 is None:
            V1, V1_str = extract_value_unit(self.setup['V1'])

        options = plot_options(kwargs)

        positive_start = False
        positive_start = V0 < V1
        #print("startDIR:", positive_start)

        y = options.smooth_y(y)

        self.xmin = x.min()
        self.xmax = x.max()
        #array of dx
        if(len(x)>10):
            x_div = np.gradient(savgol_filter(x, 10, 1))
        else:
            x_div = np.gradient(x)
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        #print("ZERO:",zero_crossings)
        if Rate_V_s_ is None:
            self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        else:
            self.rate_V_s = Rate_V_s_
        #print(f"Rate: {self.rate_V_s}")
        if(len(zero_crossings)==0):
            zero_crossings =[len(time)-1]
            print("APPEN DING")
        self.E_max = 2.5
        self.E_min = -2.5
        dE_range = int((self.E_max - self.E_min)*1000)
        x_sweep = np.linspace(self.E_min, self.E_max, dE_range) 
        self.E = x_sweep
        print("zero_crossings",zero_crossings)
        if positive_start:
            x_sub = x[0:zero_crossings[0]]
            y_sub = y[0:zero_crossings[0]]
        else:
            x_sub = np.flipud(x[0:zero_crossings[0]])
            y_sub = np.flipud(y[0:zero_crossings[0]])

        y_pos=np.interp(x_sweep, x_sub, y_sub)

        for index in range(1,y_pos.size):
            if y_pos[index-1] == y_pos[index]:
                y_pos[index-1] = math.nan
            else :
                break
            
        for index in range(y_pos.size-2,0,-1):
            if y_pos[index] == y_pos[index+1]:
                y_pos[index+1] = math.nan
            else :
                break
            
        self.i = y_pos     
    
   ######################################################################################### 
    def norm(self, norm_to:str):
         
        norm_factor = self.get_norm_factor(norm_to)
        #print(norm_factor)
        if norm_factor:
            self.i = self.i / float(norm_factor)
             
        #norm_factor_inv = norm_factor ** -1
            current = Q_V(1,self.i_unit, self.i_label) / norm_factor
         
            self.i_label = current.quantity
            self.i_unit = current.unit
        
        return 
    
    ############################################################################        
    def plot(self,**kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot=subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        '''
        
        options = plot_options(kwargs)
        options.set_title(self.setup_data.name)
        options.name = self.setup_data.name
        options.legend = self.legend(**kwargs)
        
        options.x_data = self.E
        options.y_data = self.i
                
        options.set_x_txt("E", "V")
        options.set_y_txt(self.i_label, self.i_unit) 
        
        return options.exe()
    
    ####################################################################################################
    def get_index_of_E(self, E:float):
        index = 0
        for x in self.E:
            if x > E:
                break
            else:
                index = index + 1
        return index
    
    ########################################################################################################
    def get_i_at_E(self, E:float, dir:str = "all"):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            _type_: _description_
        """
        index = self.get_index_of_E(E)
                
        return self.i[index]
    ###########################################################################################

    def integrate(self, start_E:float, end_E:float, dir:str = "all", show_plot: bool = False, *args, **kwargs):
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
        i = self.i[imin:imax+1].copy()
        i[np.isnan(i)] = 0
       
        array_Q = integrate.cumulative_simpson(i, x=self.E[imin:imax+1], initial=0) / float(self.rate)    
        
        Q_unit =self.i_unit.replace("A","C")
        #yn= np.concatenate(i_p,i_n,axis=0)
        
        y = [np.max(i), np.min(i)]
        x1 = [self.E[imin],self.E[imin]]
        x2 = [self.E[imax+1],self.E[imax+1]]  
        dataPlot_kwargs = kwargs  
        if show_plot:
            dataPlot_kwargs["dir"] = dir
            line, ax = self.plot(**dataPlot_kwargs)
            ax.plot(x1,y,'r',x2,y,'r')
           
            ax.fill_between(self.E[imin:imax+1],i,color='C0',alpha=0.2)
           
            
        #except ValueError as e:
        #    print("the integration did not work on this dataset")
        #    return None
        end = len(array_Q)-1
        Q = Q_V(array_Q[end]-array_Q[0],Q_unit,"Q")        
         
        print(Q)
        
        return Q
        
   ##################################################################################################################
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        Tafel_op= {"LSV_plot": None,"analyse_plot": None}
        Tafel_op.update(kwargs)
        data_plot = Tafel_op["LSV_plot"]
        analyse_plot = Tafel_op["analyse_plot"]
        if Tafel_op["LSV_plot"] is None and Tafel_op["analyse_plot"] is None:
            fig = make_plot_2x("Tafel Analysis")
            data_plot = fig.plots[0]
            analyse_plot =  fig.plots[1]
            data_plot.title.set_text('LSV')
            analyse_plot.title.set_text('Tafel Plot')
            
        
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        LSV = copy.deepcopy(self)
        lsv_kwargs = kwargs
        plot_color2= []
        
        rot.append( math.sqrt(LSV.rotation))
    
        for arg in args:
            #if arg == "area":
            LSV.norm(arg)
        lsv_kwargs["legend"] = str(f"{float(LSV.rotation):.0f}")
        lsv_kwargs["plot"] = data_plot
        line,a = LSV.plot(**lsv_kwargs)
        plot_color2.append(line.get_color())
        plot_color =line.get_color()
        #.get_color()
        #color = line.get_color()
        xmin = LSV.get_index_of_E(min(lims))
        xmax = LSV.get_index_of_E(max(lims))
            
            
            
        if E_for_idl != None:
            i_dl = LSV.get_i_at_E(E_for_idl)
            y.append(LSV.get_i_at_E(E_for_idl))
            E.append(E_for_idl)
            with np.errstate(divide='ignore'):
                y_data = [math.log10(abs(1/(1/i-1/i_dl))) for i in LSV.i]
        else:
            y_data = [math.log10(abs(i)) for i in LSV.i]
            
                
        Tafel_slope = Tafel(LSV.E[xmin:xmax],y_data[xmin:xmax],LSV.i_unit,LSV.i_label,plot_color,"Pos",LSV.E, y_data,plot=analyse_plot)
       
        y_values = np.array(y)
        if E_for_idl is not None:
            data_plot.plot(E,y_values[:,0], STYLE_POS_DL, E,y_values[:,1],STYLE_NEG_DL)
        data_plot.legend()
    
        return Tafel_slope