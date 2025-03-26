"""
Utility module.

"""

#import math
from scipy.signal import savgol_filter, medfilt
import numpy as np
#from scipy import ndimage, datasets
import matplotlib.pyplot as plt
from collections import namedtuple
#from fractions import Fraction
#import matplotlib.pyplot as plt
from enum import StrEnum
#from .util import Quantity_Value_Unit as Q_V



NEWPLOT = "new_plot"

NO_PLOT = "no_plot"

Figure = namedtuple("Figure", ["fig", "plots"])
"""Tuplet:
    - fig   : a plt.figure() object.
    - plots :  subplots of the figure
"""

ANALYSE_PLOT = "analyse_plot"
DATA_PLOT = "data_plot"
PLOT = "plot"

class ENUM_legend(StrEnum):
    NONE ="_"
    NAME = "legend_name"
    DATE = "legend_date"
    TIME = "legend_time"
    DATETIME = "legend_datetime"
    ROT = "legend_rot"
    RATE = "legend_rate"
    VSTART = "legend_start"
    V1 = "legend_v1"
    V2 = "legend_v2"

LEGEND = ENUM_legend

def update_legend(*args,**kwargs):
    loc_args = list(args) 
    #loc_args.insert(0,listargs)
    default_legend=kwargs.get("default_legend",None)
    if default_legend is not None:
         loc_args.insert(0,default_legend)
   
    for arg in loc_args:
        if isinstance(arg,ENUM_legend):
            kwargs["legend"]=str(arg).replace("legend_","")
        if isinstance(arg,str):
            if arg.startswith("legend"):
                kwargs["legend"]=str(arg).replace("legend_","")
    return kwargs


def make_plot_1x(Title:str):
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(6)
    plt.suptitle(Title)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1.0, hspace=0.8)
    plot1 = fig.subplots()
    
    return Figure(fig,[plot1])

def make_plot_2x(Title:str,Vertical = False):
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(13)
    plt.suptitle(Title)
    if Vertical:
        fig.set_figheight(5)
        fig.set_figwidth(4)
        plot1,plot2 = fig.subplots(2,1)
    else:
        fig.set_figheight(5)
        fig.set_figwidth(13)
        plot1,plot2 = fig.subplots(1,2)
    return Figure(fig,[plot1,plot2])
    #
    #return plot1, plot2
    
def make_plot_2x_1(Title:str):
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(13)
    plt.suptitle(Title)
    ax_right = fig.add_subplot(122)
    ax_left_top = fig.add_subplot(221)
    ax_left_bottom = fig.add_subplot(223)
    ax_left_bottom.label_outer()
    ax_left_top.label_outer()
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1.0, hspace=0.8)
    #plot1,plot2 = fig.subplots(1,2)
    return Figure(fig,[ax_left_top, ax_left_bottom, ax_right ])
    # return ax_left_top, ax_left_bottom, ax_right


def quantity_plot_fix(s:str):
    list_of_quantities = str(s).strip().split(" ", 100)
    s_out =""
    for single_quantity in list_of_quantities:
        aa = single_quantity.strip().split("^",2)
        nyckel = aa[0]
        if len(aa)>1:                   #if "^" was found.
            nyckel = nyckel + "$^{" + aa[1] + "}$"  
        s_out = s_out +" " + nyckel
    #print("AA", s_out.strip())
    return s_out.strip()  


class plot_options:
    def __init__(self, kwargs):
        self.fig = None
        self.name = NEWPLOT
        self.x_label="x"
        self.x_unit = "xunit"
        self.y_label = "y"
        self.y_unit = "y_unit"
        self.x_data = []
        self.y_data =[]
        #self.x = tuple(self.x_data,self.x_label,self.x_unit)
        self.options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'y_median'   : 0,
            'yscale':None,
            'xscale':None,
            PLOT : NEWPLOT,
            'dir' : "all",
            'legend' : "_",
            'xlabel' : "def",
            'ylabel' : "def",
            'style'  : "",
            'title'  : ""
        }

        self.options.update(kwargs)
        return
    
    def set_title(self,title:str = "", override: bool=False):
        if self.options['title'] == "" or override:
            self.options['title'] = title
    
    def set_y_txt(self, label, unit):
        self.y_label = label
        self.y_unit = unit
        
    def set_x_txt(self, label, unit):
        self.x_label = label
        self.x_unit = unit
        

    def get_y_txt(self):
        return str(self.y_label + " ("+ self.y_unit +")")
    def get_x_txt(self):
        return str(self.x_label + " ("+ self.x_unit +")")
    
    
    def get_legend(self):
        return str(self.options['legend'])
    
    @property
    def legend(self):
        return self.get_legend()

    @legend.setter
    def legend(self, value:str) -> str:
        self.options['legend'] = value
        #return self.get_legend()
    
    def get_x_smooth(self):
        return int(self.options['x_smooth'])
    
    def get_y_smooth(self):
        return int(self.options['y_smooth'])
    
    def get_dir(self):
        return str(self.options['dir'])
    
    def get_plot(self):
        
        
        return self.options[PLOT]
    
    def smooth_y(self, ydata =[]):
        #try:
        y_smooth = self.get_y_smooth()
        # print("SA VALUE")
        # print(y_smooth)
        if(y_smooth > 0) and len(ydata)>2:
            ydata_array= np.isnan(ydata)
            for i in range(len(ydata_array)):
                if ydata_array[i]:
                    ydata[i]=0
            ydata = savgol_filter(ydata, y_smooth+1, 1)
            for i in range(len(ydata_array)):
                if ydata_array[i]:
                    ydata[i]=np.nan
                    
            # print("SA FITER")
    #except:
        #    pass
        return ydata
    
    def median_y(self, ydata =[]):
        try:
            y_median = self.options["y_median"]
            if(y_median>0): 
                if y_median % 2 ==0:
                    y_median +=1           
                ydata_s = medfilt(ydata, y_median)
            else:
                ydata_s = ydata
        except:
            pass
        return ydata_s
    
    def smooth_x(self, xdata):
        try:
            x_smooth = self.get_x_smooth()
            if(x_smooth > 0):
                xdata = savgol_filter(xdata, x_smooth, 1)
        except:
            pass
        return xdata
            
    
    def fig(self, **kwargs):
        try:
            ax = kwargs[PLOT]
        except KeyError("plot keyword was not found"):
            #fig = plt.figure()
            #  plt.subtitle(self.name)
            fig = make_plot_1x(self.options['title'])
            ax = fig.plots[0]

    def no_smooth(self):
        self.options["y_smooth"]=0
        self.options["x_smooth"]=0
        self.options["y_median"]=0
        return
    
    def exe(self):
        """_summary_

        Returns:
            line, ax: Line and ax handlers
        """
        ax = self.options[PLOT]
        fig = None
        if ax == NEWPLOT or ax is None:
           # fig = plt.figure()
           # plt.suptitle(self.name)
            self.fig = make_plot_1x(self.options['title'])
            ax = self.fig.plots[0]
            if self.options['yscale']:
                ax.set_yscale(self.options['yscale'])
            if self.options['xscale']:
                ax.set_xscale(self.options['xscale'])
        
        
        try:
            y_median = int(self.options['y_median'])
            if y_median > 0:
                if y_median % 2 ==0:
                    y_median +=1 
                #print("median filter Y", y_median)
                self.y_data = medfilt(self.y_data, y_median)
        except:
            pass
        self.y_data = self.smooth_y(self.y_data)
        try:
            yscale = ax.get_yscale()
            if yscale == "log":
                self.y_data=abs(self.y_data)
        except:
            pass
       
        
        try:
            x_smooth = int(self.options['x_smooth'])
            if x_smooth > 0:
                self.x_data = savgol_filter(self.x_data, x_smooth, 1)
            xscale = ax.get_xscale()
            if xscale == "log":
                self.x_data=abs(self.x_data)
        except:
            pass
        line = None
        try:
            line, = ax.plot(self.x_data, self.y_data, self.options['style'])
            #line,=analyse_plot.plot(rot,y_pos,'-' )
            if self.x_data is not None:
                line.set_label( quantity_plot_fix(self.get_legend()) )
                if self.get_legend()[0] != "_":
                    ax.legend()
            
        except:  # noqa: E722
            pass
        ax.set_xlabel(f'{quantity_plot_fix(self.x_label)} ({quantity_plot_fix(self.x_unit)})')
        ylabel = quantity_plot_fix(self.y_label) + " (" + quantity_plot_fix(self.y_unit)+ ")"
        #ax.set_ylabel(f'{quantity_plot_fix(self.y_label)}    {quantity_plot_fix(self.y_unit)}')
        #print(f'{ylabel}')
        ax.set_ylabel(f'{ylabel}')
        
        return line, ax
    
    def render_plot(self):
        ax = self.options[PLOT]
        if ax == NEWPLOT or ax is None:
            return
        else:
            ax.set_xlabel(f'{quantity_plot_fix(self.x_label)} ({quantity_plot_fix(self.x_unit)})')
            
            ylabel = quantity_plot_fix(self.y_label) + " (" + quantity_plot_fix(self.y_unit)+ ")"
            ax.set_ylabel(f'{ylabel}')
        return
    
    def close(self, *args):
        # print("CLOSE:", args)
        for item in args:
            s = str(item).casefold()    
            if s == "noshow".casefold():
                # print("CLOSING")
                plt.close('all')
                break
        return
    
    def saveFig(self,**kwargs):
        #print("fig")
        saveFig(self.fig,**kwargs)
            


def saveFig(fig:Figure,**kwargs):
    if fig is not None:
            name = kwargs.get("savefig",None)
            if name is not None:
                fig.fig.savefig(name, dpi='figure', format=None, bbox_inches ="tight")
    else:
        # print("fig is non")
        pass