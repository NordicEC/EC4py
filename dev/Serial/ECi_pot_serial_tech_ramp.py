import numpy as np
from enum import Enum


from ECi_pot_serial_tech import tempData
from ec4py import LSV_Data, LSV_Datas
    
def tech_ramp(comFx,  start,v1,v2,rate_V_s,nr_of_ramps):
    #tech_ramp_aquire_ini(comFx)
    lsv_data = tech_ramp_aquire(comFx,  start,v1,v2,rate_V_s,nr_of_ramps)
    return lsv_data
    
    
###############################################################
def tech_ramp_aquire(comFx,  start,v1,v2,rate_V_s,nr_of_ramps):
    nextRamp = tech_ramp_aquire_ini(comFx)
    #print("\n------------nextRamp: ",nextRamp)
    datas = LSV_Datas()
    
    for lsv_nr in range(nr_of_ramps+2):
        newlsv = LSV_Data()
        newlsv.setup_data._setup['Start'] = str(f"{start} V")
        newlsv.setup_data._setup['V1'] = str(f"{v1} V")
        tdata,nextRamp = tech_ramp_aquire_single_ramp(comFx)
        
        if(lsv_nr%2 == 0):
            V_start = v2
            if lsv_nr == 0:
                V_start = start
            V_end = v1
        else:
            V_start = v1
            V_end = v2
        if len(tdata.Time()) > 0:   
            print("LEN",len(tdata.Time()), V_start,V_end,rate_V_s )
            newlsv.convert(tdata.Time(),tdata.E(),tdata.i(), V_start,V_end, rate_V_s )
            datas.append(newlsv)
        #lastLine = tdata.lastLine
        if nextRamp[0:4].casefold() == "Done".casefold():
            break
        if nextRamp is None:
            break
        if len(nextRamp) == 0:
            break
        
        print("AAA",lsv_nr,nextRamp)
    return datas 

########################################################
def tech_ramp_aquire_ini(comFx):
          
    print("INI: ", end ="") 
    inidata = tempData()
    for x in range(1000):
        line = comFx()
        if line[0:5].casefold() == "Start".casefold():
            break
        else:
            inidata.append(line)
            print("x", end ="")
    print(" indexData",inidata.index)
    print("START") 
    for x in range(4):
        line = comFx()
        nextRamp = change_to(line)
        if len(nextRamp) > 0:
            break
        if line[0] == "\t":
            break
    #nextRamp = comFx()
    #print(f"{nextRamp}0: ",end ="")
    #line = comFx()
    return nextRamp

def tech_ramp_aquire_single_ramp(comFx):
    tdata = tempData()
    nextRamp = ""
    for x in range(2000):  
        line = comFx()
        if line[0:4].casefold() == "Ramp".casefold():
            break
        if line[0:9].casefold() == "change to".casefold():
            print(f"\n{line}: ",end ="")
            nextRamp = line[10:13]
            break
        elif line[0:4].casefold() == "Done".casefold():
            print("\nDone")
            break
        else:
            tdata.append(line)
            print("-", end ="")
    return tdata,nextRamp

def change_to(line):
    if line[0:9].casefold() == "change to".casefold():
        print(f"\n{line}: ",end ="")
        return line[10:13]
    else:
        return ""