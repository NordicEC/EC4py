import serial
from ECi import ECipot
pot = ECipot()
from ec4py import EC_Data
import matplotlib.pyplot as plt
from ec4py import LSV_Data,LSV_Datas
from ECi_pot_serial_tech_ramp import tech_ramp_aquire, tech_ramp
import math
import numpy as np



class testFX:
    def __init__(self, datas = 200):
        self.index_max = datas
        self.tdata = np.array([i/100 for i in range(self.index_max)])
        self.Edata = self.tdata * 2+0.01
        self.idata = np.array([math.log(x) for x in self.Edata])
        self.index = 0
        self.sp_text =[]
        self.sp_index = []
        
        return
    
    def comFX(self):
        self.index = self.index + 1
        sp = next((x for x in self.sp_index if x == self.index) ,None)
        if sp is not None:
            print(len(self.sp_index))
            del self.sp_index[0]
            t = self.sp_text[0]
            del self.sp_text[0]
            self.index = self.index - 1
            return t
        if(self.index == self.index_max):
            return "Done"
        else:
            return f"\t{self.tdata[self.index]}\t{self.Edata[self.index]}\t{self.idata[self.index]}"
        
    def make_steps(self):
        self.sp_index = [5,50,100]
        self.sp_text = ["Start", "STEP ","STEP "]
        
    def make_ramp(self, ini_nr =5,in_ramp =False, v1=1):
        self.sp_index = []
        self.sp_text = []
        if(ini_nr>0):
            self.sp_index.append(ini_nr)
            self.sp_text.append("INI")
            start_index = ini_nr+51
        else:
            start_index=1
        if not in_ramp:
            self.sp_index.append(start_index-1)
            self.sp_text.append("Start")
            self.sp_index.append(start_index)
            self.sp_text.append("Change to Pos ")
        done_at =self.index_max-5
        self.sp_index.append(done_at)
        self.sp_text.append("Done")
        
            
        self.Edata = self.tdata * 2+0.01
        
       
        for index in range(self.index_max):
            if index <start_index: 
                self.Edata[index] = 0 
            elif index >done_at:
                self.Edata[index] = 1*v1
            else:
               self.Edata[index] = (index-start_index) /(done_at-start_index)*v1 
