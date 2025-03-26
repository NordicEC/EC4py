""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations

from pathlib import Path

import copy

from .ec_data import EC_Data
from .ec_data_util import EC_Channels
from .eis_data import EIS_Data
from .ec_setup import EC_Setup
from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV

from .util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x,saveFig
from .util_eis import make_Bode_plot


class EIS_Datas:
    """
    """
    def __init__(self, paths:list[Path] | Path, *arg, **kwargs):

        if not isinstance(paths,list ):
            path_list = [paths]
        #if isinstance(paths,Path ):
        #    path_list = [paths]
        else:
            path_list = paths
        self.datas = [EIS_Data() for i in range(len(path_list))]
        index=0
        for path in path_list:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec,*arg, **kwargs)
            finally:
                index=index+1 
        #print(index)
        return
    
    
    def nq(self,*args, **kwargs):
        
        p = plot_options(kwargs)
        p.set_title("NQ")
        line, EIS_plot = p.exe()
        # EIS_plot.lines.pop(0)
        # legend = p.legend
        
        EISs = copy.deepcopy(self.datas)
        
        EIS_kwargs = kwargs
        lines = []
        for eis in EISs:
            #rot.append(math.sqrt(cv.rotation))


            EIS_kwargs["plot"] = EIS_plot
            EIS_kwargs["name"] = eis.setup_data.name

            line, ax = eis.nq(*args, **EIS_kwargs)
            lines.append(line)
        for line in lines:
            if line.get_label() != "_":
                EIS_plot.legend()
                break
        p.saveFig(**kwargs)
        return EIS_plot,lines
    
    def bode(self,*args, **kwargs):
        """Creates a bode plot:
        
        kwargs:
            maxf: set max frequency in Hz
            minf: set min frequency in Hz

        Returns:
            _type_: _description_
        """  
       
        plotZ,plotA,opt_f,opt_A =make_Bode_plot(*args,**kwargs)
        opt_f.exe()
        opt_A.exe()
        lines = []
        for data in self.datas:
            line,a = data.bode(*args, bode_Z=plotZ,bode_phase=plotA,**kwargs)
            lines.append(line[0])
        
       
        for line in lines:
            if line.get_label() != "_":
                # print("a",line.get_label())
                plotZ.legend()
                break
        # opt_f.render_plot()
       
        # bode_f.set_y_txt(data.i_label, data.i_unit)  