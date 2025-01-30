import re



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
            'E' : "E",
            'i' : "i",
            'Z' : "Z_E",
            'Phase' : "Phase_E"
            }
        self.update(*args, **kwargs)
        return
    
    def __str__(self):
        return str(self._channels)
    
    def update(self,*args, **kwargs):
        a = str()
        for arg in args:
            if(isinstance(arg, str) ):
                numMatch=re.search("[0-9]+", arg)
                if arg[0]=='i' and numMatch!= None:
                    # to get the different channels of the MWE.
                    self._channels["i"]=arg
                    self._channels["Z"]="Z"+numMatch.group()
                    self._channels["Phase"]="Phase"+numMatch.group()
                if arg[0]=='P' and numMatch!= None:
                    self._channels["E"]=arg+"_E"
                    self._channels["i"]=arg+"_i"
                    self._channels["Z"]=arg+"_Z"
                    self._channels["Phase"]=arg+"_Phase"       
                if arg.casefold()=='cell'.casefold():
                    self._channels["E"]="Ucell"
                    self._channels["i"]="i"
                    self._channels["Z"]="Z_cell"
                    self._channels["Phase"]="Phase_cell"      
        self._channels.update(kwargs)                
        return
    
    @property
    def Voltage(self):
        return self._channels["E"]
    
    @property
    def Current(self):
        return self._channels["i"]
    
    @property
    def Impedance(self):
        return self._channels["Z"]
    @property
    def Phase(self):
        return self._channels["Phase"]
