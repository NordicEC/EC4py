import numpy as np

from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options

def Tafel(x_data,y_data, y_axis_unit,y_axis_title,plot_color,lineName="",x_data_ext =None, y_data_ext =None,  **kwargs):
    """Tafel analys

    Args:
        x_data (_type_): potential data
        y_data (_type_): current data in log
        y_axis_unit (_type_): current unit
        y_axis_title (_type_): current quantity
        plot_color (_type_): _description_
        lineName (str, optional): _description_. Defaults to "".
        x_data_ext (_type_, optional): _description_. Defaults to None.
        y_data_ext (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    p = plot_options(kwargs)
    p.set_title("Tafel")
    line, analyse_plot = p.exe()
    Tafel_options={ 
                   lineName :"" 
                   }
    
    ##FIT    
    m, b = np.polyfit(x_data,y_data, 1)
    y_fit= m*x_data+b
    Tafel_slope = (Q_V(1/ m,"V/dec","dE"))
    
    if x_data_ext is not None and y_data_ext is not None: 
        analyse_plot.plot(x_data_ext, y_data_ext,c= plot_color)
    else:    
        analyse_plot.plot(x_data, y_data,c= plot_color)
    line, = analyse_plot.plot(x_data, y_fit, linewidth=3.0, c= plot_color)
    line.set_label(f"{lineName} m={1000/m:3.1f}mV/dec")
    
        
        
        #print(cv.setup)
    #print(rot)

    y_values = np.array(y_data)
    x = np.array(x_data)
    
    analyse_plot.set_xlim(x.min()-0.1,x.max()+0.1)
    
    analyse_plot.set_xlabel("E ( V )")
    analyse_plot.set_ylabel(f"log( {y_axis_title} / {y_axis_unit} )" )
    
    analyse_plot.legend()
       
    return Tafel_slope 