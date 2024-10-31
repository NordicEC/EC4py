""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
import math
import numpy as np
from .ec_data import EC_Data
from .cv_data import CV_Data,STYLE_POS_DL,STYLE_NEG_DL, POS, NEG 

from pathlib import Path
import copy
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig,NEWPLOT
from .analysis_levich import Levich
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas:
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
    def __init__(self, paths:list[Path] | Path, **kwargs):

        if not isinstance(paths,list ):
            path_list = [paths]
        #if isinstance(paths,Path ):
        #    path_list = [paths]
        else:
            path_list = paths
        self.datas = [CV_Data() for i in range(len(path_list))]
        index=0
        for path in path_list:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec,**kwargs)
            finally:
                index=index+1 
        #print(index)
        return
    #############################################################################
    
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
    
    def __sub__(self, other: CV_Data):
        """_summary_

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Datas: returns a copy of the initial dataset. 
        """

        if isinstance(other, CV_Data):
            new_CVs = copy.deepcopy(self)
            for new_cv in new_CVs:
                new_cv.i_p = new_cv.i_p - other.i_p
                new_cv.i_n = new_cv.i_n - other.i_n
        elif isinstance(other, CV_Datas):
            new_CVs = copy.deepcopy(self)
            for new_cv in new_CVs:
                new_cv.i_p = new_cv.i_p - other.i_p
                new_cv.i_n = new_cv.i_n - other.i_n
        return new_CVs


    #############################################################################
    
    def append(self,CV = CV_Data):
        self.datas.append(CV)
    
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

    def plot(self, *args, **kwargs):
        """Plot CVs.
            use args to normalize the data
            - area or area_cm
            - rotation
            - rate
            
            #### use kwargs for other settings.
            
            - legend = "name"
            - x_smooth = 10
            - y_smooth = 10
            
            
        """
        #CV_plot = make_plot_1x("CVs")
        
        p = plot_options(kwargs)
        p.set_title("CVs")
        line, CV_plot = p.exe()
        # legend = p.legend
        
        CVs = copy.deepcopy(self.datas)
        
        cv_kwargs = kwargs
        for cv in CVs:
            #rot.append(math.sqrt(cv.rotation))


            cv_kwargs["plot"] = CV_plot
            cv_kwargs["name"] = cv.setup_data.name

            plot = cv.plot(args, **cv_kwargs)

        CV_plot.legend()
        p.saveFig(**kwargs)
        return CV_plot

    #################################################################################################    
    
    def Levich(self, Epot:float, *args, **kwargs):
        """Levich analysis. Creates plot of the data and a Levich plot.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        fig = make_plot_2x("Levich Analysis")
        CV_plot = fig.plots[0] 
        analyse_plot = fig.plots[1]
        # CV_plot, analyse_plot = fig.subplots(1,2)
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Levich Plot')

        #########################################################
        # Make plot
        cv_kwargs = kwargs
        cv_kwargs["plot"] = CV_plot

        rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas,Epot,*args, **cv_kwargs)
        # rot = np.array(rot)
        # y = np.array(y)
        # rot_max = max(rot) 
        # Levich analysis
        B_factor_pos = Levich(rot, y[:,0], y_axis_unit, y_axis_title, STYLE_POS_DL, POS, plot=analyse_plot )
        B_factor_neg = Levich(rot, y[:,1], y_axis_unit, y_axis_title, STYLE_NEG_DL, NEG, plot=analyse_plot )

        print("Levich analysis" )
        print("dir", "\tpos     ", "\tneg     " )
        print(" :    ",f"\t{y_axis_unit} / rpm^0.5",f"\t{y_axis_unit} / rpm^0.5")
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

        fig = make_plot_2x("Koutechy-Levich Analysis")
        CV_plot = fig.plots[0] 
        analyse_plot = fig.plots[1]
        CV_plot.title.set_text('CVs')
        analyse_plot.title.set_text('Koutechy-Levich Plot')
        """
        rot=[]
        y = []
        E = []
        #Epot=-0.5
        y_axis_title =""
        y_axis_unit =""
        CVs = copy.deepcopy(self.datas)
        for cv in CVs:
            x_qv = cv.rotation
            rot.append( math.sqrt(cv.rotation))
            for arg in args:
                cv.norm(arg)
            cv_kwargs["legend"] = str(f"{float(cv.rotation):.0f}")
            cv.plot(plot = CV_plot, **cv_kwargs)
            y.append(cv.get_i_at_E(Epot))
            E.append([Epot, Epot])
            y_axis_title= cv.i_label
            y_axis_unit= cv.i_unit
            #print(cv.setup)
        #print(rot)
        
        """

        # CV_plot.plot(E,y_values[:,0], STYLE_POS_DL, E,y_values[:,1],STYLE_NEG_DL)
        # CV_plot.legend()
        cv_kwargs = kwargs
        cv_kwargs["plot"] = CV_plot
        rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas, Epot, *args, **cv_kwargs)

        # rot = np.array(rot)

        rot = 1 / rot 
        x_plot = np.insert(rot, 0, 0)  
        x_qv = QV(1, "rpm^0.5","w")
        x_u =  QV(1, x_qv.unit,x_qv.quantity)** -0.5
        # print(x_plot) 
        y_values = np.array(y)
        y_inv = 1/ y_values

        y_qv = QV(1, y_axis_unit.strip(), y_axis_title.strip())**-1
        # print(rot)
        # print(y[:,0])

        analyse_plot.plot(rot, y_inv[:, 0], STYLE_POS_DL, rot, y_inv[:,1], STYLE_NEG_DL)
        # print("AAAA", x_qv.quantity,x_qv)
        # print("AAAA", x_u.quantity, x_u)
#        analyse_plot.set_xlabel(str("$\omega^{-0.5}$" + "("+ "rpm$^{-0.5}$" +")"))
        analyse_plot.set_xlabel(f"{quantity_plot_fix(x_u.quantity)} ( {quantity_plot_fix(x_u.unit)} )")

        analyse_plot.set_ylabel(str( f"(1 / ({quantity_plot_fix(y_axis_title)}) ({quantity_plot_fix(y_qv.unit)})"))

        # FIT pos

        dydx_qv = y_qv / x_u
        m_pos, b = np.polyfit(rot, y_inv[:,0], 1)

        y_pos= m_pos * x_plot + b
        slope_pos = QV(m_pos, dydx_qv.unit, dydx_qv.quantity)

        B_pos = 1 / m_pos
        line, = analyse_plot.plot(x_plot, y_pos, 'b-' )
        line.set_label(f"pos: m={B_pos:3.3e}")
        # FIT neg
        m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        slope_neg = QV(m_neg,dydx_qv.unit,dydx_qv.quantity)
        y_neg= m_neg * x_plot + b
        B_neg = 1/m_neg
        line,=analyse_plot.plot(x_plot,y_neg, 'r-' )
        line.set_label(f"neg: m={B_neg:3.3e}")


        analyse_plot.legend()
        analyse_plot.set_xlim(left=0, right=None)
        print("KouLev analysis" )
        print("dir","\tpos     ", "\tneg     " )
        print(" :", f"\trpm^0.5 /{y_axis_unit}", f"\trpm^0.5 /{y_axis_unit}")
        print("slope:", "\t{:.2e}".format(B_pos) , "\t{:.2e}".format(B_neg))
        
        saveFig(fig,**kwargs)
        return slope_pos,slope_neg
    
    ##################################################################################################################
    
    
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        
        fig = make_plot_2x("Tafel Analysis")
        CV_plot = fig.plots[0] 
        analyse_plot = fig.plots[1]
        CV_plot.title.set_text('CVs')
        analyse_plot.title.set_text('Tafel Plot')   
        cv_kwargs = kwargs
        cv_kwargs['cv_plot'] = CV_plot
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
            cv.norm(args)
        return

#########################################################################

def plots_for_rotations(datas: CV_Datas, Epot: float, *args, **kwargs):
    rot = []
    y = []
    E = []
    # Epot=-0.5
    y_axis_title = ""
    y_axis_unit = ""
    CVs = copy.deepcopy(datas)
    cv_kwargs = kwargs
    # x_qv = QV(1, "rpm^0.5","w")
    line=[]
    for cv in CVs:
        # x_qv = cv.rotation
        rot.append(float(cv.rotation))
        cv.norm(args)
        cv.set_active_RE(args)
        cv_kwargs["legend"] = str(f"{float(cv.rotation):.0f}")
        # cv_kwargs["plot"] = CV_plot
        l, ax = cv.plot( **cv_kwargs)

        line.append(l)
        y.append(cv.get_i_at_E(Epot))
        E.append([Epot, Epot])
        y_axis_title = str(cv.i_label)
        y_axis_unit = str(cv.i_unit)
    rot = np.array(rot)
    y = np.array(y)
    CV_plot = cv_kwargs["plot"]
    CV_plot.plot(E, y[:, 0], STYLE_POS_DL, E, y[:, 1], STYLE_NEG_DL)
    CV_plot.legend()
    return rot, y, E, y_axis_title, y_axis_unit
