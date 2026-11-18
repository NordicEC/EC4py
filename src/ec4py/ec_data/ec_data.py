""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import numpy.typing as npt
from numpy.typing import NDArray

import matplotlib.pyplot as plt
from pathlib import Path
from scipy import integrate
#from . import util
from ..util_graph import plot_options
from ..ec_setup.ec_setup import EC_Setup
from ..util import Quantity_Value_Unit as QV
#from .ec_util.ec_data_util import EC_Channels
from pathlib import Path
from ..ec_util.ec_data_base import index_at_time
#from .ec_util.ec_data_base import EC_Data_Base

from ..ec_util.ec_data_tdms import help_get_wf_prop

class EC_Data(EC_Setup):
    """ Reads and stores data from a TDMS file in the format of EC4 DAQ.

    """
    def __init__(self, path:Path|str="",*args, **kwargs):

        super().__init__(self,*args, **kwargs)
        # self._area=1
        # self._area_unit="cm^2"
        # self.rotation =0
        # self.rotation_unit ="/min"
        #sel_channels = EC_Channels()
        self.Time = np.array([], dtype=np.float64)
        self.E:npt.NDArray[np.float64] = np.array([], dtype=np.float64)
        self.i = np.array([], dtype=np.float64)
        self.U = np.array([], dtype=np.float64)
        self.Z_E = np.array([], dtype=np.float64)
        self.Phase_E = np.array([], dtype=np.float64)
        self.Z_U = np.array([], dtype=np.float64)
        self.Phase_U = np.array([], dtype=np.float64)
        self.path = ""
        self.rawdata:dict = {}
        """All setup information given in the file.
        """

        if path == "":
            # print("no path")
            return
        else:
            try:
                tdms_file = TdmsFile.read(path)
                tdms_file.close()
                self.path = str(path)
                self.log(f'EC_Data({self.path})')
                self.setup_data.fileName = Path(path).name
                # print(tdms_file.properties)
                
                try:
                    Items = tdms_file['Setup']['Item']
                    Value = tdms_file['Setup']['Value']
                    for x in range(len(Items)):
                        self.setup_data._setup[Items[x]] = Value[x]
                    self.setup_reset()
                except KeyError:
                    pass

                self.setup_data.name = str(tdms_file.properties['name'])
                self.setup_data.dateTime = np.datetime64(str(tdms_file.properties['dateTime']))
                
                self.rawdata = tdms_file['EC']

                rawdata_names = [x for x in self.rawdata]
                if 'Time' in rawdata_names:
                    
                    self.Time = np.asarray(self.rawdata['Time'].data,dtype=np.float64)
                if 'i' in rawdata_names:
                    self.i =    np.asarray(self.rawdata['i'].data,dtype=np.float64)
                if  'E' in rawdata_names:
                    self.E =    np.asarray(self.rawdata['E'].data,dtype=np.float64)
                if 'Z_E' in tdms_file['EC']:
                    self.Z_E = np.asarray(tdms_file['EC']['Z_E'].data,dtype=np.float64)  # not all data file contains U channel
                    self.Phase_E = tdms_file['EC']['Phase_E'].data  # not all data file contains U channel
                
                if 'Ucell' in tdms_file['EC']:
                    self.U = np.asarray(tdms_file['EC']['Ucell'].data,dtype=np.float64)  # not all data file contains U channel
                
                if 'Z_cell' in tdms_file['EC']:
                    self.Z_U = np.asarray(tdms_file['EC']['Z_cell'].data,dtype=np.float64)  # not all data file contains U channel
                if 'Phase_cell' in tdms_file['EC']:
                    self.Phase_U = np.asarray(tdms_file['EC']['Phase_cell'].data,dtype=np.float64)  # not all data file contains U channel
                
                
                
                # [self.area, self.setup_data._area_unit] = util.extract_value_unit(self.setup["Electrode.Area"])
                # [self.rotation, self.setup_data.rotation_unit] = util.extract_value_unit(self.setup["Inst.Convection.Speed"])

            except FileNotFoundError:
                print(f"TDMS file was not found: {path}")
            except KeyError as e:
                print(f"TDMS error: {e}")
        
    #def set_area(self, value, unit):
    #    self._area = value
    #    self._area_unit = unit

    #def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
     #   return f"{self.setup_data.name}"
    def __repr__(self):
        """Get the name of the data file.
        """
        return f"EC_Data('{self.setup_data.fileName}')"
    
    @property 
    def channels(self):
        ch_names=list()
        for ch_name in self.rawdata:
                ch_names.append(ch_name)
        return ch_names

    

    def get_channel(self, datachannel: str) -> tuple[npt.NDArray[np.float64], str, str,float]:
        """
        Get the channel of the EC4 DAQ file.

        Returns:
            tuple: [channel, quantity-name, unit name]


        - Time
        - E,U , E-IZ,E-IR
        - i, j
        - Z_E. Z_U

        """
        if self.rawdata is None:
            info=[np.array([], dtype=np.float64),"","",1]
        else:
            dt = 1
            if 'Time' in self.rawdata:
                dt = self.rawdata["Time"].properties.get("wf_increment", 1)
            info=[np.array([], dtype=np.float64),"","",dt]

        match datachannel:
            case "Time":
                info[0:3] = [self.Time, "t", "s"]
            case "E":
                info[0:3] = [self.E, "E", "V"]
            case "U":
                info[0:3] = [ self.U, "U", "V"]
            case "i":
                info[0:3] = [ self.i, "i", "A"]
            case "j":
                info[0:3] = [ self.i/float(self.area), "j", f"A/{self.area.unit}"]
            case "Z_E":
                info[0:3] = [ self.Z_E, "Z_E", "Ohm"]
                info[1:4] = help_get_wf_prop(self.rawdata, datachannel)
            case "Z_U":
                info[0:3] = [ self.Z_U, "Z_U", "Ohm"]
                info[1:4] = help_get_wf_prop(self.rawdata, datachannel)
            case "Phase_E":
                info[0:3] = [ self.Phase_E, "Phase_E", "rad"]
            case "Phase_U":
                info[0:3] = [ self.Phase_U, "Phase_U", "rad"]
            case "R_E":
                # cosValue=self.Phase_E/self.Phase_E
                # index=0
                # for i in self.Phase_E:
                #    cosValue[index] = math.cos(self.Phase_E[index])
                #    index=index+1
                info[0:3] = [ self.Z_E * self.cosVal(self.Phase_E), "R_WE", "Ohm"]
            case "E-IZ":
                info[0:3] = [ self.E - self.i*self.Z_E, "E-IZ", "V"]

            case "E-IR":
                info[0:3] = [ self.E - self.i*self.Z_E, "E-IR", "V"]
            case _:
                # if datachannel in self.rawdata.channels():
                try:
                    if  self.rawdata is not None:
                        unit = self.rawdata[datachannel].properties.get("unit_string", "")
                        quantity = self.rawdata[datachannel].properties.get("Quantity", "")
                        dT = self.rawdata[datachannel].properties.get("wf_increment", 1)
                        info = [ self.rawdata[datachannel].data, str(quantity) , str(unit), dT]

                    else:
                        unit = "No channel"
                        quantity = "No channel"
                        dT = 1
                        info = [ np.array([], dtype=np.float64), str(quantity) , str(unit), dT]
                except KeyError:
                    raise NameError("Error:" + datachannel + " channel name is not supported")
        return tuple(info)
                # return np.array([2]), "No channel", "No channel"

    def cosVal(self, phase: NDArray):
        cosValue = phase/phase
        max_index = len(phase)
        for i in range(max_index):
            cosValue[i] = math.cos(self.Phase_E[i])
        return cosValue          

    def index_at_time(self, time_s_: float):
        return index_at_time(self.Time, time_s_ )
    
    ##################################################################################

    def _norm_single(self, current:npt.NDArray[np.float64], quantityUnit:QV, norm_to:str|tuple|None=None):
        norm_factor = self.get_norm_factors(norm_to)
        i_shifted = None
        qv = QV(0,"","")
        if norm_factor is not None:
            i_shifted = current.copy()
            
            i_shifted = np.asarray(current / float(norm_factor), dtype=np.float64)
            qv = quantityUnit/ norm_factor
           
            return i_shifted, qv
        else:
            return np.asarray(current,dtype=np.float64),quantityUnit
        

    def _norm(self, current:list[npt.NDArray[np.float64]]|npt.NDArray[np.float64], quantityUnit:QV, norm_to:str|tuple|None=None):
        
        norm_factor = self.get_norm_factors(norm_to)
        i_shifted = None
        qv = QV(0,"","")
        if norm_factor is not None:
            i_shifted = current.copy()
            if isinstance(current, list):
                i_shifted = current.copy()
                for i in range(len(current)):
                    # print("aaaa-shifting",i)
                    
                    i_shifted[i] = np.asarray(current[i] / float(norm_factor),dtype=np.float64)
            else:
                i_shifted = np.asarray(current / float(norm_factor), dtype=np.float64)
        #norm_factor_inv = norm_factor ** -1
            #qv = QV(1, i_unit, i_label) / norm_factor
            qv = quantityUnit/ norm_factor
            #self.i_unit = qv.unit
            #self.i_label = qv.quantity
            # print("aaaa-shifting",self.i_unit)
            return i_shifted, qv
        else:
            return np.asarray(current,dtype=np.float64),quantityUnit
    


    def plot(self, x_channel: str, y_channel: str, *args,**kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot = subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        '''
        # xlable ="wrong channel name"
        # xunit = "wrong channel name"
        # ylable ="wrong channel name"
        # yunit = "wrong channel name"

        plot_range = {
            'limit_min': -1,
            'limit_max': -1
        }
        plot_range.update(kwargs)

        options = plot_options(**kwargs)
        options.legend = self.legend(*args, **kwargs)
        #print(self.legend(*args, **kwargs))
        index_min = 0
        if plot_range["limit_min"] > 0:
            index_min = self.index_at_time(plot_range["limit_min"])
        index_max = len(self.Time)-1
        if plot_range["limit_max"] >0:
            index_max = self.index_at_time(plot_range["limit_max"])
        try:
            y_data, options.y_label, options.y_unit,y_dT = self.get_channel(y_channel)
            if y_data is not None:
                y_data = np.asarray(y_data,dtype=np.float64)
            if(options.y_unit == "A"):
                loc_args = args
                y_data,qv = self._norm_single(y_data,QV(1,options.y_unit,options.y_label),*loc_args)
                options.y_label = qv.quantity
                options.y_unit = qv.unit
            options.y_data = y_data[index_min:index_max]
        except NameError:
            print(f"ychannel {y_channel} not supported")
            
        try:
            if x_channel == "index".casefold():
                x_data = np.array(range(len(options.y_data)))
                options.x_label = "index"
                options.x_unit = ""
                options.x_data = x_data[index_min:index_max]
            else:
                x_data, options.x_label, options.x_unit,x_dT = self.get_channel(x_channel)
                x_data = np.asarray(x_data, dtype = np.float64)

                if(options.y_unit == "A"):
                    loc_args = args
                    x_data,qv = self._norm_single(x_data,QV(1,options.x_unit,options.x_label),*loc_args)
                    options.x_label = qv.quantity
                    options.x_unit = qv.unit
                    
                options.x_data = x_data[index_min:index_max]
        except NameError:
            print(f"xchannel {x_channel} not supported")
        
        #print(options.options["color"])
        pl = options.exe()
        options.saveFig(**kwargs)
        return pl

    def plot_rawdata(self):
        fig = plt.figure()

        plt.suptitle(self.setup_data.name)
        nr_data = len(self.rawdata) -1  # The time channel should not be counted.
        print(self.setup_data.name, ": EC data sets: ", nr_data)
        plot = fig.subplots(nr_data, 1)
        
        # ax = fig.subplots()
        index = 0
        for ch_name in self.rawdata:
            if(ch_name != 'Time'):
                try:
                    # time = channel.time_track()
                    plot[index].plot(self.rawdata[ch_name].time_track(),self.rawdata[ch_name].data)
                    yunit = self.rawdata[ch_name].properties["unit_string"]
                    plot[index].set_ylabel(f'{ch_name} / {yunit}')
                    plot[index].set_xlabel('Time / s')
                finally:
                    index +=1                    

        return
    
    def integrate(self, t_start, t_end, y_channel: str = "i"):
        """_summary_

        Args:
            t_start (_type_): _description_
            t_end (_type_): _description_
            y_channel (str, optional): _description_. Defaults to "i".

        Returns:
            _type_: _description_
        """
        idxmin=self.index_at_time(t_start)
        idxmax=self.index_at_time(t_end)+1
        y, quantity, unit,value = self.get_channel(y_channel)
        array_Q = integrate.cumulative_simpson(y[idxmin:idxmax], x=self.Time[idxmin:idxmax], initial=0)
        Charge = QV(array_Q[len(array_Q)-1]-array_Q[0],unit,quantity)*QV(1,"s","t")
        return Charge 
    
    def IR_comp_value(self, y_channel: str = "i", comp_value:float = float("nan") ,**kwargs):
        """_summary_

        Args:
            y_channel (str, optional): _description_. Defaults to "i".
            comp_value (float, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        y, quantity, unit,value = self.get_channel(y_channel)
        if comp_value is float("nan"):
            comp_value = float(kwargs.get('comp_resistor',float("nan")))
        if comp_value is not float("nan"):
            return np.asarray(y*(comp_value),dtype=np.float64)
        return np.zeros(len(y),dtype=np.float64)
        
