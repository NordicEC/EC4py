import numpy as np



from enum import Enum

from ECi_pot_serial_tech import tempData

from ec4py import Step_Data
from ec4py import CV_Data, CV_Datas
from ec4py import LSV_Data, LSV_Datas
    

class loopCtrl(Enum):
    run = 0
    stop = 1
    

class CV_Tech(Enum):
    run = 0
    stop = 1
    
def tech_step(comFx):
    
    tdata = tech_step_aquire(comFx)
    data = Step_Data()
    data.Time = tdata.Time() /1000. # time is given in ms
    data.Time = data.Time - data.Time[0]
    data.E = tdata.E()
    data.i = tdata.i()
    return data        
###############################################################
def tech_step_aquire(comFx):
    tdata = tempData()
    for x in range(50):
        line = comFx()
        print(line)
        if line[0:3].casefold() == "INI".casefold():
            break
        elif line[0:5].casefold() == "Start".casefold():
            break
    #########################    
    for x in range(500):
        line = comFx()
        ##print(line)
        if line[0:4].casefold() == "Done".casefold():
                print("\nDone")
                break
        elif line[0:4].casefold() == "Step".casefold():
                print(f"\n{line}: ",end ="")
        else:
            tdata.append(line)
            print("-",end ="")
    return tdata   
