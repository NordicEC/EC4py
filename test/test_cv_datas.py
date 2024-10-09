

from ec4py import cv_datas
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path


class Test_CV_Datas(unittest.TestCase):
    
    def load_files(self):
        
        E =np.array([1,2,3])
        paths = []
        path_to_dataSetFolder = Path(".").cwd().parent.parent / "test_data" /"CV"
        print(path_to_dataSetFolder)
        #paths.append( path_to_dataSetFolder / "CV_144913_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_153559_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_153541_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_153333_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_151300_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_151725_ 3.tdms")
        paths.append( path_to_dataSetFolder / "CV_151512_ 3.tdms")
        for path in paths:
            Path(".").exists
            self.assertEqual(path.exists, True)
        self.assertEqual(True, True)
        
        
        
    
       
        
        
    
  

if __name__ == '__main__':
    unittest.main()
