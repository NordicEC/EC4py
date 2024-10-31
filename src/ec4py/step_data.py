""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data,index_at_time

from .ec_setup import EC_Setup
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,make_plot_2x_1,saveFig
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV
from .analysis_tafel import Tafel


#from .step_datas import Step_Datas

class Step_Data(EC_Setup):

    def __init__(self,*args, **kwargs):
        super().__init__()
        #self._area=2
        #self._area_unit="cm^2"
        #self.rotation =0
        #self.rotation_unit ="/min"
        self.Time=np.array([],dtype=np.float64)
        self.E=np.array([],dtype=np.float64)
        self.i=np.array([],dtype=np.float64)
        self.i_label = "i"
        self.i_unit = "A"
        self.E_label = "E"
        self.E_unit = "V"
        self.step_Time =[]
        self.step_E =[]
        self.step_Type =[]
        self.E_shifted_by = None
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]),**kwargs)
    #############################################################################   
    def __getitem__(self, item_index:int|slice) -> Step_Data: 
        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.step_Time)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop 
            
            return [self.get_step(i) for i in range(start,stop,step)]
        else:
            return self.get_step(item_index)
    ###########################################
    @property 
    def repetitions(self):
        """setup meta data

        Returns:
            dict[]: list of key words
        """
        return self.setup_data._setup["Repetitions"]
    
    @property 
    def nr_of_steps(self):
        """setup meta data

        Returns:
            dict[]: list of key words
        """
        return int(self.setup_data._setup["Repetitions"])*len(self.step_Time)
    ##########################       
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a CV

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
            self.setup_data = ec_data.setup_data
            #self.convert(ec_data.Time,ec_data.E,ec_data.i,**kwargs)
            self.Time = ec_data.Time
            self.i =ec_data.i
            self.E = ec_data.E
            
            #self.step_Time = self.setup["Step.Time"].split(";",-1)
            #self.step_E = self.setup["Step.E"].split(";",-1)
            #self.step_Type = self.setup_data._setup["Step.Type"].split(";",-1)
            self.step_Time = List_Str2float(self.setup["Step.Time"])
            self.step_E =List_Str2float(self.setup["Step.E"])
            self.step_Type = List_Str2Str(self.setup["Step.Type"])
            self.E_label = "E vs " + self.RE
        except ValueError:
            print("no_data")
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return
    
    def plot(self, x_channel:str="Time", y_channel:str="i", *args, **kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot = subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        '''
        #xlable ="wrong channel name"
        #xunit = "wrong channel name"
        #ylable ="wrong channel name"
        #yunit = "wrong channel name"
        
        range = {
            'limit_min' : -1,
            'limit_max' : -1   
        }
        range.update(kwargs)
        #print(kwargs)
        #print(range)
        options = plot_options(kwargs)
        data = copy.deepcopy(self)
        
        # print("plotARGS",args)
        data.norm(args)
        data.set_active_RE(args)
        # print("QQQQ",data.E_label)
        index_min = 0
        if range["limit_min"] >0:
            index_min = data.index_at_time(range["limit_min"])
        index_max = len(data.Time)-1
        if range["limit_max"] >0:
            index_max = data.index_at_time(range["limit_max"])
        
        #max_index = len(self.Time)-1
        #print("index", index_min,index_max)
        try:
            x_data, options.x_label, options.x_unit = data.Time,"t","s"
            options.x_data = x_data[index_min:index_max]
        except NameError:
            print(f"xchannel {x_channel} not supported")
        try:
            if y_channel =='E':
                y_data, options.y_label, options.y_unit = data.E,data.E_label,data.E_unit
            else:
                y_data, options.y_label, options.y_unit = data.i,data.i_label,data.i_unit
            options.y_data = y_data[index_min:index_max]
        except NameError:
            print(f"ychannel {y_channel} not supported")

        return options.exe()
        ##################################################################################################################

    def index_at_time(self, time_s_:float):
        return index_at_time(self.Time, time_s_)
       ##################################################################################################################
    def get_current_at_time(self, time_s_:float, dt_s_:float = 0):
        current = 0.0
        if dt_s_ == 0:
            index = self.index_at_time(time_s_)
            current = self.i[index]
        else:
            index_low = self.index_at_time(time_s_-dt_s_ /2)
            index_high = self.index_at_time(time_s_+ dt_s_ /2)
            current = np.average(current[index_low, index_high])
        return current
       ##################################################################################################################
    
    
    def get_step(self,step_index:int, steprange:int = 1):
        singleStep = Step_Data()
        singleStep.setup_data = copy.deepcopy(self.setup_data)
        singleStep.setup_data.name =str(self.setup_data.name)  + '#' + str(step_index)
        #print(self.step_Time)
        total_nr_steps = len(self.step_Time)
        s=[0.0]
        for i in range(0, total_nr_steps):
            num =float(self.step_Time[i])
            s.append(s[i]+num)
        #print(s)
        idx = step_index % total_nr_steps
       # print("total", total_nr_steps)
       # print("idx", idx)
        multi = math.floor(step_index / total_nr_steps)
      #  print("multi", multi)
        extra = s[total_nr_steps]*multi
      #  print("extra", extra)
        startT = s[idx]
        endT = s[idx+steprange]
         
     #   print("startT",startT)
      #  print("endT",endT)
        
        
        
        start_index = self.index_at_time(startT+extra)-1
        if start_index< 0 : 
            start_index = 0
        end_index =   self.index_at_time(endT+extra)-1
        #shift dateTime
        singleStep.setup_data.dateTime = self.setup_data.dateTime + np.timedelta64(int(self.Time[start_index]*1000000),'us')
      #  print("startT",start_index)
     #   print("endT",end_index)
        aSize=end_index-start_index #+1
        singleStep.E = np.empty(aSize) 
        singleStep.i = np.empty(aSize) 
        singleStep.Time = np.empty(aSize)    
        np.copyto(singleStep.E, self.E[start_index:end_index])
        np.copyto(singleStep.i, self.i[start_index:end_index])
        np.copyto(singleStep.Time, self.Time[start_index:end_index]-self.Time[start_index])
        #print(idx)
        singleStep.step_Time =[singleStep.Time.max()]
        singleStep.step_E =[self.step_E[idx]]
        singleStep.step_Type =[self.step_Type[idx]]
        
        singleStep.E_label=self.E_label
        singleStep.E_unit =self.E_unit
        singleStep.i_label=self.i_label
        singleStep.i_unit =self.i_unit
        return singleStep
    
    #########################################################################################
       
    def append(self, step_to_append:Step_Data, use_DateTime=True):
        """Append a step to another step.

        Args:
            step_to_append (Step_Data): Step to be appended.
            use_DateTime (bool, optional): _description_. Defaults to True.
        """
        self.E= np.append(self.E, step_to_append.E)
        self.i=np.append(self.i, step_to_append.i)
        dt = (step_to_append.setup_data.dateTime-self.setup_data.dateTime) / np.timedelta64(1,'us') /1.0e6
        print("dt", dt , len(step_to_append.Time+ dt))
        step_to_append.Time[0]=np.nan
        self.Time=np.append(self.Time, (step_to_append.Time+ dt ))
        
    #########################################################################################

       
        
    def norm(self, norm_to:str|tuple):
        end_norm_factor = 1
        current = QV(1,self.i_unit, self.i_label)
        # print("argeLIST", type(norm_to))
        if isinstance(norm_to, tuple):
           
            for item in norm_to:
                # print("ITTTT",item)
                norm_factor = self.get_norm_factor(item)
                if norm_factor:
                    end_norm_factor= end_norm_factor * float(norm_factor)
                    current = current / norm_factor
                
                
        else:
            norm_factor = self.get_norm_factor(norm_to)
            #print(norm_factor)
            if norm_factor:
                end_norm_factor = end_norm_factor* float(norm_factor)
                current = current / norm_factor
                
            #norm_factor_inv = norm_factor ** -1
            
        if(end_norm_factor!= 1):
            self.i = self.i / float(norm_factor)   
            self.i_label = current.quantity
            self.i_unit = current.unit
        
        return 
    
    def set_active_RE(self,shift_to:str|tuple):
        """Set active Reference electrode for plotting

        Args:
            shift_to (str | tuple): use RHE, SHE

        Returns:
            _type_: _description_
        """
        end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        last_Active_RE = self.setup_data.getACTIVE_RE()
        end_norm_factor = EC_Setup.set_active_RE(self, shift_to)
    
        self.E_label = "E vs "+ self.setup_data.getACTIVE_RE()      
        if end_norm_factor is not None:
            if  self.E_shifted_by == end_norm_factor.value :  
                pass #potential is already shifted.
            else:
                if self.E_shifted_by is None :
                    self.E_label = end_norm_factor.quantity
                    self.E_unit = end_norm_factor.unit
                    self.E_shifted_by = end_norm_factor.value
                    self.E = self.E - self.E_shifted_by
                else:
                    self.E_label = "fdsdE vs "+ self.RE
                    self.E_unit = self.E_unit = "V" 
                    self.E = self.E + self.E_shifted_by
                    self.E_shifted_by = None   
        
                
                return end_norm_factor.value
        return None
    
    def integrate(self,t_start:float,t_end:float, step_nr:int = -1, *args, **kwargs):
        """_summary_

        Args:
            t_start (_type_): start time for integration
            t_end (_type_): end time for the integration

        Returns:
            Quantity_Value_Unit: Integrated charge including the unit.
        """
        
        idxmin=self.index_at_time(t_start)
        idxmax=self.index_at_time(t_end)+1
        
        data_kwargs = kwargs
        #print(kwargs)
        fig = None
        if 'plot_i' in data_kwargs:
            data_plot_i = data_kwargs["plot_i"]
            data_plot_E = data_kwargs["plot_E"]
            analyse_plot = data_kwargs["analyse_plot"]
            # print("plots are there")
        else:
            fig = make_plot_2x_1("Integrate Analysis")
            data_plot_i = fig.plots[0]
            data_plot_E = fig.plots[1]
            analyse_plot =  fig.plots[2]
            #data_plot_i,data_plot_E, analyse_plot = make_plot_2x_1("Integrate Analysis")
            #########################################################
            # Make plot
            data_kwargs = kwargs
            data_kwargs["plot_i"] = data_plot_i
            data_kwargs["plot_E"] = data_plot_E
            data_plot_i.axvspan(self.Time[idxmin], self.Time[idxmax], color='C0', alpha=0.2)
        
        if(step_nr>-1):
                step = self.get_step(step_nr)
        else:
                step= copy.deepcopy(self)     
        
        l_i, ax1 = step.plot("Time", "i", plot=data_plot_i, *args, **data_kwargs)
        l_E, ax2 = step.plot("Time", "E", plot=data_plot_E, *args, **data_kwargs)
        
        #ax1.label_outer()
        #ax2.label_outer()
       # for arg in args:
            #if arg == "area":
       #     cv.norm(arg)
        #y,quantity,unit = self.get_channel(y_channel)
        #print("befre",step.i_unit)
        step.norm(args)
        step.set_active_RE(args)
        #print(step.i_unit,args)
        array_Q = integrate.cumulative_simpson(step.i[idxmin:idxmax], x=step.Time[idxmin:idxmax], initial=0)
        Charge = QV(array_Q[len(array_Q)-1]-array_Q[0],step.i_unit.replace("A","C"),self.i_label.replace("i","Q")) #* QV(1,"s","t")
        
        options = plot_options(kwargs)
        options.options["plot"] = analyse_plot
        options.x_data = step.Time[idxmin:idxmax]
        options.x_label, options.x_unit = "t", "s"
        options.y_label, options.y_unit = "Q", Charge.unit
        options.y_data = array_Q
        #analyse_plot.plot(self.Time[idxmin:idxmax], array_Q)
        #Charge = QV(array_Q[len(array_Q)-1]-array_Q[0],self.i_unit,self.i_label)* QV(1,"s","t")
        options.exe()
        saveFig(fig,**kwargs)
        return Charge
    
    
    def Tafel(self, lims=[-1,1], *args, **kwargs):
        x_data =np.empty(self.nr_of_steps)
        y_data =np.empty(self.nr_of_steps)
        for i in self.nr_of_steps:
            singleStep = self.get_step[i]
            maxIndex = len(singleStep.Time)-1
            x_data[i] = singleStep.E[maxIndex]
            y_data[i] = singleStep.i[maxIndex]
        return Tafel(x_data, y_data, self.i_unit, self.i_label,  **kwargs)
##END OF CLASS
########################################################################################## 

##HELP FUNCTIONS       
def List_Str2float(list_str:str):
    LIST = list_str.split(";",-1)
    length = len(LIST)
    for i in range(length):
        idx = length-i-1
        s=LIST[idx].strip()
        if(len(s)==0):
            LIST.pop(idx)
    length = len(LIST)
    for i in range(length):
        LIST[i] = float(LIST[i])
    return LIST

def List_Str2Str(list_str:str):
    LIST = list_str.split(";",-1)
    length = len(LIST)
    for i in range(length):
        idx = length-i-1
        s=LIST[idx].strip()
        if(len(s)==0):
            LIST.pop(idx)
    length = len(LIST)
    for i in range(length):
        LIST[i] = str(LIST[i]).strip()
    return LIST
 
 