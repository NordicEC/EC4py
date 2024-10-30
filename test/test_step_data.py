
import copy
from ec4py import Step_Data
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path

E =np.array([1,2,3])
paths = []
path_to_dataSetFolder = Path(".").cwd() / "test_data" /"Step"
print(path_to_dataSetFolder)
#paths.append( path_to_dataSetFolder / "CV_144913_ 3.tdms")
paths.append( path_to_dataSetFolder / "Steps_102346.tdms")
paths.append( path_to_dataSetFolder / "CV_153541_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_153333_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151300_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151725_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_151512_ 3.tdms")

gsize = 110
gdata = Step_Data()
gdata.Time=np.array(range(0,gsize),dtype=np.float64)/20
gdata.E=np.ones(gsize,dtype=np.float64)
gdata.i=np.ones(gsize,dtype=np.float64)*2

# C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test\test_step_data.py
class test_Step_Datas(unittest.TestCase):

    def test_load_file(self):
        
        print(paths[0].exists)
        self.assertTrue(paths[0].exists)
    
    def test_index_at_time(self):
        
        index = gdata.index_at_time(2.0)
        self.assertEqual(gdata.Time[index],2.0)
        index = gdata.index_at_time(100)
        self.assertEqual(index,gsize-1)
        
        
    def test_integrate(self):
        data = copy.deepcopy(gdata)
        v = data.integrate(2.0,4.0)
        self.assertAlmostEqual(v.value,4.0)
        self.assertEqual(v.unit,"C")
        data.area = "10 m^2"
        data.norm("area")
        v = data.integrate(2.0,4.0)
        self.assertAlmostEqual(v.value,0.40)
        self.assertEqual(v.unit,"C m^-2")

        
                
    
       
        
        
    
  

if __name__ == '__main__':
    unittest.main()
