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
from .util import Quantity_Value_Unit as Q


class EC_Data(EC_Setup):
    """ Reads and stores data from a TDMS file in the format of EC4 DAQ.

    """
    def __init__(self, path=""):

        super().__init__()
        # self._area=1
        # self._area_unit="cm^2"
        # self.rotation =0
        # self.rotation_unit ="/min"
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
                # print(tdms_file.properties)
                self.rawdata = tdms_file['EC']
                self.Time = tdms_file['EC']['Time'].data
                self.i = tdms_file['EC']['i'].data
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
                try:
                    Items = tdms_file['Setup']['Item']
                    Value = tdms_file['Setup']['Value']
                    for x in range(len(Items)):
                        self.setup[Items[x]] = Value[x]
                    self.setup_reset()
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

    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return f"{self.setup_data.name}"

    def get_channel(self, datachannel: str) -> tuple[list, str, str]:
        """
        Get the channel of the EC4 DAQ file.

        Returns:
            tuple: [channel, quantity-name, unit name]


        - Time
        - E,U , E-IZ,E-IR
        - i, j
        - Z_E. Z_U

        """
        match datachannel:
            case "Time":
                return self.Time, "t", "s"
            # case "E":
            #    return self.E, "E", "V"
            case "U":
                return self.U, "U", "V"
            case "i":
                return self.i, "i", "A"
            case "j":
                return self.i/self._area, "j", f"A/{self._area_unit}"
            case "Z_E":
                return self.Z_E, "Z_E", "Ohm"
            case "Z_U":
                return self.Z_U, "Z_U", "Ohm"
            case "Phase_E":
                return self.Phase_E, "Phase_E", "rad"
            case "Phase_U":
                return self.Phase_U, "Phase_U", "rad"
            case "R_E":
                # cosValue=self.Phase_E/self.Phase_E
                # index=0
                # for i in self.Phase_E:
                #    cosValue[index] = math.cos(self.Phase_E[index])
                #    index=index+1
                return self.Z_E * self.cosVal(self.Phase_E), "R_WE", "Ohm"
            case "E-IZ":
                return self.E - self.i*self.Z_E, "E-IZ", "V"

            case "E-IR":
                return self.E - self.i*self.Z_E, "E-IR", "V"
            case _:
                # if datachannel in self.rawdata.channels():
                try:
                    unit = self.rawdata[datachannel].properties.get("unit_string", "")
                    quantity = self.rawdata[datachannel].properties.get("Quantity", "")
                    return self.rawdata[datachannel].data, str(quantity) , str(unit)
                except KeyError:
                    raise NameError("The channel name is not supported")
                # return np.array([2]), "No channel", "No channel"

    def cosVal(self, phase: float):
        cosValue = phase/phase
        max_index = len(phase)
        for i in range(max_index):
            cosValue[i] = math.cos(self.Phase_E[i])
        return cosValue          

    def index_at_time(self, time_s_: float):
        return index_at_time(self.Time, time_s_)


    def plot(self, x_channel: str, y_channel: str, **kwargs):
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
        index_min = 0
        if range["limit_min"] > 0:
            index_min = self.index_at_time(range["limit_min"])
        index_max = len(self.Time)-1
        if range["limit_max"] >0:
            index_max = self.index_at_time(range["limit_max"])

        try:
            x_data, options.x_label, options.x_unit = self.get_channel(x_channel)
            options.x_data = x_data[index_min:index_max]
        except NameError:
            print(f"xchannel {x_channel} not supported")
        try:
            y_data, options.y_label, options.y_unit = self.get_channel(y_channel)
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
        Charge = Q(array_Q[len(array_Q)-1]-array_Q[0],unit,quantity)*Q(1,"s","t")
        return Charge        


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
