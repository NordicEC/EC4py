""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
# from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data
from .ec_data_util import EC_Channels

from .lsv_data import LSV_Data

from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV
from .util_voltammetry import Voltammetry, OFFSET_AT_E_MIN, OFFSET_AT_E_MAX, OFFSET_LINE,create_Tafel_data_analysis_plot,POS,NEG,AVG,DIF


from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig, LEGEND
from .analysis_tafel import Tafel
from .analysis_levich import diffusion_limit_corr

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

#POS = "pos"
#NEG = "neg"
#AVG = "avg"
#DIF = "dif"

class CV_Data(Voltammetry):
    """# Class to analyze a single CV data. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.
    
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
        Voltammetry.__init__(self, *args, **kwargs)
        # self.E=[]
        self.i_p=[]
        self.i_n=[]

        """max voltage""" 
        # self.E_max = -2.5
        """min voltage"""
        # self.E_min = -2.5
        """self.E_axis = {
                    "E_min" : -2.5,
                    "E_max" :  2.5 
                    }
                    
        self.E_axis.update(kwargs)
        """
        # self.xmin = -2.5 # View range
        # self.xmax = 2.5  # view renage
        
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]), *args, **kwargs)

    #########################################   
    def sub(self, subData: CV_Data) -> None:
        try:
            self.i_p = self.i_p-subData.i_p
            self.i_n = self.i_n-subData.i_n
        finally:
            return
    #############################################################################
    def __mul__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = copy.deepcopy(self)
        new_cv.i_p = new_cv.i_p * other
        new_cv.i_n = new_cv.i_n * other
        return new_cv
    #############################################################################
    def __div__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = copy.deepcopy(self)
        new_cv.i_p = new_cv.i_p / other
        new_cv.i_n = new_cv.i_n / other
        return new_cv
    #############################################################################    
    def div(self, div_factor:float):
        """_summary_

        Args:
            div_factor (float): div the current dataset with the factor.
        """
        try:
            self.i_p = self.i_p / div_factor
            self.i_n = self.i_n / div_factor
        finally:
            return
    #############################################################################
    def __add__(self, other: CV_Data):
        """_summary_

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Data: returns a copy of the inital dataset. 
        """
        new_cv = copy.deepcopy(self)
        new_cv.i_p = new_cv.i_p + other.i_p
        new_cv.i_n = new_cv.i_n + other.i_n
        return new_cv
    #############################################################################
    def __sub__(self, other: CV_Data):
        """_summary_

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Data: returns a copy of the inital dataset. 
        """
        new_cv = copy.deepcopy(self)
        new_cv.i_p = (new_cv.i_p - other.i_p).copy()
        new_cv.i_n = new_cv.i_n - other.i_n
        return new_cv
    
    #####################################################################################################
    def add(self, subData: CV_Data):
        try:
            self.i_p = self.i_p+subData.i_p
        finally:
            pass
        try:
            self.i_n = self.i_n+subData.i_n
        finally:
            pass
        return

    #####################################################################################################    
    def smooth(self, smooth_width:int):
        try:
            self.i_p = self._smooth(self.i_p,smooth_width)
            self.i_n = self._smooth(self.i_n,smooth_width)      
        finally:
            return


    ######################################################################################################
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
            'IR': 0,
            'E' : "E",
            'i' : 'i'
        }
        options.update(kwargs)
        sel_channels = EC_Channels(*args,**kwargs)

        try:
            data_E,q,u = ec_data.get_channel(sel_channels.Voltage)
            data_i,q,u = ec_data.get_channel(sel_channels.Current)
        except NameError as e:
            print(e)
            raise NameError(e)
            return
            
        try:
            self.setup_data = copy.deepcopy(ec_data.setup_data)
            self.convert(ec_data.Time,data_E,data_i,**kwargs)
            if 'Ref.Electrode' in self.setup:
                self.E_label = "E vs " + self.RE
                #print("aaaaa")
            else:
                self.E_label ="E"

        except ValueError:
            if(self.is_MWE):
                print("select a current channel")
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
        #print("CV", V0,V1,V2)
        options = plot_options(kwargs)
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

        x_start = np.mean(x[0:3])
        index_min = np.argmin(x)
        index_max = np.argmax(x)

        #array of dx

        x_div = np.gradient(savgol_filter(x, 10, 1))
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        #print("ZERO:",zero_crossings)
        self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        #print(f"Rate: {self.rate_V_s}")
        up_start =0
        up_end = 0



        #print(f"ZeroCrossings: {zero_crossings}")
        #print(zero_crossings)
        if x[0]<x[zero_crossings[0]]:
            up_start =0
            up_end = zero_crossings[0]
            dn_start = zero_crossings[0]
            dn_end = x.size

        else:
            up_start =zero_crossings[0]
            up_end = x.size
            dn_start = 0
            dn_end = zero_crossings[0]
            reversed=True

        """
        self.E_max = 2.5
        self.E_min = -2.5
        dE_range = int((self.E_max - self.E_min)*1000)
        x_sweep = np.linspace(self.E_min, self.E_max, dE_range) 
        
        self.E = x_sweep
        """
        # make E axis.
        self.E = self.make_E_axis()

        if positive_start:
            x_u = x[0:zero_crossings[0]]
            y_u = y[0:zero_crossings[0]]
            x_n = np.flipud(x[zero_crossings[0]:])
            y_n = np.flipud(y[zero_crossings[0]:])
        else:
            #print("neg first sweep")
            x_n = np.flipud(x[0:zero_crossings[0]])
            y_n = np.flipud(y[0:zero_crossings[0]])
            x_u = x[zero_crossings[0]:]
            y_u = y[zero_crossings[0]:]

        #y_pos=np.interp(x_sweep, x_u, y_u)
        #y_neg=np.interp(x_sweep, x_n, y_n)
        y_pos=self.interpolate(x_u, y_u)
        y_neg=self.interpolate(x_n, y_n)
        self.i_p = self.clean_up_edges(y_pos)
        self.i_n = self.clean_up_edges(y_neg)
        
   ######################################################################################### 
    def norm(self, norm_to:str|tuple):
        """Normalise the current to certain factors. 

        Args:
            norm_to (str | tuple): _description_

        Returns:
            _type_: _description_
        """
        r = Voltammetry.norm(self, norm_to,[self.i_p,self.i_n ] )
        #n = Voltammetry.norm(self, norm_to,self.i_n )
        if r is not None:
            v= r[0]
            self.i_p = v[0]
            self.i_n = v[1]
            
        return 
    ###############################
    ###under deve
    def set_active_RE(self,shift_to:str|tuple = None):
        end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        a = Voltammetry.set_active_RE(self,shift_to, [self.i_p, self.i_n])
        if a is not None:
            a,b = a
            self.i_p = b[0]
            self.i_n = b[1]
            # print("pot_shift",a, "REEE",self.E_label)
        return 
    
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
        
        dir = Voltammetry()._direction(*args,**kwargs)
        if dir == POS or dir == NEG or dir == AVG or dir == DIF:
            lsv = self.get_sweep(dir)
            return lsv.plot(*args,**kwargs)
        
        data = copy.deepcopy(self)
        options = plot_options(kwargs)
        options.options["dir"]=dir
        #print("AAAAAAAAAAAAAAAAAAAAAAA")
        #print(options.get_y_smooth())
        # print(options.get_legend(),self.legend(**kwargs))
        
        options.set_title(data.setup_data.name)
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
        
        # print(options.get_legend())
        #print("AAAAAAAAAAAAAAAAAAAAAAA")
        #print(options.get_y_smooth())
        return options.exe()
    
    ####################################################################################################
    """def get_index_of_E(self, E:float):
        index = 0
        for x in self.E:
            if x > E:
                break
            else:
                index = index + 1
        return index
    """
    ########################################################################################################
    def get_i_at_E(self, E:float, dir:str = "all",*args, **kwargs):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            float: current
        """
        
        
        cv = copy.deepcopy(self)
        cv.norm(args)
        cv.set_active_RE(args)  
        smooth_length = kwargs.get("y_smooth",None)
        if smooth_length is not None:
            cv.smooth(smooth_length)
        index = cv.get_index_of_E(E)
        # print("INDEX",index,cv.i_n[index],cv.i_unit)
        # print(cv.get_sweep(NEG).get_i_at_E(1.4))
        i_p = QV(cv.i_p[index],cv.i_unit,cv.i_label)
        i_n = QV(cv.i_n[index],cv.i_unit,cv.i_label)
        

        
        if dir.casefold() == POS.casefold():
            return i_p
        elif dir.casefold() == NEG.casefold():
            return i_n
        else:
            return [i_p , i_n]
    
    ###########################################################################################

    def get_E_at_i(self, i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs):
        """Get the voltage at a specific current..

        Args:
            i (float): the current. 
            dir (str): direction, "pos,neg or all"
            
            "tolerance": value
            
        Returns:
            float: Voltage at a specific current.
        """
        options = {"plot": None
                   }
        options.update(kwargs)
                       
        if dir.casefold() == POS.casefold():
            
            return self._get_E_at_i(self.i_p, i, **kwargs)
        elif dir.casefold() == NEG.casefold():
            
            return self._get_E_at_i(self.i_n, i, **kwargs)
        else:
            
            return [self._get_E_at_i(self.i_p, i, **kwargs) , self._get_E_at_i(self.i_n, i, **kwargs)]
    
    ###########################################################################################


    def get_sweep(self,sweep:str, update_label = True):
        """_summary_

        Args:
            sweep (str): _description_

        Returns:
            _type_: _description_
        """
        lsv = LSV_Data()
        # lsv.setup_data =  copy.deepcopy(self.setup_data)
        lsv.copy_from(self)
        
        if str(sweep).casefold() == POS.casefold():
            lsv.i = copy.deepcopy(self.i_p)
            lsv.i_label = self.i_label+"$_{+}$"
            lsv.dir = POS
        elif str(sweep).casefold() == NEG.casefold():
            lsv.i = copy.deepcopy(self.i_n)
            lsv.i_label = self.i_label+"$_{-}$"
            lsv.dir = NEG
        elif str(sweep).casefold() == AVG.casefold():
            lsv.i = copy.deepcopy((self.i_n+self.i_p)/2)
            lsv.i_label = "( " + self.i_label+"$_{+} $+ " + self.i_label+"$_{-}$)/2"
            lsv.dir = AVG
        elif str(sweep).casefold() == DIF.casefold():
            lsv.i = (self.i_p-self.i_n)
            lsv.i_label = "( " + self.i_label+"$_{+}$ - " + self.i_label+"$_{-}$ )"
            lsv.dir = DIF
        else:
            print("use pos,neg,avg or dif")
        if not update_label:
            lsv.i_label =self.i_label
        return lsv
        
        

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
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        
        data_plot,analyse_plot,fig = create_Tafel_data_analysis_plot("CV", **kwargs)   
        Tafel_kwargs = kwargs
        Tafel_kwargs["data_plot"]=data_plot
        Tafel_kwargs["analyse_plot"]=analyse_plot
        dir = self._direction(*args,**kwargs)

        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        
        Tafel_pos = None
        Tafel_neg = None
        
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
        
            
        
        """
        cv = copy.deepcopy(self)
        cv.norm(args)
        cv.set_active_RE(args)
        
        cv_kwargs = kwargs
        Tafel_kwargs = kwargs

        dir = kwargs.get("dir", "all")
        plot_color2= []
        
        rot.append( math.sqrt(cv.rotation))
    
        cv_kwargs["legend"] = str(f"{float(cv.rotation):.0f}")
        cv_kwargs["plot"] = data_plot
        line,a = cv.plot(**cv_kwargs)
        plot_color2.append(line.get_color())
        plot_color =line.get_color()
        #.get_color()
        #color = line.get_color()
        xmin = cv.get_index_of_E(min(lims))
        xmax = cv.get_index_of_E(max(lims))
            
            
            
        if E_for_idl != None:
            i_dl_p,i_dl_n = cv.get_i_at_E(E_for_idl)
            y.append(cv.get_i_at_E(E_for_idl))
            E.append(E_for_idl)
            
            y_data_p =(np.abs(diffusion_limit_corr(cv.i_p,i_dl_p)))
            y_data_n =(np.abs(diffusion_limit_corr(cv.i_n,i_dl_n)))

        else:
            y_data_p = cv.i_p
            y_data_n = cv.i_n 
                
        Tafel_pos = Tafel(cv.E[xmin:xmax],y_data_p[xmin:xmax],cv.i_unit,cv.i_label,plot_color,"Pos",cv.E, y_data_p, plot=analyse_plot, x_label = "E vs "+ self.setup_data.getACTIVE_RE())
        Tafel_neg = Tafel(cv.E[xmin:xmax],y_data_n[xmin:xmax],cv.i_unit,cv.i_label,plot_color,"Neg",cv.E, y_data_n, plot=analyse_plot, x_label = "E vs "+ self.setup_data.getACTIVE_RE())
        
        
        
        y_values = np.array(y)
        if E_for_idl is not None:
            data_plot.plot(E,y_values[:,0], STYLE_POS_DL, E,y_values[:,1],STYLE_NEG_DL)
        data_plot.legend()
        """
        saveFig(fig,**kwargs)

        return Tafel_pos, Tafel_neg
    

