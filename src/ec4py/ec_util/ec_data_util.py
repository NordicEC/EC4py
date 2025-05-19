import re
from enum import StrEnum


class ENUM_Channel_Names(StrEnum):
    unknown ="_"
    Time = "Time"
    E = "E"
    i = "i"
    Z = "Z"
    Phase = "Phase"

ch = ENUM_Channel_Names

class EC_Channels:
    """
    property
    - Voltage:
    - Current
    - Impedance
 
    - Phase - returns the phase
    
    """
    def __init__(self,*args, **kwargs):
        self._channels = {
            ch.Time: "Time",
            ch.E : "E",
            ch.i : "i",
            ch.Z : "Z_E",
            ch.Phase : "Phase_E",
            'MWE_CH': None
            }
        self.update(*args, **kwargs)
        return
    
    def __str__(self):
        return str(self._channels)
    
    def update(self,*args, **kwargs):
        #a = str()
        for arg in args:
            if(isinstance(arg, str) ):
                numMatch=re.search("[0-9]+", arg)
                if arg[0]=='i' and numMatch is not None:
                    # to get the different channels of the MWE.
                    self._channels[ch.i]="i_"+numMatch.group()
                    self._channels[ch.Z]="Z_"+numMatch.group()
                    self._channels[ch.Phase]="Phase_"+numMatch.group()
                    self._channels["MWE_CH"]=int(numMatch.group())
                if arg[0]=='P' and numMatch is not None:
                    self._channels[ch.E]=arg+"_E"
                    self._channels[ch.i]=arg+"_i"
                    self._channels[ch.Z]=arg+"_Z"
                    self._channels[ch.Phase]=arg+"_Phase"       
                if arg.casefold()=='cell'.casefold():
                    self._channels[ch.E]="Ucell"
                    self._channels[ch.i]="i"
                    self._channels[ch.Z]="Z_cell"
                    self._channels[ch.Phase]="Phase_cell"      
        self._channels.update(kwargs)                
        return
    
    @property
    def Voltage(self):
        return str(self._channels[ch.E])
    
    @property
    def Current(self):
        return str(self._channels[ch.i])
    
    @property
    def Impedance(self):
        return str(self._channels[ch.Z])
    @property
    def Phase(self):
        return str(self._channels[ch.Phase])
    @property
    def MWE_CH(self):
        return self._channels["MWE_CH"]
    
    @property
    def Time(self):
        return str(self._channels[ch.Time])
