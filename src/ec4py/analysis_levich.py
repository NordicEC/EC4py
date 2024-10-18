
import numpy as np
from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options, quantity_plot_fix


def Levich(rot, y_data, y_axis_unit:str="A", y_axis_title:str="i", STYLE_DL: str="bo", line_title:str="",  rot_unit:str="rpm", *args, **kwargs):
        """Generates a Levich plot and fits 

        Args:
            rot (_type_): rotation rate.
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
        
        
        
        rot_sqrt = np.sqrt(np.array(rot))
        
        # analyse_plot.plot(rot_sqrt, y_data, STYLE_DL_plot)
        x_qv = Q_V(1, rot_unit, "w")
        x_qv = x_qv**0.5
        x_qv.value = 1
        x_rot = Q_V(1, x_qv.unit, x_qv.quantity)
        ##print("aa", x_qv.unit)
        y_qv = Q_V(1, y_axis_unit.strip(), y_axis_title.strip())
        
        x_plot = np.insert(rot_sqrt, 0, 0)
        m , b = np.polyfit(rot_sqrt, y_data, 1)
        y_pos= m * x_plot + b
        ##print("AAA",x_rot, "BBB", x_rot.quantity)

        B_factor = Q_V(m , y_axis_unit, y_axis_title) / x_rot
        ##print("AAA",B_factor_pos, "BBB", B_factor_pos.quantity)
        
        #Levich Plot
        p = plot_options(kwargs)
        p.set_title("Levich",1)
        p.set_x_txt("$\omega$^0.5", f"{rot_unit}^0.5")
        p.set_y_txt(y_axis_title, y_axis_unit)

        p.options["style"]=STYLE_DL[0]+"o"
        p.y_data = y_data
        p.x_data = rot_sqrt 
        line, analyse_plot = p.exe()        
        print(p.get_x_txt())
        STYLE_DL= STYLE_DL[0] + "-"
        line, = analyse_plot.plot(x_plot, y_pos, STYLE_DL )
        line.set_label(f"{line_title} B={m :3.3e}")
        #ax.xlim(left=0)
        analyse_plot.legend()
        analyse_plot.set_xlim(left=0, right =None)

        return B_factor

def diffusion_limit_corr(current, idl:float):
    if idl is not None:
        with np.errstate(divide='ignore'):
                y_data_corr = [1/(1/i-1/idl) for i in current]      
    else:
            y_data_corr = current
    return y_data_corr
