from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV

from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig, ENUM_legend




def make_Bode_plot(*args, **kwargs):
    
    fig = make_plot_2x("Bode Plot",True)
    plot_Z = fig.plots[0]
    plot_Z.set_xscale("log")
    lims_x ={"left": None,"right": None}
    lims_x.update(kwargs)
    #plot_Z.set_xlim(lims_x)
    plot_phase = fig.plots[1]
    plot_phase.set_xscale("log") 
    bode_f_args=dict()
    bode_f_args["plot"]=plot_Z
    bode_f_args["xscale"]="log"
    bode_f_args["style"]="o"
    
    bode_f = plot_options(bode_f_args )
    bode_f.set_x_txt("Freq", "Hz")
    bode_f.set_y_txt("Z", "Ohm")
    bode_f.render_plot()
    bode_A_args=dict()
    
    bode_A_args["plot"]=plot_phase
    bode_A_args["xscale"]="log"
    bode_A_args["style"]="o"
    bode_phase = plot_options(bode_A_args )
    bode_phase.set_x_txt("Freq", "Hz")
    bode_phase.set_y_txt("Phase", "rad")
    
    bode_phase.render_plot()
    BODE_op= {"bode_Z": plot_Z,"bode_phase": plot_phase}
    return plot_Z, plot_phase,bode_f,bode_phase


def bode_plot_Z(plot_Z:None,**kwargs):
    
    bode_f_args=dict()
    bode_f_args["plot"]=plot_Z
    bode_f_args["xscale"]="log"
    bode_f_args["style"]="o"
    
    bode_f = plot_options(bode_f_args )
    bode_f.set_x_txt("Freq", "Hz")
    bode_f.set_y_txt("Z", "Ohm")
    bode_f.render_plot()
    return bode_f

def bode_plot_phase(plot_phase:None):
    """_summary_

    Args:
        plot_phase (None): _description_

    Returns:
        _type_: plot_options
    """
    bode_A_args=dict()
    if plot_phase is not None:
        bode_A_args["plot"]=plot_phase
    bode_A_args["xscale"]="log"
    bode_A_args["style"]="o"
    bode_phase = plot_options(bode_A_args )
    bode_phase.set_x_txt("Freq", "Hz")
    bode_phase.set_y_txt("Phase", "rad")
    bode_phase.render_plot()
    return bode_phase