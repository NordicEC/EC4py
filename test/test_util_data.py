from ec4py import EC_Data
from ec4py.ec_data_util import EC_Channels

from ec4py import LSV_Data, CV_Data,RHE,POS,NEG,AVG

from ec4py.util_data import get_Impedance, get_IR,calc_ir_manual,calc_ir
from ec4py.util_data import IR_comp_R,IR_comp_Z,IR_comp_Rmed,IR_comp_Zmed

from pathlib import Path
import numpy as np

import unittest   # The test framework


#Test are exe from base dir.
paths = []
path_to_dataSetFolder = Path(".").cwd() / "test_data" /"CV"
print(path_to_dataSetFolder)
#paths.append( path_to_dataSetFolder / "CV_144913_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_144700_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_153541_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_153333_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151300_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151725_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151512_ 3.tdms")

gdata_u = np.array([range(0,101)])/100
gdata_d = np.array([range(99,0,-1)])/100

gdata_ud = np.concatenate((gdata_u, gdata_d),axis=1)
gdata_du = np.concatenate((gdata_d, gdata_u),axis=1)

class test_util_data( unittest.TestCase ):
    
    def test_get_Impedance(self):
        d = EC_Data()
        d.E = np.linspace(-0.5, 0.5, 10)
        d.i = np.linspace(-0.5, 0.5, 10)
        d.Z_E = np.linspace(-0.5, 0.5, 10)
        d.Phase_E = np.linspace(-0.5, 0.5, 10)
        ch = EC_Channels()
        imp, Phase = get_Impedance(d,ch)
        self.assertTrue(np.allclose(d.Z_E, imp,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(d.Phase_E, Phase,  atol=1e-10, rtol=1e-10))
        
    
        
    def test_calc_ir_manual(self):
        d = EC_Data()
        dataPoints =10
        d.E = np.linspace(-0.5, 0.5, dataPoints)
        d.i = np.ones(dataPoints)*0.5
        ch = EC_Channels()
        r=123
        res = calc_ir_manual(d,ch,r)
        self.assertTrue(res[0])
        #print(res[1])
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*0.5*r,  atol=1e-10, rtol=1e-10))
        
    def test_calc_ir_from_genData(self):
        i,imp,Ph = {0.5,8,np.pi/6*2}
        
        d = EC_Data()
        dataPoints =10
        d.E = np.linspace(-0.5, 0.5, dataPoints)
        d.i = np.ones(dataPoints)*i
        d.Z_E = np.ones(dataPoints)*imp
        d.Phase_E = np.ones(dataPoints)*Ph
        ch = EC_Channels()
        
        res = calc_ir(d,ch,"Zafd")
        self.assertFalse(res[0])

        #Absolute Impedance
        res = calc_ir(d,ch,IR_comp_Z)
        self.assertTrue(res[0])
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp,  atol=1e-10, rtol=1e-10))   
        #Absolute Impedance
        res = calc_ir(d,ch,IR_comp_Zmed)
        self.assertTrue(res[0])
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp,  atol=1e-10, rtol=1e-10))   
        #Reistance
        res = calc_ir(d,ch,IR_comp_R)
        self.assertTrue(res[0])
        #print(res[1])
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp*np.cos(Ph),  atol=1e-10, rtol=1e-10))
        #Reistance
        res = calc_ir(d,ch,IR_comp_Rmed)
        self.assertTrue(res[0])
        #print(res[1])
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp*np.cos(Ph),  atol=1e-10, rtol=1e-10))
        
        
    
    def test_get_imp_real(self):
        self.assertTrue(paths[2].exists())
        print()
        print(len(paths),paths[2])
        d = EC_Data(paths[2])
   
        ch = EC_Channels()
        imp, pha = get_Impedance(d,ch)
        ##Different sizes.
        #self.assertTrue(np.allclose(d.Z_E, imp,  atol=1e-10, rtol=1e-10))
        #self.assertTrue(np.allclose(d.Phase_E, pha,  atol=1e-5, rtol=1e-5))
      
        
    def test_calc_ir_manual_real(self):
        i,imp,Ph = {0.5,8,np.pi/6*2}
        self.assertTrue(paths[2].exists())
        print()
        print(len(paths),paths[2])
        data = EC_Data(paths[2])
        dataPoints = len(data.i)
       
        data.i = np.ones(len(data.i))*i
        data.Z_E = np.ones(len(data.Z_E))*imp
        data.Phase_E = np.ones(len(data.Phase_E))*Ph
        ch = EC_Channels()
        #IR_comp_Zmed
        res = calc_ir(data,ch,IR_comp_Zmed)
        self.assertTrue(res[0])
        self.assertTrue(len(res[1])==dataPoints)
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp,  atol=1e-10, rtol=1e-10))
        res = calc_ir(data,ch,IR_comp_Rmed)
        #IR_comp_Rmed
        self.assertTrue(res[0])
        self.assertTrue(len(res[1])==dataPoints)
        print(res[1])
        print(i*imp*np.cos(Ph))
        self.assertTrue(np.allclose(res[1], np.ones(dataPoints)*i*imp*np.cos(Ph),  atol=1e-10, rtol=1e-10))

        #self.assertGreater(data_E,0)  
        
    def test_get_IR(self):
        i,imp,Ph = {0.5,8,np.pi/6*2}
        data = EC_Data(paths[2])
        dataPoints = len(data.i)
        data.i = np.ones(len(data.i))*i
        data.Z_E = np.ones(len(data.Z_E))*imp
        data.Phase_E = np.ones(len(data.Phase_E))*Ph
        ch = EC_Channels()
        #IR_comp_Zmed
        res = get_IR(data,ch,IR_comp_Zmed)
        self.assertTrue(res[0])  
        res = get_IR(data,ch,IR_comp_Zmed)
        self.assertTrue(res[0])  
        res = get_IR(data,ch,IR_comp_Zmed)
        self.assertTrue(res[0])  
        res = get_IR(data,ch,IR_comp_Zmed)
        self.assertTrue(res[0])  
        res = get_IR(data,ch,5)
        self.assertTrue(res[0])   
        res = get_IR(data,ch,"5")
        self.assertTrue(res[0])   
        
        #res = get_IR(data,ch,"A")
        #self.assertFalse(res[0])       
        
    
  

if __name__ == '__main__':
    unittest.main()
