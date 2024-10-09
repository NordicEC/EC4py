

from ec4py.analysis_tafel import Tafel
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np

E =np.array([1,2,3])

class Test_Tafel(unittest.TestCase):
    
    def linear_slope(self):
        
        y_data = np.exp(E)
        unit = "AAA"
        result = Tafel(E, y_data, unit, "", "bo")
        self.assertEqual(result.value, 1.0)
        y_data = 2*y_data
        result =  Tafel(E, y_data, unit, "", "bo")
        self.assertEqual(result.value, 2.0)
       
        
    def test_units_slope(self):
        y_data = np.exp(E)

        unit = "AAA"
        result = Tafel(E, y_data, unit, "", "bo")
        self.assertEqual(result.unit, "V^-1")
        # self.assertEqual(result.unit, "m")
    
    def test_quantity_slope(self):
        rot =np.array([30,40,50])
        y_data = [10,20,30]
        
        
    
  

if __name__ == '__main__':
    unittest.main()
