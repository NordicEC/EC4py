

from pathlib import Path

import unittest   # The test framework



class test_cv_data( unittest.TestCase ):
    
    def Test_aa(self):
        
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
        self.assertEqual(paths[0].exists, True)
        
            
    
  

if __name__ == '__main__':
    unittest.main()
