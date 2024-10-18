
from ec4py.analysis_tafel import Tafel
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np

E =np.array([1,2,3,4])

def  rn(value):
    return round(value*1000000)/1000000
class test_Tafel(unittest.TestCase):
    
    def test_linear_slope(self):
        y_data = np.power(10,E)
        unit = "AAA"
        result = Tafel(E, y_data, unit, "", "b")
        self.assertEqual(rn(result.value), 1.0)
        y_data = np.power(10,E/5)
        result2 =  Tafel(E, y_data, unit, "", "b")
        self.assertEqual(rn(result2.value), 5.0)
       
        
    def test_units_slope(self):
        y_data = np.exp(E)

        unit = "AAA"
        result = Tafel(E, y_data, unit, "", "b")
        self.assertEqual(result.unit, "V/dec")
        # self.assertEqual(result.unit, "m")
    
    def test_quantity_slope(self):
        rot =np.array([30,40,50])
        y_data = [10,20,30]
        
        
    
  

if __name__ == '__main__':
    unittest.main()
