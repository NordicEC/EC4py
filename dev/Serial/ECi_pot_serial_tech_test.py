import serial
#from ECi_pot_serial import ECipot
#pot = ECipot()
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
        sp = next((x for x in self.sp_index if x >= self.index and x < self.index+1) ,None)
        if sp is not None:
            #print(len(self.sp_index))
            del self.sp_index[0]
            t = self.sp_text[0]
            del self.sp_text[0]
            self.index = self.index - 1
            return t
        if(self.index >= self.index_max):
            return "Done"
        else:
            return f"\t{self.tdata[self.index]*1000}\t{self.Edata[self.index]}\t{self.idata[self.index]}"
     
    def show(self):
        for x in range(self.index_max+10):
            line = self.comFX()
            print(line)
            if self.index >=self.index_max:
                break 
    def plot(self):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Horizontally stacked subplots')
        ax1.plot(self.tdata, self.Edata)
        ax2.plot(self.tdata, self.idata)

        
    def make_steps(self,v0=1,v1=None,v2=None, **kwargs ):
        steps_kwargs = {
            't0' : 0.1,
            'v0'  : v0,
            't1'   : 1,
            'v1' : v1,
            't2' : 1,
            'v2' : v2,
            'sweeps': 1
        }
        steps_kwargs.update(kwargs)
        self.index=0
        start_index = 5
        sindex=[start_index,-1,-1,-1,-1,-1]
        self.sp_index = [start_index]
        self.sp_text = ["Start"]
        print(v1,v2)
        stepINDEX=0
        v0 = float(steps_kwargs["v0"])
        vEnd =v0
        if v1 is not None:
            i= sindex[stepINDEX]+ 50
            stepINDEX=stepINDEX+1
            sindex[stepINDEX] = i
            v1 = float(steps_kwargs["v1"])
            self.sp_index.append(i)
            self.sp_text.append("STEP")
            vEnd = v1
        
        if v2 is not None:
            i= sindex[stepINDEX]+ 50
            stepINDEX=stepINDEX+1
            sindex[stepINDEX] = i
            v2 = float(steps_kwargs["v2"])
            self.sp_index.append(i)
            self.sp_text.append("STEP")
            vEnd =v2
        ###ENDINGS
        i= sindex[stepINDEX]+ 50
        stepINDEX=stepINDEX+1
        sindex[stepINDEX]=i
        self.sp_index.append(i)
        self.sp_text.append("Done")
        #self.sp_index = [start_index,50,100,150]
        #self.sp_text = ["Start", "STEP ","STEP ","STEP "]
        
        #v1 = float(steps_kwargs["v1"])
        #v2 = float(steps_kwargs["v2"])
        print(sindex)

        for index in range(self.index_max):
            if index <start_index: 
                self.Edata[index] = v0+ -1 
            elif index >=sindex[0] and index <sindex[1]:
                self.Edata[index] = v0
            elif index >=sindex[1] and index <sindex[2]:
                self.Edata[index] = v1
            elif index >=sindex[2] and index <sindex[3]:
                self.Edata[index] = v2
            else:
                self.Edata[index] = vEnd
            
                
        
 ###################################################################################       
    def make_ramp(self, ini_nr =5,in_ramp =False, v1=1, **kwargs ):
        ramp_kwargs = {
            'v0' : 0.0,
            'v1'  : v1,
            'v2'   : 0.0,
            'rate' : 1.0,
            'sweeps': 1
        }
        v0=0
        ramp_kwargs.update(kwargs)
        self.index=0
        self.sp_index = []
        self.sp_text = []
        if(ini_nr>0):
            self.sp_index.append(ini_nr)
            self.sp_text.append("INI")
            start_index = ini_nr+51
        else:
            start_index=1
        if not in_ramp:
            self.sp_index.append(start_index)
            self.sp_text.append("Start")
            self.sp_index.append(start_index)
            if v1>v0:
                self.sp_text.append("Change to Pos ")
            else:
                self.sp_text.append("Change to Neg ")
        done_at =self.index_max-5
        v0 = float(ramp_kwargs["v0"])
        v1 = float(ramp_kwargs["v1"])
        v2 = float(ramp_kwargs["v2"])
        nr =ramp_kwargs["sweeps"]
        dir = v2>v1
        sweep_di = 1
        sindex = [start_index,-1,-1,-1,-1,-1,-1,-1]
        if nr>1:
            sweep_di = (done_at - start_index)/nr
            for x in range(1,nr+1):
                n_index = start_index+sweep_di*x
                sindex[x] =n_index
                self.sp_index.append(n_index)
                if dir:
                    self.sp_text.append("Change to Pos ")
                else:
                    self.sp_text.append("Change to Neg ")
                dir = not dir
            
        self.sp_index.append(done_at)
        self.sp_text.append("Done")
        
        self.Edata = self.tdata * 2+0.01
        
        vEnd = v1
        if nr % 2 == 0:
            vEnd = v2
        #print(sindex)
        for index in range(self.index_max):
            if index <start_index: 
                self.Edata[index] = v0 
            elif index >=sindex[0] and index <sindex[1]:
                 self.Edata[index] = (index-sindex[0]) /(sweep_di)*v1 + v0
            elif index >=sindex[1] and index <sindex[2]:
                 self.Edata[index] = (index-sindex[1]) /(sweep_di)*(v2-v1) + v1 
            elif index >=sindex[2] and index <sindex[3]:
                 self.Edata[index] = (index-sindex[2]) /(sweep_di)*(v1-v2) + v2
            elif index >=sindex[3] and index <sindex[4]:
                 self.Edata[index] = (index-sindex[3]) /(sweep_di)*(v2-v1) + v1 
            elif index >=sindex[4] and index <sindex[5]:
                 self.Edata[index] = (index-sindex[4]) /(sweep_di)*(v1-v2) + v2
            elif index >=sindex[5] and index <sindex[6]:
                 self.Edata[index] = (index-sindex[5]) /(sweep_di)*(v2-v1) + v1 
            elif index >=sindex[6] and index <sindex[7]:
                 self.Edata[index] = (index-sindex[6]) /(sweep_di)*(v1-v2) + v2


            elif index >done_at:
                self.Edata[index] = vEnd
            else:   #single sweep
               self.Edata[index] = (index-start_index) /(done_at-start_index)*vEnd 
