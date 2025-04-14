""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from nptdms import TdmsFile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from . import util
from .util_graph import plot_options
from .ec_setup import EC_Setup
from .util import Quantity_Value_Unit as QV
from .ec_data_util import EC_Channels
from pathlib import Path

class EC_Data(EC_Setup):
    """ Reads and stores data from a TDMS file in the format of EC4 DAQ.

    """
    def __init__(self, path=""):

        super().__init__()
        # self._area=1
        # self._area_unit="cm^2"
        # self.rotation =0
        # self.rotation_unit ="/min"
        sel_channels = EC_Channels()
        self.Time = np.array([], dtype=np.float64)
        self.E = np.array([], dtype=np.float64)
        self.i = np.array([], dtype=np.float64)
        self.U = np.array([], dtype=np.float64)
        self.Z_E = np.array([], dtype=np.float64)
        self.Phase_E = np.array([], dtype=np.float64)
        self.Z_U = np.array([], dtype=np.float64)
        self.Phase_U = np.array([], dtype=np.float64)
        self.path = ""
        self.rawdata = None
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
                
                self.rawdata = tdms_file['EC']
                self.Time = tdms_file['EC']['Time'].data
                try:
                    self.i = tdms_file['EC']['i'].data
                except KeyError:
                    pass
                
                self.E = tdms_file['EC']['E'].data
                self.setup_data.name = tdms_file.properties['name']
                self.setup_data.dateTime = tdms_file.properties['dateTime']
                try:
                    self.Z_E = tdms_file['EC']['Z_E'].data  # not all data file contains U channel
                    self.Phase_E = tdms_file['EC']['Phase_E'].data  # not all data file contains U channel
                except KeyError:
                    pass
                try:
                    self.U = tdms_file['EC']['Ucell'].data  # not all data file contains U channel
                except KeyError:
                    pass
                try:
                    self.Z_U = tdms_file['EC']['Z_cell'].data  # not all data file contains U channel
                    self.Phase_U = tdms_file['EC']['Phase_cell'].data  # not all data file contains U channel
                except KeyError:
                    pass
                
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

    def get_channel(self, datachannel: str) -> tuple[list, str, str,float]:
        """
        Get the channel of the EC4 DAQ file.

        Returns:
            tuple: [channel, quantity-name, unit name]


        - Time
        - E,U , E-IZ,E-IR
        - i, j
        - Z_E. Z_U

        """
        info=[None,"","",self.rawdata["Time"].properties.get("wf_increment", 1)]
        match datachannel:
            case "Time":
                info[0:3] = [self.Time, "t", "s"]
            # case "E":
            #    return self.E, "E", "V"
            case "U":
                info[0:3] = [ self.U, "U", "V"]
            case "i":
                info[0:3] = [ self.i, "i", "A"]
            case "j":
                info[0:3] = [ self.i/self._area, "j", f"A/{self._area_unit}"]
            case "Z_E1":
                info[0:3] = [ self.Z_E, "Z_E", "Ohm"]
            case "Z_U":
                info[0:3] = [ self.Z_U, "Z_U", "Ohm"]
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
                    unit = self.rawdata[datachannel].properties.get("unit_string", "")
                    quantity = self.rawdata[datachannel].properties.get("Quantity", "")
                    dT = self.rawdata[datachannel].properties.get("wf_increment", 1)
                    info = [ self.rawdata[datachannel].data, str(quantity) , str(unit), dT]
                except KeyError:
                    raise NameError("Error:" + datachannel + " channel name is not supported")
        return tuple(info)
                # return np.array([2]), "No channel", "No channel"

    def cosVal(self, phase: float):
        cosValue = phase/phase
        max_index = len(phase)
        for i in range(max_index):
            cosValue[i] = math.cos(self.Phase_E[i])
        return cosValue          

    def index_at_time(self, time_s_: float):
        return index_at_time(self.Time, time_s_)
    
    ##################################################################################
    def _norm(self, current:list, quantityUnit:QV, norm_to:str|tuple=None):
        
        norm_factor = self.get_norm_factors(norm_to)
        i_shifted = None
        qv = QV(0,"","")
        if norm_factor is not None:
            i_shifted = current.copy()
            if isinstance(current, list):
                i_shifted = current.copy()
                for i in range(len(current)):
                    # print("aaaa-shifting",i)
                    
                    i_shifted[i] = current[i] / float(norm_factor)
            else:
                i_shifted = current / float(norm_factor)
        #norm_factor_inv = norm_factor ** -1
            #qv = QV(1, i_unit, i_label) / norm_factor
            qv = quantityUnit/ norm_factor
            #self.i_unit = qv.unit
            #self.i_label = qv.quantity
            # print("aaaa-shifting",self.i_unit)
            return i_shifted, qv
        else:
            return current,quantityUnit
    


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

        range = {
            'limit_min': -1,
            'limit_max': -1
        }
        range.update(kwargs)

        options = plot_options(kwargs)
        options.legend = self.legend(*args, **kwargs)

        index_min = 0
        if range["limit_min"] > 0:
            index_min = self.index_at_time(range["limit_min"])
        index_max = len(self.Time)-1
        if range["limit_max"] >0:
            index_max = self.index_at_time(range["limit_max"])

        try:
            x_data, options.x_label, options.x_unit,x_dT = self.get_channel(x_channel)
            if(options.y_unit == "A"):
                loc_args = args
                x_data,qv = self._norm(x_data,QV(1,options.x_unit,options.x_label),*loc_args)
                options.x_label = qv.quantity
                options.x_unit = qv.unit
                
            options.x_data = x_data[index_min:index_max]
        except NameError:
            print(f"xchannel {x_channel} not supported")
        try:
            y_data, options.y_label, options.y_unit,y_dT = self.get_channel(y_channel)
            if(options.y_unit == "A"):
                loc_args = args
                y_data,qv = self._norm(y_data,QV(1,options.y_unit,options.y_label),*loc_args)
                options.y_label = qv.quantity
                options.y_unit = qv.unit
            options.y_data = y_data[index_min:index_max]
        except NameError:
            print(f"ychannel {y_channel} not supported")

        return options.exe()

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
        y,quantity,unit = self.get_channel(y_channel)
        array_Q = integrate.cumulative_simpson(y[idxmin:idxmax], x=self.Time[idxmin:idxmax], initial=0)
        Charge = QV(array_Q[len(array_Q)-1]-array_Q[0],unit,quantity)*QV(1,"s","t")
        return Charge 
    
    def IR_comp_value(self, y_channel: str = "i", comp_value = None ,**kwargs):
        """_summary_

        Args:
            y_channel (str, optional): _description_. Defaults to "i".
            comp_value (float, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        y, quantity, unit = self.get_channel(y_channel)
        if comp_value is None:
            comp_value = kwargs.get('comp_resistor',None)
            if comp_value is None:
                return y*comp_value
        
        
               


def index_at_time(Time, time_s_:float):
    max_index = len(Time)
    index = -1
    if time_s_ < 0:
        index = len(Time)-1
    else: 
        for i in range(max_index):
            if time_s_ <= Time[i]:
                index = i
                break
    if index < 0 : 
        index = len(Time)-1
    return index
