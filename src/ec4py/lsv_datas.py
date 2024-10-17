""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
import math
import numpy as np
from .ec_data import EC_Data
from .lsv_data import LSV_Data

from pathlib import Path
import copy
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x
from .analysis_levich import Levich
from .analysis_tafel import Tafel


STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Datas:
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
    def __init__(self, paths:list[Path] | Path = None, **kwargs):
        self.datas = []
        if paths is None:
            return
        if not isinstance(paths,list ):
            path_list = [paths]
        #if isinstance(paths,Path ):
        #    path_list = [paths]
        else:
            path_list = paths
        self.datas = [LSV_Data() for i in range(len(path_list))]
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
    
    def __getitem__(self, item_index:slice | int) -> LSV_Data: 

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
    
    def __setitem__(self, item_index:int, new_LSV:LSV_Data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_LSV
    #############################################################################
    
    def __sub__(self, other: LSV_Data):
        """_summary_

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Datas: returns a copy of the initial dataset. 
        """

        if isinstance(other, LSV_Data):
            new_LSVs = copy.deepcopy(self)
            for new_LSV in new_LSVs:
                new_LSV.i = new_LSV.i - other.i
              
        elif isinstance(other, LSV_Datas):
            new_LSVs = copy.deepcopy(self)
            for new_LSV in new_LSVs:
                new_LSV.i = new_LSV.i - other.i
        return new_LSVs


    #############################################################################
    
    def append(self,LSV = LSV_Data):
        self.datas.append(LSV)
    
    def bg_corr(self, bg: LSV_Data|Path) -> LSV_Data:
        """Background correct the data by subtracting the bg. 

        Args:
            bg_cv (CV_Datas, CV_Data or Path):
        
        Returns:
            CV_Data: copy of the data.
        
        """
        if isinstance(bg, LSV_Datas):
            if len(bg.datas) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].sub(bg[i])
            else:
                raise ValueError('The data sets are not of the same length.')

        else:         
            if isinstance(bg, LSV_Data):
                corr_lsv =bg    
            else:
                corr_lsv =LSV_Data(bg)
            for data in self.datas:
                data.sub(corr_lsv)
        return copy.deepcopy(self)

################################################################   

    def plot(self, *args, **kwargs):
        """Plot LSVs.
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
        p.set_title("LVs")
        line, data_plot = p.exe()
        legend = p.legend
        
        datas = copy.deepcopy(self.datas)
        data_plot_kwargs = kwargs
        for data in datas:
            #rot.append(math.sqrt(cv.rotation))
            for arg in args:
                data.norm(arg)

            data_plot_kwargs["plot"] = data_plot
            data_plot_kwargs["name"] = data.setup_data.name
            if legend == "_" :
                data_plot_kwargs["legend"] = data.setup_data.name

            p = data.plot(**data_plot_kwargs)

        data_plot.legend()
        return data_plot

    #################################################################################################    
    
    def Levich(self, Epot:float, *args, **kwargs):
        """Levich analysis. Creates plot of the data and a Levich plot.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        fig = make_plot_2x("Levich Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        
        # CV_plot, analyse_plot = fig.subplots(1,2)
        data_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Levich Plot')

        #########################################################
        # Make plot
        dataPlot_kwargs = kwargs
        dataPlot_kwargs["plot"] = data_plot

        rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas,Epot,*args, **dataPlot_kwargs)
        # rot = np.array(rot)
        # y = np.array(y)
        # rot_max = max(rot) 
        # Levich analysis
        B_factor_pos = Levich(rot, y[:,0], y_axis_unit, y_axis_title, STYLE_POS_DL, "pos", plot=analyse_plot )
        B_factor_neg = Levich(rot, y[:,1], y_axis_unit, y_axis_title, STYLE_NEG_DL, "neg", plot=analyse_plot )

        print("Levich analysis" )
        print("dir", "\tpos     ", "\tneg     " )
        print(" :    ",f"\t{y_axis_unit} / rpm^0.5",f"\t{y_axis_unit} / rpm^0.5")
        print("slope:", "\t{:.2e}".format(B_factor_pos.value) , "\t{:.2e}".format(B_factor_neg.value))
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
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]


        data_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Koutechy-Levich Plot')
        
        # CV_plot.plot(E,y_values[:,0], STYLE_POS_DL, E,y_values[:,1],STYLE_NEG_DL)
        # CV_plot.legend()
        dataPlot_kwargs = kwargs
        dataPlot_kwargs["plot"] = data_plot
        rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas, Epot, *args, **dataPlot_kwargs)

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
        return slope_pos,slope_neg
    
    ##################################################################################################################
    
    
    def Tafel2(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        fig = make_plot_2x("Tafel Analysis")
        data_plot = fig.plots[0]
        analyse_plot =  fig.plots[1]
        data_plot.title.set_text('LSV')

        analyse_plot.title.set_text('Tafel Plot')   
        dataPlot_kwargs = kwargs
        dataPlot_kwargs['cv_plot'] = data_plot
        dataPlot_kwargs['analyse_plot'] = analyse_plot
        Tafel_pos =[]
        for data in self.datas:
            a, b = data.Tafel(lims, E_for_idl, **dataPlot_kwargs)
            Tafel_pos.append(a)
        return Tafel_pos
##################################################################################################################


    """
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        ""_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        ""
        CV_plot, analyse_plot = make_plot_2x("Tafel Analysis")
        CV_plot.title.set_text('CVs')

        analyse_plot.title.set_text('Tafel Plot')

        rot=[]
        y = []
        E = []
        Tafel_pos =[]
        Tafel_neg =[]
        #Epot=-0.5
        y_axis_title =""
        CVs = copy.deepcopy(self.datas)
        cv_kwargs = kwargs
        dir = kwargs.get("dir", "all")
        plot_color2= []
        for cv in CVs:
            rot.append( math.sqrt(cv.rotation))

            for arg in args:
                #if arg == "area":
                cv.norm(arg)
            cv_kwargs["legend"] = str(f"{float(cv.rotation):.0f}")
            cv_kwargs["plot"] = CV_plot
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
                with np.errstate(divide='ignore'):
                    y_data_p = [math.log10(abs(1/(1/i-1/i_dl_p))) for i in cv.i_p]
                    y_data_n = [math.log10(abs(1/(1/i-1/i_dl_n))) for i in cv.i_n]
            else:
                y_data_p = [math.log10(abs(i)) for i in cv.i_p]
                y_data_n = [math.log10(abs(i)) for i in cv.i_n]
            #y_data = cv.i_p[xmin:xmax]
            
            ##FIT    
            m_pos, b = np.polyfit(cv.E[xmin:xmax], y_data_p[xmin:xmax], 1)
            y_pos= m_pos*cv.E[xmin:xmax]+b
            Tafel_pos.append(QV(1/ m_pos,"V/dec","dE"))
            m_neg, b = np.polyfit(cv.E[xmin:xmax], y_data_n[xmin:xmax], 1)
            y_neg= m_neg*cv.E[xmin:xmax]+b
            Tafel_neg.append(QV(1/ m_neg,"V/dec","dE"))
            
            print("Tafel", 1./ m_pos , "V/dec")
            if E_for_idl != None:
                E.append([E_for_idl, E_for_idl])
            
            y_axis_title= cv.i_label
            y_axis_unit= cv.i_unit
            if dir!="neg":
                analyse_plot.plot(cv.E, y_data_p,c= plot_color)
                line, = analyse_plot.plot(cv.E[xmin:xmax], y_pos,linewidth=3.0, c= plot_color)
                #line.set_color(plot_color)
                line.set_label(f"pos: m={1000/m_pos:3.1f}mV/dec")
            if dir!="pos":
                analyse_plot.plot(cv.E, y_data_n,c= plot_color)
                line, = analyse_plot.plot(cv.E[xmin:xmax], y_neg,linewidth=3.0,c= plot_color)
                line.set_label(f"neg: m={1000/m_neg:3.1f}mV/dec")
            
            #print(cv.setup)
        #print(rot)

        y_values = np.array(y)
        if E_for_idl != None:
            CV_plot.plot(E,y_values[:,0], STYLE_POS_DL, E,y_values[:,1],STYLE_NEG_DL)
        CV_plot.legend()


        analyse_plot.set_xlim(lims[0]-0.1,lims[1]+0.1)

        analyse_plot.set_xlabel("E ( V )")
        analyse_plot.set_ylabel(f"log( {y_axis_title} / {y_axis_unit} )" )
        #m_pos, b = np.polyfit(rot, y_inv[:,0], 1)
        #y_pos= m_pos*rot+b
        #line,=analyse_plot.plot(rot,y_pos,'-' )
        #line.set_label(f"pos: m={m_pos:3.3e}")
        #m_neg, b = np.polyfit(rot, y_inv[:,1], 1)
        #y_neg= m_neg*rot+b
        #line, = analyse_plot.plot(rot,y_neg,'-' )
        #line.set_label(f"neg: m={m_neg:3.3e}")
        analyse_plot.legend()
        #print("Tafel",m_pos,m_neg)
        #return m_pos,m_neg
        return Tafel_pos, Tafel_neg
        """


def plots_for_rotations(datas: LSV_Datas, Epot: float, *args, **kwargs):
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
        rot.append(math.sqrt(cv.rotation))
        for arg in args:
            cv.norm(arg)
        cv_kwargs["legend"] = str(f"{float(cv.rotation):.0f}")
        # cv_kwargs["plot"] = CV_plot
        l, ax = cv.plot(**cv_kwargs)
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
