

from ec4py.analysis_rate import sweep_rate_analysis
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import numpy as np

import unittest   # The test framework


rate =np.array([300,400,500])

def  rn(value):
    return round(value*1000000)/1000000

class Test_Analysis_SweepRate(unittest.TestCase):
    
    def test_linear_slope(self):
        
        y_data = 1*rate
        unit = "AAA"
        result = sweep_rate_analysis(rate, y_data, unit, "", "bo")
        self.assertEqual(rn(result.value), 1.0)
        y_data = 2*y_data
        result = sweep_rate_analysis(rate, y_data, unit, "", "bo")
        self.assertEqual(rn(result.value), 2.0)
        # self.assertEqual(result.unit, "m")

        
    def test_units_slope(self):
        rate = [QVU(x,"V /s") for x in range(0,10)]
        y_data = 1*rate
        unit = "X"
        result = sweep_rate_analysis(rate, y_data, "A", "", "bo")
        self.assertEqual(result.unit, "F")
        result = sweep_rate_analysis(rate, y_data, unit, "", "bo")
        self.assertEqual(result.unit, unit+" F A^-1")
        # self.assertEqual(result.unit, "m")
    
    def test_quantity_slope(self):
        rate = [QVU(x,"V /s","v") for x in range(0,10)]
        y_data = 1*rate
        result = sweep_rate_analysis(rate, y_data, "", "", "bo")
        self.assertEqual(result.quantity, "v^-1")
        q = "AAA"
        result = sweep_rate_analysis(rate, y_data, "", q, "bo")
        self.assertEqual(result.quantity, q+" v^-1")
        
    def real_data(self):
        pass
        
    
  

if __name__ == '__main__':
    unittest.main()
