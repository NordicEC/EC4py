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
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig,NEWPLOT,LEGEND,ANALYSE_PLOT,DATA_PLOT,update_legend

from .util_voltammetry import create_Tafel_data_analysis_plot,create_RanSev_data_analysis_plot,create_Rate_data_analysis_plot,create_Levich_data_analysis_plot,create_KouLev_data_analysis_plot


from .analysis_levich import Levich
from .analysis_tafel import Tafel
from .analysis_ran_sev   import ran_sev
from .analysis_rate   import sweep_rate_analysis


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
        self.dir =""
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
        
    @property
    def rate(self):
        rates=[]
        for lsv in self.datas:
            
            rates.append(lsv.rate)
        return rates
    
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

    def get_i_at_E(self, E:float,*args, **kwargs):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            float: current
        """
        i_at_E=[]
        for x in self.datas:
            lsv = copy.deepcopy(x)
            
            a =lsv.get_i_at_E(E,*args,**kwargs)
            i_at_E.append(a)
            
        return i_at_E
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
        data_plot_kwargs = update_legend(LEGEND.NAME,*args,**kwargs)
        #if data_plot_kwargs.get("legend",None) is None:
            #data_plot_kwargs["legend"] = LEGEND.NAME
        #    data_plot_kwargs = update_legend(LEGEND.NAME,**kwargs)

        p = plot_options(data_plot_kwargs)
        p.no_smooth()
        p.set_title("LSVs")
        p.x_data= None
        line, data_plot = p.exe()
        legend = p.legend
        
        datas = copy.deepcopy(self.datas)
        #data_plot_kwargs = kwargs
        data_plot_kwargs["plot"] = data_plot
        for data in datas:
            #rot.append(math.sqrt(cv.rotation))
  
            data_plot_kwargs["name"] = data.setup_data.name
            # print(data_plot_kwargs["legend"])
            #if legend == "_"  :
            #    data_plot_kwargs["legend"] = data.setup_data.name

            data.plot(*args, **data_plot_kwargs)

        data_plot.legend()
        p.saveFig(**kwargs)
        return data_plot

    #################################################################################################    
    
    def RateAnalysis(self, Epot:float,*args, **kwargs):
        """.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
    
        data_plot, analyse_plot,fig = create_Rate_data_analysis_plot()
       
        #########################################################
        # Make plot
        cv_kwargs = kwargs
        cv_kwargs["plot"] = data_plot
        
        rate = [float(val) for val in self.rate]
        E =[Epot for val in self.rate]
       
        if fig is not None:
            self.plot(LEGEND.RATE,*args, **cv_kwargs)

        y = self.get_i_at_E(Epot,*args, **kwargs)
        #PLOT
        style = self.datas[0].get_point_color()

        data_plot.plot(E, y, style)
        y_axis_title =y[0].quantity
        y_axis_unit = y[0].unit
        # print(y_axis_title)
        B_factor_pos=0
        B_factor_pos = sweep_rate_analysis(rate, y, y_axis_unit, y_axis_title, style, self.dir,plot=analyse_plot )
        
        saveFig(fig,**kwargs)
        return B_factor_pos
    
        #################################################################################################    

    def RanSev(self, Epot:float,*args, **kwargs):
        """.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of 
        """
    
        data_plot, analyse_plot,fig = create_RanSev_data_analysis_plot()
       
        #########################################################
        # Make plot
        dataPlot_kwargs = kwargs
        dataPlot_kwargs["plot"] = data_plot
        if fig is not None:
            #if kwargs.get("legend",None) is None:
            #    dataPlot_kwargs["legend"] = LEGEND.RATE
            self.plot(LEGEND.RATE,*args, **dataPlot_kwargs)
                
        rate = [float(val) for val in self.rate]
        E =[Epot for val in self.rate]
       
 
        
        
        y = self.get_i_at_E(Epot,*args, **kwargs)
        #PLOT
        style = self.datas[0].get_point_color()

        data_plot.plot(E, y, style)
        y_axis_title =y[0].quantity
        y_axis_unit = y[0].unit
        # print(y_axis_title)
        B_factor=0
        B_factor = ran_sev(rate, y, y_axis_unit, y_axis_title, style, self.dir,plot=analyse_plot )
        
        saveFig(fig,**kwargs)
        return B_factor 
    
        #################################################################################################   
    
    def Levich(self, Epot:float, *args, **kwargs):
        """Levich analysis. Creates plot of the data and a Levich plot.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
        data_plot, analyse_plot, fig = create_Levich_data_analysis_plot("Data",*args,**kwargs)
        
      
        #########################################################
        # Make plot
        data_Plot_kwargs = kwargs
        data_Plot_kwargs["plot"] = data_plot
        data_plot_kwargs = update_legend(LEGEND.ROT,*args,**data_Plot_kwargs)

        #only plot raw data if not called
        if fig is not None:
       #     if kwargs.get("legend",None) is None:
       #         dataPlot_kwargs["legend"] = LEGEND.ROT
            self.plot(*args,**data_Plot_kwargs)

        # rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas,Epot,*args, **dataPlot_kwargs)
        y_axis_unit="AAA"
        y = self.get_i_at_E(Epot,*args,**kwargs)
        y_axis_unit = y[0].unit
        y_axis_title = y[0].quantity
        
        rot = [lsv.rotation for lsv in self.datas ]
        E = [Epot for x in y]
        style = self.datas[0].get_point_color()
        #print(style)
        #print(E)
        #print(y)
        data_plot.plot(E,[float(i) for i in y],style)
       
        # Levich analysis
        B_factor = Levich(rot, y, y_axis_unit, y_axis_title, style, self.dir, plot=analyse_plot )
        if fig is not None:
            print("Levich analysis" )
            print("dir", f"\t{self.dir}     " )
            print(" :    ",f"\t{B_factor.unit}")
            print("slope:", "\t{:.2e}".format(B_factor.value) )
        saveFig(fig,**kwargs)
        return B_factor

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
        data_plot, analyse_plot, fig = create_KouLev_data_analysis_plot("Data",*args,**kwargs)

         #########################################################
        # Make plot
        dataPlot_kwargs = kwargs
        dataPlot_kwargs["plot"] = data_plot

        if fig is not None:
            #dataplot_kwargs = update_legend(LEGEND.ROT,*args,**dataPlot_kwargs)
            self.plot(LEGEND.ROT,*args,**dataPlot_kwargs)

        # rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas,Epot,*args, **dataPlot_kwargs)
        y_axis_unit="AAA"
        y = self.get_i_at_E(Epot,*args,**kwargs)
        y_axis_unit = y[0].unit
        y_axis_title = y[0].quantity
        
        E = [Epot for x in y]
        style = self.datas[0].get_point_color()
        #print(style)
        #print(E)
        #print(y)
        data_plot.plot(E,[float(i) for i in y],style)
        
        rot_inv = [(lsv.rotation)**-0.5 for lsv in self.datas ]
        y_inv = [y_val**-1 for y_val in y]
        
        x_values = [x.value for x in rot_inv]
        y_values = [y.value for y in y_inv]
        
        
        point_style = self.datas[0].get_point_color()
        
        pkwargs={"plot" : analyse_plot,
                 "style" : point_style}
        p = plot_options(pkwargs)
        p.options["plot"]=analyse_plot
        p.set_x_txt(rot_inv[0].quantity,rot_inv[0].unit)
        p.set_y_txt(y_inv[0].quantity,y_inv[0].unit)

        p.x_data=x_values
        p.y_data=y_values
        # analyse_plot.plot(rot_inv, y_inv, style)
        p.exe()
        
        line_style = self.datas[0].get_line_color()

        x_fit = np.insert(x_values, 0, 0)  
        x_qv = QV(1, "rpm^0.5","w")
        x_u =  QV(1, x_qv.unit,x_qv.quantity)** -0.5

        # FIT pos

        m_pos, b = np.polyfit(x_values, y_values, 1)
        dydx_qv= y_inv[0] / rot_inv[0]
        y_fit= m_pos * x_fit + b
        slope_pos = QV(m_pos, dydx_qv.unit, dydx_qv.quantity)

        B_pos = slope_pos**-1
        line, = analyse_plot.plot(x_fit, y_fit, line_style )
        line.set_label(f"pos: m={B_pos.value:3.3e}")

        saveFig(fig,**kwargs)
        ####################################
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
        """
        return slope_pos
    
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
        E.append(Epot)
        y_axis_title = str(cv.i_label)
        y_axis_unit = str(cv.i_unit)
    rot = np.array(rot)
    y = np.array(y)
    CV_plot = cv_kwargs["plot"]
    CV_plot.plot(E, y, STYLE_POS_DL)
    CV_plot.legend()
    return rot, y, E, y_axis_title, y_axis_unit
