
from ec4py.util_graph import plot_options,should_plot_be_made
from ec4py.util_graph import NO_PLOT

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

class test_util_graph( unittest.TestCase ):
    
    def test_y_smooth(self):
        #kwarg={"y_smooth":"3"}
        #opt = plot_options(kwarg)
        #print(gdata_u)
        #print("HEJ")
        # opt.smooth_y(gdata_u)
        self.assertTrue(True)
        
    def test_should_plot_be_made(self):
        self.assertTrue(should_plot_be_made())
        self.assertTrue(should_plot_be_made(5,"avd","53"))
        self.assertFalse(should_plot_be_made(NO_PLOT))
        self.assertFalse(should_plot_be_made(5,"fdfd",NO_PLOT))
       
        
    
    
    
  

if __name__ == '__main__':
    unittest.main()
