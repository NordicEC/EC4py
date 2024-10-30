
from ec4py.util_voltammetry import Voltammetry 
from pathlib import Path
import numpy as np
import math
import unittest   # The test framework


gdata_u = np.array([range(0,101)])/100
gdata_d = np.array([range(99,0,-1)])/100

gdata_ud = np.concatenate((gdata_u, gdata_d),axis=1)
gdata_du = np.concatenate((gdata_d, gdata_u),axis=1)

class test_util_voltammetry( unittest.TestCase ):
    
        
    def test_E_range(self):
        data= Voltammetry()
        self.assertEqual(data.E_axis["E_max"],2.5)
        self.assertEqual(data.E_axis["E_min"],-2.5)
        
        ma = 5
        mi = -5
        data= Voltammetry(E_min = mi, E_max = ma)
        self.assertEqual(data.E_axis["E_max"],ma)
        self.assertEqual(data.E_axis["E_min"],mi)
        
        self.assertEqual(max(data.E),ma)
        self.assertEqual(min(data.E),mi)
    
    def test_interpolate(self):
        data= Voltammetry(E_min=-2,E_max=2)
        size =51
        x = np.array(range(0,size))/size-0.1
        y= x**2
        aa = data.interpolate(x,y)
        error = 0
        err=[]
        for i in range(size):
            current = aa[data.get_index_of_E(x[i])]
            error = error + (current-y[i])**2
            err.append((current-y[i]))
        err =np.array(err)    
        rms = math.sqrt(error )/size
        
        self.assertTrue(rms < 0.001)  
            
    def test_intergrate(self):
        data= Voltammetry(E_min=-1,E_max=1)
        rr= 10
        x = np.array(range(0,rr))/10-0.2
        y= np.ones(rr)
        aa = data.interpolate(x,y)
        bb,pl = data._integrate(0,0.5,aa)
        self.assertAlmostEqual(bb.value,0.5)
        self.assertEqual(bb.unit,"C")
    
    
    
        
    def test_get_E_at_i(self):
        data = Voltammetry(E_min=-2,E_max=2)
        data_i = data.E*2
        i = data._get_E_at_i(data_i,0)
        self.assertAlmostEqual(i,0)
        i = data._get_E_at_i(data_i,1)
        self.assertAlmostEqual(i,0.5)
        data_i = data.E*2+1
        i = data._get_E_at_i(data_i,-1)
        self.assertAlmostEqual(i,-1)
        i = data._get_E_at_i(data_i,0.1)
        self.assertAlmostEqual(i,-0.45)

if __name__ == '__main__':
    unittest.main()
