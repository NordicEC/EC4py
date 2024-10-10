

from ec4py import CV_Datas
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path

E =np.array([1,2,3])
paths = []
path_to_dataSetFolder = Path(".").cwd() / "test_data" /"CV"
print(path_to_dataSetFolder)
#C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test_data\CV\CV_144700_ 3.tdms
#paths.append( path_to_dataSetFolder / "CV_144913_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_144700_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_153541_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_153333_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151300_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151725_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151512_ 3.tdms")
        

class Test_CV_Datas(unittest.TestCase):
    
    def test_files_exists(self):
        for path in paths:
            self.assertTrue(path.exists)
            
    def test_files_load(self):
        datas = CV_Datas(paths)
        
            
        
    def test_plot(self):
        datas = CV_Datas(paths)
        a = datas.plot()
        
        
    
       
        
        
    
  

if __name__ == '__main__':
    unittest.main()
