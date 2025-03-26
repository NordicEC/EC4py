
import numpy as np
from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options, quantity_plot_fix



"""
This file is using the Randles–Sevcik equation and plot. 
Please see: 
https://en.wikipedia.org/wiki/Randles%E2%80%93Sevcik_equation
for more info.

"""

def sweep_rate_analysis(rate_values, current, y_axis_unit:str="A", y_axis_title:str="i", STYLE_DL: str="bo", line_title:str="",  rate_unit:str="V /s", *args, **kwargs):
        """Generates a Randles–Sevcik plot and fits a line.  

        Args:
            rate (_type_): rotation rate.
            y_data (_type_): _description_
            y_axis_unit (str): _description_
            y_axis_title (str): _description_
            STYLE_DL (str, optional): _description_. Defaults to "bo".
            line_title (str, optional): _description_. Defaults to "".

        Returns:
            Quantity_Value_Unit: Levich slope
        """
        
        
        
        # p.set_xlabel("$\omega^{0.5}$ ( rpm$^{0.5}$)")
        #p.set_ylabel(f"{quantity_plot_fix(y_axis_title)} ({quantity_plot_fix(y_axis_unit)})" )
        
        
        # rate_sqrt = np.sqrt(np.array([float(val) for val in rate_values]))
        rate = (np.array([float(val) for val in rate_values]))
        
        y_data = np.array([float(val) for val in current])
        # ([print(float(val)) for val in current])
        
        # analyse_plot.plot(rot_sqrt, y_data, STYLE_DL_plot)
        x_qv = Q_V(1, rate_unit, "v")
        # x_qv = x_qv**0.5
        x_qv.value = 1
        x_rot = Q_V(1, x_qv.unit, x_qv.quantity)
        ##print("aa", x_qv.unit)
        y_qv = Q_V(1, y_axis_unit.strip(), y_axis_title.strip())
        
        m , b = np.polyfit(rate, y_data, 1)
        rate_t = np.sort(rate)
        x_plot = np.insert(rate_t,0, 0.8*rate_t[0]) #rate_t[0]*
        x_plot = np.append(x_plot,np.nanmax(rate_t)*1.2)
        
        y_pos= m * x_plot + b
        ##print("AAA",x_rot, "BBB", x_rot.quantity)

        B_factor = Q_V(m , y_axis_unit, y_axis_title) / x_rot
        B_factor = B_factor * Q_V(1, "C V /A /s") 
        ##print("AAA",B_factor_pos, "BBB", B_factor_pos.quantity)
        
        #Levich Plot
        p = plot_options(kwargs)
        p.no_smooth()
        
        p.set_title("Sweep Rate",1)
        p.set_x_txt("$v$", f"{rate_unit}")
        p.set_y_txt(y_axis_title, y_axis_unit)

        p.options["style"]=STYLE_DL[0]+"o"
        p.y_data = y_data
        p.x_data = rate
        line, analyse_plot = p.exe()        
        # print(p.get_x_txt())
        STYLE_DL= STYLE_DL[0] + "-"
        line, = analyse_plot.plot(x_plot, y_pos, STYLE_DL )
        line.set_label(f"{line_title} {m :3.3e} {B_factor.unit}")
        #ax.xlim(left=0)
        analyse_plot.legend()
        #analyse_plot.set_xlim(left=0, right =None)

        return B_factor

