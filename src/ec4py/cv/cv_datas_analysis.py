""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
# import math
# import numpy as np
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Self

# from .analysis_levich import Levich
from ..analysis import ran_sev,sweep_rate_analysis

#from ..ec_data.ec_data import EC_Data
#from ..lsv.lsv_data import LSV_Data
#from ..lsv.lsv_datas import LSV_Datas
from ..method_util.ec_datas_util import EC_Datas_base, check_paths
from ..method_util.util_voltammetry import (
    Voltammetry,
    create_KouLev_data_analysis_plot,
    create_Levich_data_analysis_plot,
    create_RanSev_data_analysis_plot,
    create_Rate_data_analysis_plot,
    create_Tafel_data_analysis_plot,
)
from ..util import Quantity_Value_Unit as QV

# from .util import Quantity_Value_Unit as QV
from ..util_graph import (
    ANALYSE_PLOT,
    DATA_PLOT,
    LEGEND,
    ENUM_plotKW,
    plot_options,
    saveFig,
    should_plot_be_made,
    update_plot_kwargs,
)
from .cv_data import NEG, POS, STYLE_NEG_DL, STYLE_POS_DL, CV_Data
from .cv_datas_extra import CV_Datas_Extra

if TYPE_CHECKING:
    # Gives Pylance/Pyright full autocomplete without circular imports
    from .cv_datas import CV_Datas
    _Base = CV_Datas
else:
    _Base = object

# import pandas as pd
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas_Anlysis(CV_Datas_Extra,_Base):
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
            p = plot_options(**kwargs)
            p.set_title("CVs")
            line, CV_plot = p.exe()
            # legend = p.legend
            
            CVs = copy.deepcopy(self.datas)
            
            cv_kwargs = kwargs
            lines = []
            for index, cv in enumerate(CVs):
                cv_kwargs = update_plot_kwargs(index, **kwargs)
               
                cv_kwargs["plot"] = CV_plot
                cv_kwargs["name"] = cv.setup_data.name
                line, ax = cv.plot(*args, **cv_kwargs)
                lines.append(line)
            # print(p.legend)
            if p.legend != "" and p.legend != LEGEND.NONE and p.legend != "_" or kwargs.get(ENUM_plotKW.LABEL,None) is not None:     
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
            B_factor_pos =QV()
            B_factor_neg =QV()

            if plot:
                plot.plot(E, yu, STYLE_POS_DL)
                plot.plot(E, yn, STYLE_NEG_DL)

            if isinstance(yu, list):

                y_axis_title =str(yu[0].quantity).replace("$_{+}$","")
                y_axis_unit = yu[0].unit
                B_factor_pos=0
                B_factor_pos = ran_sev(rate, yn, y_axis_unit, y_axis_title, STYLE_POS_DL, POS, plot=analyse_plot )
                B_factor_neg = ran_sev(rate, yu, y_axis_unit, y_axis_title, STYLE_NEG_DL, NEG, plot=analyse_plot )

            print("RanSev analysis" )
            print("dir", "\tpos     ", "\tneg     " )
            print(" :    ",f"\t{B_factor_pos.unit}",f"\t{B_factor_pos.unit}")
            print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
            if fig is not None:
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
            y = self.get_i_at_E(Epot,"",*args, **kwargs)
            y1 =y[1]
            #if isinstance(y1,list):
            yp = [x[0] for x in y if isinstance(x,list )]
            yn = [x[1] for x in y if isinstance(x,list )]
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
            print("slope:", f"\t{B_factor_pos.value:.2e}" , f"\t{B_factor_neg.value:.2e}")
            if fig is not None:
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
            return lsvs.KouLev(Epot,*args,**kwargs)
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
    
    
    def Tafel(self, lims=[-1,1], E_for_idl:float=float('nan') , *args, **kwargs):
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
        for index, cv in enumerate(self.datas):
            cv_kwargs = update_plot_kwargs(index, **kwargs)
            cv_kwargs[DATA_PLOT] = data_plot
            cv_kwargs[ANALYSE_PLOT] = analyse_plot
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