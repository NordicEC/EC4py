
from ec4py.util_voltammetry import Voltammetry 
from ec4py import Quantity_Value_Unit 

from pathlib import Path
import numpy as np
import math
import unittest   # The test framework
from numpy.testing import assert_almost_equal

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
        
        
        test_data = np.ones(len(data.E))
        for i in range(data.get_index_of_E(0)):
            test_data[i]=0
        i = data._get_E_at_i(test_data,0.9,tolerance=0.01)
        i=math.ceil(i)
        self.assertAlmostEqual(i,0)
        i = data._get_E_at_i(test_data,0.0,tolerance=0.01)
        i=math.ceil(i)
        self.assertAlmostEqual(i,-1)

    
    def test_shift_array(self):
        data = Voltammetry(E_min=-2,E_max=2)
        test_data = np.zeros(len(data.E))
        test_data[data.get_index_of_E(0)]=1
        test_list_data = list(test_data)
        #shift None
        shift_data = data._shift_Current_Array(test_data, None)
        test_shift_data = list(shift_data)
        self.assertListEqual(test_list_data,test_shift_data )
        #shift 0
        shift_data = data._shift_Current_Array(test_data, 0.0)
        test_shift_data = list(shift_data)
        self.assertListEqual(test_list_data,test_shift_data )
        
        #shift 0.5
        #test_data = np.zeros(len(data.E))
        index_of_test_i = np.argwhere(test_data > 0.5)[0][0]
        voltage_shift = -0.5
        shift_index_E = data.get_index_of_E(voltage_shift)-data.get_index_of_E(0)
        shift_data = data._shift_Current_Array(test_data, voltage_shift)
        index_of_shifted_i = np.argwhere(shift_data > 0.5)[0][0]
        shift_index_i =  index_of_test_i - index_of_shifted_i
        self.assertEqual(shift_index_E,shift_index_i )

    def test_norm(self):
        data = Voltammetry(E_min=-2,E_max=2)
        data.set_area(2)
        print(data.area)
        testdata = np.array([10])
        r = data.norm("AREA_CM",testdata)
        print(r)
        self.assertIsInstance(r,tuple)
        self.assertEqual((r[0])[0],[5/10000]) #should return the data-
        q=r[1]
        self.assertIsInstance(q,Quantity_Value_Unit)
        print(q)
        self.assertEqual(q.unit,"A cm^-2")
        
        data = Voltammetry(E_min=-2,E_max=2)

        data.set_area("5 m^2")
        print(data.area)
        r = data.norm("AREA",testdata)
        self.assertIsInstance(r,tuple)
        self.assertEqual((r[0])[0],[2]) #should return the data-
        q=r[1]
        self.assertIsInstance(q,Quantity_Value_Unit)
        print(q)
        print(data.get_norm_factor("AREA_CM"))
        print(data.get_norm_factor("AREA"))

        self.assertEqual(q.unit,"A m^-2")
        
 
    def test_set_active_RE(self):
        data = Voltammetry(E_min=-2,E_max=2)
        testdata=data.E.copy()
       
        #r = data.set_active_RE("RHE",testdata)
     
        data.set_RHE(0.0)
        r1 = data.set_active_RE("RHE",testdata)
        print(r1)
        #self.assertSequenceEqual(r1[1],data.E )
       
        data = Voltammetry(E_min=-2,E_max=2)
        data.set_RHE(1.0)
        r1 = data.set_active_RE("RHE",[testdata])
        print(r1)
        #self.assertEqual(r1,[data.E])
        self.assertIsInstance(r1,tuple)
        r1 = data.set_active_RE("RE",[testdata,testdata])
        print(r1)
        self.assertIsInstance(r1,tuple)
        r1 = data.set_active_RE("RHE",[testdata,testdata])
        self.assertIsNotNone(r1) #cannot shift twice.

        print(r1)

        #self.assertEqual(r1,[data.E, data.E])
        

if __name__ == '__main__':
    unittest.main()
