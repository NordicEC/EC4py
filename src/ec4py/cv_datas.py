""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
import math
import numpy as np
from .ec_data import EC_Data
from .ec_datas_util import EC_Datas_base,check_paths

from .cv_data import CV_Data,STYLE_POS_DL,STYLE_NEG_DL, POS, NEG 

from pathlib import Path
import copy
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig,NEWPLOT,LEGEND,should_plot_be_made

from .analysis_levich import Levich
from .analysis_ran_sev   import ran_sev
from .analysis_rate   import sweep_rate_analysis


from .util_voltammetry import Voltammetry,create_Tafel_data_analysis_plot,create_RanSev_data_analysis_plot
from .util_voltammetry import create_Rate_data_analysis_plot,create_Levich_data_analysis_plot,create_KouLev_data_analysis_plot
from .lsv_datas import LSV_Datas

import pandas as pd
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas(EC_Datas_base):
    """# Class to analyze CV datas. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.

    ### Analysis:
    - .Levich() - plot data    
    - .KouLev() - Koutechy-Levich analysis    
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """
    def __init__(self,paths:list[Path]|Path = None,*args, **kwargs):
        
        EC_Datas_base.__init__(self,*args, **kwargs)
        #self.datas =[]
        
        if paths is not None:
            path_list = check_paths(paths)
            # paths = args[0]
            """
            if not isinstance(paths,list ):
                path_list = [paths]
            #if isinstance(paths,Path ):
            #    path_list = [paths]
            else:
                path_list = paths
            """
            self.datas = [CV_Data() for i in range(len(path_list))]
            index=0
            for path in path_list:
                ec = EC_Data(path)
                #print([x for x in args])
                try:
                    
                    self.datas[index].conv(ec,*args,**kwargs)
                finally:
                    index=index+1 
            #print(index)
    #############################################################################
    
    def __repr__(self):
        """CV Datas
        """
        delimiter = "','"
        r =delimiter.join([x.setup_data.fileName for x in self.datas])
        return f"CV_Datas(['{r}'])"
    
    
    def __getitem__(self, item_index:slice | int) -> CV_Data: 

        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop    
            return [self.datas[i] for i in range(start, stop, step)  ]
        else:
            return self.datas[item_index]
    #############################################################################
    
    def __setitem__(self, item_index:int, new_CV:CV_Data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_CV
    #############################################################################
    
    def __add__(self, other: CV_Data):
        """add

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.add(other)
        return new_CVs
    
    def __sub__(self, other: CV_Data):
        """sub

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.sub(other)
        return new_CVs
    
    def __mul__(self, other: float):
        """multiply

        Args:
            other (float): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.mul(other)
        return new_CVs
    
    def __truediv__(self, other: float):
        """divide

        Args:
            other (float): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """
        new_CVs = copy.deepcopy(self)
        new_CVs.div(other)
        return new_CVs

    #def __len__(self):
    #    return len(self.datas)

    #############################################################################
    
    
    def add(self,other):
        """add

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, CV_Datas) or isinstance(other, list):
            if len(other) == len(self):
                for i in range(0,len(self.datas)):
                    self.datas[i].add(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.add(other)  
        ##########################################        
    def sub(self,other):
        """sub

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, CV_Datas) or isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].sub(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.sub(other)
                
    def mul(self,other):
        """multiply the current by a number or a list of numbers.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].mul(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.mul(other)
            
    def div(self,other):
        """divide the current by a number.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].div(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for cv in self.datas:
                cv.div(other)   
        
    
    def append(self,other = CV_Data):
        """append

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, CV_Data):
            self.datas.append(other)
        elif isinstance(other, CV_Datas):
            for cv in other:
                self.datas.append(cv)
    
    def pop(self,index):
        self.datas.pop(index)
    
    
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero.
        
        Args:
            E (float): potential where to set the current to zero. 

        """
        for x in self.datas:
            x.set_i_at_E_to_zero(E,*args,**kwargs)
    
    def bg_corr(self, bg_cv: CV_Data|Path) -> CV_Data:
        """Background correct the data by subtracting the bg_cv. 

        Args:
            bg_cv (CV_Datas, CV_Data or Path):
        
        Returns:
            CV_Data: copy of the data.
        
        """
        if isinstance(bg_cv, CV_Datas):
            if len(bg_cv.datas) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].sub(bg_cv[i])
            else:
                raise ValueError('The data sets are not of the same length.')

        else:         
            if isinstance(bg_cv, CV_Data):
                corr_cv =bg_cv    
            else:
                corr_cv =CV_Data(bg_cv)
                #print(bg_cv)
            for cv in self.datas:
                cv.sub(corr_cv)
        return copy.deepcopy(self)

    def pot_shift(self,shift_to:str|tuple = None):
        """Shift the potential to another defined reference potential.

        Args:
            shift_to (str | tuple, optional): RHE or SHE. Defaults to None.
        """
        for cv in self.datas:
            cv.pot_shift(shift_to)
    
################################################################   

    def get_i_at_E(self, E:float, direction:str,*args, **kwargs):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            list of current at E
        """
                
        return [x.get_i_at_E(E,direction,*args,**kwargs) for x in self.datas]
        
    ########################################################################################################

    def get_sweep(self,sweep:str,update_label=True):
        """_summary_

        Args:
            sweep (str): use "POS","NEG", "AVG" or "DIF" 
            update_label (bool, optional): Change the label of the current according to the sweep. Defaults to True.

        Returns:
            LSV_Datas
        """
        
        
        LSVs = LSV_Datas()
        LSVs.dir = sweep
        for cv in self.datas:
            LSVs.append(cv.get_sweep(sweep,update_label))
        return LSVs
    
    @property
    def rate(self):
        rate=[]
        for cv in self.datas:
            
            rate.append(cv.rate)
        return rate
    
    @property
    def area(self):
        return [x.area for x in self.datas]

    @property
    def name(self):
        return [x.name for x in self.datas]
    
    @property
    def pressure(self):
        """
        Returns:
            list[Quantity_Value_Unit]
        """
        return [x.pressure for x in self.datas]
    
    @property
    def temp0(self):
        return [x.temp0 for x in self.datas]
    
    @property
    def RE(self):
        return [x.RE for x in self.datas]

    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        return [cv.get_E_of_max_i(E1,E2,*args, **kwargs) for cv in self.datas]
    
    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        return [cv.get_E_of_min_i(E1,E2,*args, **kwargs) for cv in self.datas]

    def norm(self,*args, **kwargs):
        """Normalise the current to certain factors. 

        Args:
            norm_to (str | tuple): _description_
        """
        
        for x in self.datas:
            x.norm(args)
        return

    def plot(self, *args, **kwargs):
        """Plot CVs.
            
            *args (str): Variable length argument list to normalize the data or shift the potential.             
                - AREA or AREA_CM (constants)
                - ROT or SQRT_ROT (constants)
                - RATE or SQRT_RATE (constants)
                - LEGEND (enum) for legend of plot
                
            
            
            #### use kwargs for other settings.
            
            - x_smooth = 10
            - y_smooth = 10
            
            
        """
        #CV_plot = make_plot_1x("CVs")
        if should_plot_be_made(*args,**kwargs):
            p = plot_options(kwargs)
            p.set_title("CVs")
            line, CV_plot = p.exe()
            # legend = p.legend
            
            CVs = copy.deepcopy(self.datas)
            
            cv_kwargs = kwargs
            lines = []
            for cv in CVs:
                #rot.append(math.sqrt(cv.rotation))


                cv_kwargs["plot"] = CV_plot
                cv_kwargs["name"] = cv.setup_data.name

                line, ax = cv.plot(*args, **cv_kwargs)
                lines.append(line)
                
            CV_plot.legend()
            p.saveFig(**kwargs)
            return CV_plot
        else:
            return None
    #################################################################################################    
    
    def RanSev(self, Epot:float,*args, **kwargs):
        """Randles–Sevcik analysis. Creates plot of the data and a Randles–Sevcik plot.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        dir = Voltammetry()._direction(*args)
        #print("AA",Voltammetry()._direction(*args))
        if dir == "":
            dir = "all"
        #op.update(kwargs)
       
        if(dir.casefold() !="all".casefold()):
            lsvs = self.get_sweep(dir)
            return lsvs.RanSev(Epot,*args,**kwargs)
           
        else:
                    
            data_plot, analyse_plot,fig = create_RanSev_data_analysis_plot()
        
            #########################################################
            # Make plot
            cv_kwargs = kwargs
            cv_kwargs["plot"] = data_plot
            
            rate = [float(val) for val in self.rate]
            E =[Epot for val in self.rate]
            plot =self.plot(LEGEND.RATE,*args, **kwargs)
            
            yu,yn = self.get_i_at_E(Epot,"all",*args, **kwargs)
            #[print(x) for x in yu]
            #print("yn")
            #[print(x) for x in yn]
            #print(yu[0])
            # rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas,Epot,*args, **cv_kwargs)
            plot.plot(E, yu, STYLE_POS_DL)
            plot.plot(E, yn, STYLE_NEG_DL)
            y_axis_title =str(yu[0].quantity).replace("$_{+}$","")
            y_axis_unit = yu[0].unit
            B_factor_pos=0
            B_factor_pos = ran_sev(rate, yn, y_axis_unit, y_axis_title, STYLE_POS_DL, POS, plot=analyse_plot )
            B_factor_neg = ran_sev(rate, yu, y_axis_unit, y_axis_title, STYLE_NEG_DL, NEG, plot=analyse_plot )

            print("RanSev analysis" )
            print("dir", "\tpos     ", "\tneg     " )
            print(" :    ",f"\t{B_factor_pos.unit}",f"\t{B_factor_pos.unit}")
            print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
            
            saveFig(fig,**kwargs)
            return B_factor_pos, B_factor_neg
    #################################################################################################  
      
    def RateAnalysis(self, Epot:float,*args, **kwargs):
        """.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        dir = Voltammetry()._direction(*args)
        #print("AA",Voltammetry()._direction(*args))
                
        rate = [float(val) for val in self.rate]
        E =[Epot for val in self.rate]
        rate_unit = self.rate[0].unit
        #print("DIR",dir)
        if(dir !=""):
            lsvs = self.get_sweep(dir)
            return lsvs.RateAnalysis(Epot,*args,**kwargs)
           
        else:
            data_plot, analyse_plot,fig = create_Rate_data_analysis_plot(*args,**kwargs)
            #########################################################
            # Make plot
            cv_kwargs = kwargs
            cv_kwargs["plot"] = data_plot
            plot =self.plot(LEGEND.RATE, *args, **cv_kwargs) 
            
            analyse_kwargs = kwargs
            
            analyse_kwargs["update_label"]=True          
            yp,yn = self.get_i_at_E(Epot,"",*args, **kwargs)
            if plot is not None:
                plot.plot(E, yp, STYLE_POS_DL)
                plot.plot(E, yn, STYLE_NEG_DL)
            self.datas[0].get_i_at_E(Epot,"",*args,**analyse_kwargs)
            y_axis_title =y_axis_title =str(yp[0].quantity).replace("$_{+}$","")
            y_axis_unit = yp[0].unit
            B_factor_pos=0
            analyse_kwargs["plot"] = analyse_plot
            B_factor_pos = sweep_rate_analysis(rate, yp, y_axis_unit, y_axis_title, STYLE_POS_DL, POS,rate_unit, *args, **analyse_kwargs )
            B_factor_neg = sweep_rate_analysis(rate, yn, y_axis_unit, y_axis_title, STYLE_NEG_DL, NEG,rate_unit,*args, **analyse_kwargs )

            print("Sweep Rate analysis" )
            print("dir", "\tpos     ", "\tneg     " )
            print(" :    ",f"\t{B_factor_pos.unit}",f"\t{B_factor_neg.unit}")
            print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
        
            saveFig(fig,**kwargs)
            return B_factor_pos, B_factor_neg
    
    
    def Levich(self, Epot:float, *args, **kwargs):
        """Levich analysis. Creates plot of the data and a Levich plot.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        dir = Voltammetry()._direction(*args)
        print(dir)
        if(dir.casefold() !="all".casefold() and dir !=""):
            lsvs = self.get_sweep(dir)
            return lsvs.Levich(Epot,*args,**kwargs)
        else:
            data_plot, analyse_plot, fig = create_Levich_data_analysis_plot("Data",*args,**kwargs)

            #########################################################
            # Make plot
            data_kwargs = kwargs
            data_kwargs["plot"] = data_plot
            #if kwargs.get("legend",None) is None:
                # data_kwargs["legend"] = LEGEND.ROT
            self.plot(LEGEND.ROT,*args, **data_kwargs)
            
            lsv_pos = self.get_sweep(POS,False)
            B_factor_pos =lsv_pos.Levich(Epot,*args,data_plot=data_plot,analyse_plot=analyse_plot,**kwargs)
            lsv_neg = self.get_sweep(NEG,False)
            B_factor_neg =lsv_neg.Levich(Epot,*args,data_plot=data_plot,analyse_plot=analyse_plot,**kwargs)
            
            print("Levich analysis" )
            print("dir", "\tpos     ", "\tneg     " )
            print(" :    ",f"\t{B_factor_pos.unit}",f"\t{B_factor_neg.unit}")
            print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
            
            saveFig(fig,**kwargs)
            return B_factor_pos, B_factor_neg

    #######################################################################################################
    
    def KouLev(self, Epot: float, *args,**kwargs):
        """Creates a Koutechy-Levich plot.

        Args:
            Epot (float): The potential where the idl is
            use arguments to normalize the data.
            for example "area"

        Returns:
            _type_: _description_
        """

        dir = Voltammetry()._direction(*args)
        print(dir)
        if(dir.casefold() !="all".casefold() and dir !=""):
            lsvs = self.get_sweep(dir)
            return lsvs.KoutLev(Epot,*args,**kwargs)
        else:
            data_plot, analyse_plot, fig = create_KouLev_data_analysis_plot("Data",*args,**kwargs)
            data_kwargs = kwargs
            data_kwargs["plot"] = data_plot
            #if kwargs.get("legend",None) is None:
            #    data_kwargs["legend"] = LEGEND.ROT
            self.plot(LEGEND.ROT,*args, **data_kwargs)
            lsv_pos = self.get_sweep(POS,False)
            B_factor_pos =lsv_pos.KouLev(Epot,*args,data_plot=data_plot,analyse_plot=analyse_plot,**kwargs)
            lsv_neg = self.get_sweep(NEG,False)
            B_factor_neg =lsv_neg.KouLev(Epot,*args,data_plot=data_plot,analyse_plot=analyse_plot,**kwargs)
            
            print("KouLev analysis" )
            print("dir","\tpos     ", "\tneg     " )
            print(" :", f"\t{B_factor_pos.unit}", f"\t{B_factor_neg.unit}")
            print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
            
            saveFig(fig,**kwargs)
            
            return B_factor_pos,B_factor_neg
            
    ##################################################################################################################
    
    
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        data_plot, analyse_plot,fig = create_Tafel_data_analysis_plot("CVs",**kwargs)
        #fig = make_plot_2x("Tafel Analysis")
        #CV_plot = fig.plots[0] 
        #analyse_plot = fig.plots[1]
        #CV_plot.title.set_text('CVs')
        #analyse_plot.title.set_text('Tafel Plot')   
        cv_kwargs = kwargs
        #cv_kwargs['data_plot'] = CV_plot
        cv_kwargs['data_plot'] = data_plot
        cv_kwargs['analyse_plot'] = analyse_plot
        Tafel_pos =[]
        Tafel_neg =[]
        for cv in self.datas:
            a, b = cv.Tafel(lims, E_for_idl, **cv_kwargs)
            Tafel_pos.append(a)
            Tafel_neg.append(b)
        
        saveFig(fig,**kwargs)
        return Tafel_pos, Tafel_neg
##################################################################################################################

    def set_active_RE(self,*args):     
        """Set active reference electrode for plotting.
        
        - RHE    - if values is not already set, use ".set_RHE()"
        
        - SHE    - if values is not already set, use ".set_RHE()"
        - None to use the exerimental 
        """
        for cv in self.datas:
            cv.set_active_RE(args)
        return

#########################################################################

    def export_DataFrame(self,direction,*args, **kwargs):
        LSVs=self.get_sweep(direction,False)
        LSVs.set_active_RE(args)
        LSVs.norm(*args)
        return LSVs.export_DataFrame()
    
    #########################################################################

    def export_Array(self,direction,*args, **kwargs):
        LSVs=self.get_sweep(direction,False)
        LSVs.set_active_RE(args)
        LSVs.norm(*args)
        return LSVs.export_Array()