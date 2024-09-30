import serial
import codecs
import numpy as np
from ec4py import Step_Data
from ec4py import CV_Data, CV_Datas
from ec4py import LSV_Data, LSV_Datas

from ECi_pot_serial_tech_step import tech_step
from ECi_pot_serial_tech import tempData
from ECi_pot_serial_tech_ramp import tech_ramp

def start_potentiostat(port: str):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = port
    ser.timeout=1
    ser.open()
    ser
    ser.is_open
    return ser


class ECipot():
    def __init__(self):
        self.cell = 0
        self.IE = 0
        self.ini = 0
        self.cmode = 0
        self.ser = None
        
    def connect(self, port: str):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.port = port
        self.ser.timeout=1
        self.ser.open()
        self.ser
        if self.ser.is_open:
            for x in range(20):
                line = self.ser.readline(100)
                if line == b'Ini start\r\n':
                    break
                    
            for x in range(20):
                line = self.read_wait()
                if line is not None:
                    self.info(line)
                if line == b'Ini Done\r\n':
                    break
                print(line)
        self.ini = 1
        self.ser.readline(100)
        self.ser.readline(100)
        return self.ser

    def close(self):
        self.ser.close()
    
    def info(self, sline:str):
        #sline = str(line, encoding='utf-8')
        if sline[0:4] == "CELL":
            #sline = str(line[4:6], encoding='utf-8')
            s =sline[4:6]
            self.cell = int(s)
            print("CELL " + s)
        elif sline[0:5] == "CMODE":
            #sline = str(line[5:7], encoding='utf-8')
            s =sline[5:7]
            self.cmode = int(s)
            print("CMODE " + s)
        elif sline[0:2] == "IE":
            #sline = str(line[2:5], encoding='utf-8')
            s =sline[2:5]
            self.IE = int(s)
            print("IE " + s)
    ##############################################################
    def cell_on(self):
        if self.ser.is_open:
            self.ser.write(b"CELL 1\n")
    def cell_off(self):
        if self.ser.is_open:
            self.ser.write(b"CELL 0\n")
    
    def reads(self):
        line = None
        for x in range(1000):
            tline = self.read()
            if tline is None:
                break
            else:
                line = tline
        return line
    
    def abort(self):
        self.ser.write(b"ABORT\n")
    
    def read(self):
        if self.ser.is_open:
            line = None
            sline = None
            if self.ser.in_waiting > 0:
                line = self.ser.readline()
                self.info(line)
                sline = str(line, encoding='utf-8').rstrip()
                return sline
            else:
                return None
        else:
            print("COM not open")
            return
        
    def read_wait(self):
        line = self.ser.readline()
        sline = str(line, encoding='utf-8').rstrip()
        return sline
    
    def write(self, line: str):
        line = line.rstrip()
        line = line + "\n"
        b_string = codecs.encode(line, 'utf-8')
        print(b_string)  
        self.ser.write(b_string)   
    ###############################################################
    def steps_raw(self,t0,v0,t1= None,v1 = None,t2= None,v2 = None): 
        if self.ser.is_open:
            string = f'step {t0} {v0}'
            if v1 is not None and t1 is not None:
                string = string + f' {t1} {v1}'
            if v2 is not None and t2 is not None:
                string = string + f' {t2} {v2}'  
            self.write(string)
              
            for x in range(500):
                line = self.read_wait()
                ##print(line)
                if line[0:4].casefold() == "Done".casefold():
                        print("\nDone")
                        break
                #elif line[0:4].casefold() == "Step".casefold():
                print(line)
                #print line
        
    def steps(self,t0,v0,t1= None,v1 = None,t2= None,v2 = None):
        if self.ser.is_open:
            string = f'step {t0} {v0}'
            if v1 is not None and t1 is not None:
                string = string + f' {t1} {v1}'
            if v2 is not None and t2 is not None:
                string = string + f' {t2} {v2}'

            self.reads()
            ini_data = line2data(self.read_wait())
            self.write(string)
            """
            for x in range(50):
                line = self.read_wait()
                print(line)
                if line[0:3] == "INI":
                    break
                elif line[0:5] == "Start":
                    break
            #########################    
            for x in range(50):
                line = self.read_wait()
                ##print(line)
                if line[0:4] == "Done":
                        print("\nDone")
                        break
                elif line[0:4] == "Step":
                        print(f"\n{line}: ",end ="")
                else:
                    tdata.append(line)
                    print("-",end ="")
            
            tdata = tech_step(self.read_wait)
            data = Step_Data()
            data.Time = tdata.Time() /1000. # time is given in ms
            data.Time = data.Time - data.Time[0]
            data.E = tdata.E()
            data.i = tdata.i()
            """
            data = tech_step(self.read_wait)
            ##ini 
            return data
        
    def ramp_test(self,start:float,v1:float,v2:float,rate_mV_s:float, nr):
        if self.ser.is_open:
            string = f'ramp {start} {v1} {v2} {rate_mV_s} {nr}\n' 
            self.write(string)
            for x in range(100):
                line = self.read_wait()
                print(line)
                if line[0:4].casefold() == "DONE".casefold():
                    break
        return
                           
    def ramp2(self,start_V:float,v1_V:float,v2_V:float,rate_V_s:float, nr_of_ramps):
        datas = LSV_Datas()
        if self.ser.is_open:
            string = f'ramp {start_V*1000:n} {v1_V*1000:n} {v2_V*1000:n} {rate_V_s*1000:n} {nr_of_ramps}\n' 
            self.write(string)
            datas= tech_ramp(self.read_wait, start_V,v1_V,v2_V,rate_V_s, nr_of_ramps)
        return datas
            
    
    def ramp(self,start:float,v1:float,v2:float,rate_mV_s:float, nr):
        if self.ser.is_open:
            string = f'ramp {start} {v1} {v2} {rate_mV_s} {nr}\n' 
            start = start/1000
            v1 = v1/1000
            rate_V_s = rate_mV_s /1000
            b_string = codecs.encode(string, 'utf-8')
            print(b_string)
            self.ser.write(b_string) 
            #pre init
            line = None
            for x in range(1000):
                line = None
                line = self.read_wait()
                if line[0:3] == "INI":
                    break
                
            ##ini 
            ini_data = np.empty([1000,3])
             
            print("INI: ", end ="")
         
            inidata = tempData()
            for x in range(1000):
                line = self.read_wait()
                if line[0:5] == "Start":
                    break
                else:
                    inidata.append(line)
                    print("x", end ="")
              
            print(" indexData",inidata.index)
            ##start
            ini_data = inidata.end()
            lastLine = inidata.lastLine
            print("start") 
            line = self.read()
            line = self.read()
            print(f"{line}0: ",end ="")
            line = self.read()
            #print(line)
            LSV  = []
            dirs = [""]
            datas = LSV_Datas()
            newDir = ""
            v_range = [start]
            for lsv_nr in range(nr+2):
                tdata = tempData()
                newlsv = LSV_Data()
                newlsv.setup_data._setup['Start'] = str(f"{start} V")
                newlsv.setup_data._setup['V1'] = str(f"{v1} V")
                newlsv.dir = dirs[lsv_nr]
                tdata.append(lastLine)
                for x in range(2000):  
                    line = None
                    line = self.read_wait()
                    if line[0:9].casefold() == "change to".casefold():
                        print(f"\n{line}: ",end ="")
                        dirs.append(line[10:13])
                        
                        break
                    elif line[0:4].casefold() == "Done".casefold():
                        print("\nDone")
                        break
                    else:
                        tdata.append(line)
                        print("-", end ="")
                LSV.append(tdata.end())
                
                #newlsv.E = tdata.E()
                #newlsv.i = tdata.i()
                if(lsv_nr%2 == 0):
                    V_start = v2
                    if lsv_nr == 0:
                        V_start = start
                    V_end = v1
                else:
                    V_start = v1
                    V_end = v2
                newlsv.convert(tdata.Time(),tdata.E(),tdata.i(), V_start,V_end, rate_V_s )
                datas.append(newlsv)
                lastLine = tdata.lastLine
                if line[0:4] == "Done":
                    break 
            print(dirs)         
            return LSV, ini_data, datas





           
    

def line2data(line):
    if line[0:1] == "\t":
        data = line.split("\t")
        #print(data)
        return data