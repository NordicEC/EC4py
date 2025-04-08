""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
# from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data
from .ec_data_util import EC_Channels
from .util_voltammetry import Voltammetry, OFFSET_AT_E_MIN, OFFSET_AT_E_MAX, OFFSET_LINE,create_Tafel_data_analysis_plot
from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,should_plot_be_made
from .analysis_tafel import Tafel
from .analysis_levich import diffusion_limit_corr

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Data(Voltammetry):
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
        self.i=[]
        self.i_label = "i"
        self.i_unit = "A"
       
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
            self.conv(EC_Data(args[0]),*args, **kwargs)
  
  
    #############################################################################
    def __add__(self, other: LSV_Data) -> LSV_Data:
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Data: returns a copy of the inital dataset. 
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.add(other)
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
        new_lsv.sub(other)
        return new_lsv
    #############################################################################
    def __mul__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.mul(other)
        return new_lsv
    
    #############################################################################
    def __truediv__(self, other):
        """ 

        Returns:
            LSV_Data: a copy of the original data
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.div(other)
        return new_lsv
   
    #####################################################################################################
    def add(self, addData: LSV_Data) -> None:
        """Add a LSV_Data or a number to the current data"""
        if isinstance(addData, LSV_Data):    
            self.i = self.i+addData.i
        else: 
            number = float(addData)
            self.i = self.i + number
        #print("ADD",self.i,addData.i)
        #raise TypeError("Addition is only possible with LSV_Data or number")

  #############################################################################   
    def sub(self, subData: LSV_Data) -> None:
        """Add a LSV_Data or a number to the current data"""
        if isinstance(subData, LSV_Data):    
            self.i = self.i-subData.i
        else:
            number = float(subData)
            self.i = self.i - number
    #############################################################################    
    def mul(self, factor:float):
        """Multiply the current by a factor

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        self.i = self.i * float(factor)
        #else:
        #    raise TypeError("Multiplication is only possible with a number")    
 #############################################################################    
    def div(self, factor:float):
        """Divide the current by a factor

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        self.i = self.i / float(factor)
        #else:
        #    raise TypeError("Division is only possible with a number")
         
    #####################################################################################################    
    def smooth(self, smooth_width:int):
        try:
            self.i = self._smooth(self.i, smooth_width)    
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
        sel_channels = EC_Channels(*args,**kwargs)
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
    def norm(self, norm_to:str| tuple):
        """Normalize lsv current

        Args:
            norm_to (str): _description_
        """
        
        r,qv = Voltammetry.norm(self, norm_to,[self.i ] )
        #print("CCCC",r)
        #print("CCCC",qv)
                #n = Voltammetry.norm(self, norm_to,self.i_n )
        
        if r is not None:
            v= r[0]
            #print("AAAAAAA",v)
            #print("BBBBBBB",v)
            if v is not None:
                self.i = v
        return 
        
    
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
            options = plot_options(kwargs)
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
    
    
    def set_active_RE(self,shift_to:str|tuple = None):
        end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        a = Voltammetry.set_active_RE(self,shift_to, [self.i])
        if a is not None:
            a,b = a
            self.i = b[0]
            # print("pot_shift",a, "REEE",self.E_label)
        return 
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero and adjust the rest of the current.

        Args:
            E (float): potential where to set the current to zero.
        """
        new_lsv = copy.deepcopy(self)
        new_lsv.set_active_RE(args)
        current = new_lsv.get_i_at_E(E,*args,**kwargs)
        self.sub(current)
    
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
    def get_i_at_E(self, E:float, *args,**kwargs):
        """Get the current at a specific voltage. The current can be normalized. 

        Args:
            E (float): potential where to get the current. 
        Returns:
             Quantity_Value_Unit: The current, units and label.
        """
        lsv = copy.deepcopy(self)
        lsv.norm(args)
        lsv.set_active_RE(args)  
        smooth_length = kwargs.get("y_smooth",None)
        if smooth_length is not None:
            lsv.smooth(smooth_length)
        
        index = self.get_index_of_E(E)
                
        return QV(lsv.i[index],lsv.i_unit,lsv.i_label)
    ###########################################################################################

    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
             (Quantity_Value_Unit | None): _description_
        """
        
        index1 = self.get_index_of_E(E1)
        index2 = self.get_index_of_E(E2)
        index_max=max(index1,index2)
        index_min=min(index1,index2)
        #print(index_min,index_max)
        index_of_max=index_min
        max_i =-1e100
        for index in range(index_min,index_max):
            if max_i<self.i[index] and not np.isnan(self.i[index]) :
                index_of_max = index
                max_i =self.i[index]
        if max_i > -1e100:    
            index_E = index_of_max
            #index_E = self.i[index_min:index_max].argmax()
            #print("index",index_E,"E", self.E[index_E])
            return QV(self.E[index_E],self.E_unit,self.E_label)
        else:
            return None
    ###########################################################################################

    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of minimum current in a range.

        Args:
            E1 (float): Start potential
            E2 (float): End potential

        Returns:
           (Quantity_Value_Unit | None): The voltage of min, or None, if not found
        """
                
        index1 = self.get_index_of_E(E1)
        index2 = self.get_index_of_E(E2)
        index_max=max(index1,index2)
        index_min=min(index1,index2)
        #print(index_min,index_max)
        index_of_min=index_min
        min_i =1e100
        for index in range(index_min,index_max):
            if self.i[index]<min_i and not np.isnan(self.i[index]) :
                index_of_min = index
                min_i =self.i[index]
        if min_i < 1e100:    
            index_E = index_of_min
            #index_E = self.i[index_min:index_max].argmax()
            #print("index",index_E,"E", self.E[index_E])
            return QV(self.E[index_E],self.E_unit,self.E_label)
        else:
            return None
    
    ##################################################################################################
    
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
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        
        data_plot,analyse_plot,fig = create_Tafel_data_analysis_plot('LSV',**kwargs)
        
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
        if E_for_idl != None:
            i_dl = lsv.get_i_at_E(E_for_idl)
            y.append(lsv.get_i_at_E(E_for_idl))
            E.append(E_for_idl)
            
            y_data =(np.abs(diffusion_limit_corr(lsv.i,i_dl)))
          
        else:
            y_data = lsv.i 
            
        Tafel_slope = Tafel(lsv.E[xmin:xmax],y_data[xmin:xmax],lsv.i_unit,lsv.i_label,plot_color,lsv.dir,lsv.E, y_data,plot=analyse_plot, x_label = "E vs "+ self.setup_data.getACTIVE_RE())
       
        y_values = np.array(y)
        if E_for_idl is not None:
            data_plot.plot(E,y_values, STYLE_POS_DL)
        data_plot.legend()
    
        return Tafel_slope
    
    
    def export_DataFrame(self):
        size = [len(Voltammetry().E),2]
        m = np.zeros(size)
        col_names= list("E")
        #print(m.shape,len(self.datas))
        m[:,0]=Voltammetry().E
        
        
            #print(x,self.datas[x].i.shape)
        m[:,1] = self.i
        col_names.append(f"{self.i_label}_{self.name} / {self.i_unit}")
        #print(col_names)
        df = pd.DataFrame.from_records(m,columns=col_names)
        return df