""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
import math
import numpy as np
import pandas as pd

from .ec_data import EC_Data
from .lsv_data import LSV_Data
from .ec_datas_util import EC_Datas_base,check_paths


from pathlib import Path
import copy
from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig,NEWPLOT,LEGEND,ANALYSE_PLOT,DATA_PLOT,update_legend,should_plot_be_made

from .util_voltammetry import create_Tafel_data_analysis_plot,create_RanSev_data_analysis_plot,create_Rate_data_analysis_plot,create_Levich_data_analysis_plot,create_KouLev_data_analysis_plot
from .util_voltammetry import Voltammetry, OFFSET_AT_E_MIN, OFFSET_AT_E_MAX, OFFSET_LINE


from .analysis_levich import Levich
from .analysis_tafel import Tafel
from .analysis_ran_sev   import ran_sev
from .analysis_rate   import sweep_rate_analysis




STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class LSV_Datas(EC_Datas_base):
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
    def __init__(self, paths:list[Path] | Path = None,*args, **kwargs):
        EC_Datas_base.__init__(self,*args, **kwargs)
        # self.datas = []
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
    
    def __len__(self):
        return len(self.datas)
    
    def __add__(self, other: LSV_Data):
        
        """Add to the current

        Args:
            other (LSV_Data): LSV_Data to be added 

        Returns:
            LSV_Datas: returns a copy of the initial dataset. 
        """

        new_LSVs = copy.deepcopy(self)
        new_LSVs.add(other)
        return new_LSVs
    
    def __sub__(self, other: LSV_Data):
        """Subtract from the current.

        Args:
            other (LSV_Data): LSV_Datas, LSV_Data or number to be subtracted 

        Returns:
            LSV_Datas: returns a copy of the initial dataset. 
        """
        new_LSVs = copy.deepcopy(self)
        new_LSVs.sub(other)
        return new_LSVs
        
    def __mul__(self, other: float):
        """multiply

        Args:
            other (float): LSV_Data  or number to be added 

        Returns:
            LSV_Datas: returns a copy of the initial dataset. 
        """
        new_LSVs = copy.deepcopy(self)
        new_LSVs.mul(other)
        return new_LSVs
    
    def __truediv__(self, other: float):
        """divide the current by a number.

        Args:
            other (float): number 

        Returns:
            LSV_Datas: returns a copy of the initial dataset. 
        """
        new_LSVs = copy.deepcopy(self)
        new_LSVs.div(other)
        return new_LSVs
    #############################################################################

    
    
    def add(self,other):
        """add

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, LSV_Datas) or isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].add(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for data in self.datas:
                data.add(other)  
        ##########################################        
    def sub(self,other):
        """sub

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, LSV_Datas) or isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].sub(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for data in self.datas:
                data.sub(other)
                
    def mul(self,other):
        """multiply the current by a number.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, LSV_Datas) or isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].mul(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for data in self.datas:
                data.mul(other)
            
    def div(self,other):
        """divide the current by a number.

        Args:
            other (_type_, optional): _description_. Defaults to CV_Data.
        """
        if isinstance(other, LSV_Datas) or isinstance(other, list):
            if len(other) == len(self.datas):
                for i in range(0,len(self.datas)):
                    self.datas[i].div(other[i])
            else:
                raise ValueError('The data sets are not of the same length.')
        else:
            for data in self.datas:
                data.div(other)  
        
    
    
    
    def append(self,LSV:LSV_Data):
        if isinstance(LSV, LSV_Data):
            self.datas.append(LSV)
        else:
            print("wrong type, must be 'LSV_Data'")
    #def pop(self,index):
    #    self.datas.pop(index)
        
    @property
    def rate(self):
        rates=[]
        for lsv in self.datas:
            
            rates.append(lsv.rate)
        return rates
    
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero.
        
        Args:
            E (float): potential where to set the current to zero. 

        """
        for x in self.datas:
            x.set_i_at_E_to_zero(E,*args,**kwargs)
            
    ################################################################
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
            list[Quantity_Value_Unit]: current
        """
        i_at_E=[]
        for x in self.datas:
            lsv = copy.deepcopy(x)
            
            a =lsv.get_i_at_E(E,*args,**kwargs)
            i_at_E.append(a)
            
        return i_at_E
    
    ################################################################  

    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of minimum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            list: (Quantity_Value_Unit | None) of found potentials.
        """
        return [lsv.get_E_of_max_i(E1,E2,*args,*kwargs) for lsv in self.datas]
    
################################################################  

    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of minimum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            list: (Quantity_Value_Unit | None) of found potentials.
        """
        return [lsv.get_E_of_min_i(E1,E2,*args,*kwargs) for lsv in self.datas]

##################################################################################################################

    def set_active_RE(self,shift_to: str | tuple = None):     
        """Set active reference electrode for plotting.
        
        - RHE    - if values is not already set, use ".set_RHE()"
        
        - SHE    - if values is not already set, use ".set_RHE()"
        - None to use the exerimental 
        """
        for x in self.datas:
            x.set_active_RE(shift_to)
        return
################################################################  

    def norm(self,*args, **kwargs):
        for x in self.datas:
            x.norm(args)
        return
    
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
        
        Returns:
            the plot handler
            
        """
        if should_plot_be_made(*args):
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
        else:
            return None

    #################################################################################################    
    
    def RateAnalysis(self, Epot:float,*args, **kwargs):
        """.

        Args:
            Epot (float): Potential at which the current will be used.

        Returns:
            List : Slope of data based on positive and negative sweep.
        """
    
        data_plot, analyse_plot,fig = create_Rate_data_analysis_plot(*args,**kwargs)
       
        #########################################################
        # Make plot
        loc_kwargs = kwargs
        loc_kwargs["plot"] = data_plot
        
        rate = [float(val) for val in self.rate]
        E =[Epot for val in self.rate]
        rate_unit = "V /s"
        if len(self)>0:
            rate_unit = self.rate[0].unit
       
        if fig is not None:
            self.plot(LEGEND.RATE,*args, **loc_kwargs)

        y = self.get_i_at_E(Epot,*args, **kwargs)
        #PLOT
        style = self.datas[0].get_point_color()
        if data_plot is not None:
            data_plot.plot(E, y, style)
        y_axis_title =y[0].quantity
        y_axis_unit = y[0].unit
        # print(y_axis_title)
        analyse_kwargs = kwargs
        analyse_kwargs["plot"] = analyse_plot
        B_factor_pos = sweep_rate_analysis(rate, y, y_axis_unit, y_axis_title, style, self.dir,rate_unit,*args, **analyse_kwargs )
        
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
    def export_Array(self):
        """Exports a Numpy Array

        Returns:
            Tuplet: Numpy Array of current data, Voltage 
        """
        size = [len(Voltammetry().E),len(self.datas)]
        m = np.zeros(size)
        col_names= [f"{self.datas[0].E_label} /{self.datas[0].E_unit}"]
        #print(m.shape,len(self.datas))
        for x in range(0,len(self.datas)):
            #print(x,self.datas[x].i.shape)
            m[:,x+1] = self.datas[x].i
            col_names.append(f"{self.datas[x].i_label}_{self.datas[x].name} / {self.datas[x].i_unit}")
        #print(col_names)
        return m,Voltammetry().E

    def export_DataFrame(self):
        size = [len(Voltammetry().E),len(self.datas)+1]
        m = np.zeros(size)
        col_names= [f"{self.datas[0].E_label} /{self.datas[0].E_unit}"]
        #print(m.shape,len(self.datas))
        m[:,0]=Voltammetry().E
        for x in range(0,len(self.datas)):
        
            #print(x,self.datas[x].i.shape)
            m[:,x+1] = self.datas[x].i
            if self.datas[x].is_MWE:
                name = f"{self.datas[x].name}#{self.datas[x].setup_data._MWE_CH}"
            else:
                name =f"{self.datas[x].name}"
            #print(name)
            col_names.append(f"[{name}] {self.datas[x].i_label} / {self.datas[x].i_unit}")
        #print(len(col_names),col_names)
        df = pd.DataFrame.from_records(m,columns=col_names)
        return df

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
"""