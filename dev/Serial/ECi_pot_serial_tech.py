import numpy as np
from enum import Enum
 

class loopCtrl(Enum):
    run = 0
    stop = 1
    

class CV_Tech(Enum):
    run = 0
    stop = 1
    

class tempData:
    def __init__(self):
        self.temp_data = np.empty([1000,3])
        self.index = 0
        self.lastLine = ""
        
    def append(self, line):
        if line[0:1] == "\t":
            self.lastLine = line
            data = line.split("\t")
            #print(data)
            self.temp_data[self.index,0] = float(data[1]) 
            self.temp_data[self.index,1] = float(data[2]) /1000.0
            self.temp_data[self.index,2] = float(data[3])
            self.index = self.index + 1
    
    def end(self):
        return np.resize(self.temp_data,(self.index,3)) 
    
    def Time(self):
        return self.temp_data[0:self.index,0]
    
    def E(self):
        return self.temp_data[0:self.index,1]
    
    def i(self):
        return self.temp_data[0:self.index,2]  
    