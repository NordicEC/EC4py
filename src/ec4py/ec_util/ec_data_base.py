import numpy as np
#import matplotlib.pyplot as plt

#from .ec_data_util import EC_Channels

from ..ec_setup import EC_Setup


class EC_Data_Base(EC_Setup):
    def __init__(self, path=""):
        super().__init__()
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
        self._channelNames = []
        self._units = []
        self._quantities = []
        self._dt=[]
        """All setup information given in the file.
        """

    @property 
    def channels(self):
        return self._channelNames
    
    def __repr__(self):
        """Get the name of the data file.
        """
        return f"EC_Data('{self.setup_data.fileName}')"
    
    

    def get_channel(self, datachannel: str) -> tuple[list, str, str,float]:
        """return data, quantity, unit, dT"""
        info=[None,"","",1]
        match datachannel:
            case "Time":
                info[0:3] = [self.Time, "t", "s"]
            case "E":
                info[0:3] = [self.E, "E", "V"]
            case "U":
                info[0:3] = [ self.U, "U", "V"]
            case "i":
                info[0:3] = [ self.i, "i", "A"]
            case "Z_E":
                info[0:3] = [ self.Z_E, "Z_E", "Ohm"]
            case "Z_U":
                info[0:3] = [ self.Z_U, "Z_U", "Ohm"]
            case "Phase_E":
                info[0:3] = [ self.Phase_E, "Phase_E", "rad"]
            case "Phase_U":
                info[0:3] = [ self.Phase_U, "Phase_U", "rad"]
            case "_":
                print("AAA")
        return  tuple(info)




def index_at_time(Time, time_s_:float):
    """Find the index of a specific time

    Args:
        Time (array like): Time array
        time_s_ (float): Time as a float

    Returns:
        int: index
    """

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
