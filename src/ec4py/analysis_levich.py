
import numpy as np

from .util import Quantity_Value_Unit as Q_V
from .util_graph import plot_options,quantity_plot_fix



def Levich(rot,y_data, y_axis_unit,y_axis_title,STYLE_DL, line_title="",*args, **kwargs):
 #Levich analysis
        p = plot_options(kwargs)
        p.set_title("CVs")
        line, analyse_plot = p.exe()
        legend = p.legend
        
        analyse_plot.plot(rot,y_data,STYLE_DL)
        x_qv = Q_V(1, "rpm^0.5","w")
        x_qv = x_qv**0.5
        x_qv.value = 1
        x_rot = Q_V(1,x_qv.unit,x_qv.quantity)
        ##print("aa", x_qv.unit)
        y_qv = Q_V(1, y_axis_unit.strip(),y_axis_title.strip())
                
        analyse_plot.set_xlabel("$\omega^{0.5}$ ( rpm$^{0.5}$)")
        analyse_plot.set_ylabel(f"{quantity_plot_fix(y_axis_title)} ({quantity_plot_fix(y_axis_unit)})" )
        #analyse_plot.set_xlim([0, math.sqrt(rot_max)])
        #analyse_plot.xlim(left=0)
        x_plot = np.insert(rot,0,0)
        m , b = np.polyfit(rot, y_data, 1)
        y_pos= m *x_plot+b
        ##print("AAA",x_rot, "BBB", x_rot.quantity)
       
        
        B_factor = Q_V(m , y_axis_unit,y_axis_title) #/ x_rot
        ##print("AAA",B_factor_pos, "BBB", B_factor_pos.quantity)
        STYLE_DL= STYLE_DL[0]+"-"
        line, = analyse_plot.plot(x_plot,y_pos,STYLE_DL )
        line.set_label(f"{line_title} B={m :3.3e}")
        #ax.xlim(left=0)
        analyse_plot.legend()
        analyse_plot.set_xlim(left=0,right =None)
        
    
        return B_factor
    
def diffusion_limit_corr(current, idl:float):
    if idl == 0:
        with np.errstate(divide='ignore'):
                y_data_corr = [1/(1/i-1/idl) for i in current]      
    else:
            y_data_corr = current
    return y_data_corr