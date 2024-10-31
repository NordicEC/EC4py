
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path


# C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test\test_step_data.py
class test_EC_Setup(unittest.TestCase):

    def test_set_area(self):
        setup = EC_Setup()
        setup.area = 5.0
        self.assertEqual(setup.area.value, 5)
        setup2= EC_Setup()
        setup2.area = "3.0 m"
        self.assertEqual(setup2.area.value, 3)
        self.assertEqual(setup2.area.unit, "m")

    def test_set_rotation(self):
        setup = EC_Setup()
        setup.rotation = 5.0
        self.assertEqual(setup.rotation.value, 5)
        
        setup.rotation = "2.0 rpm"
        self.assertEqual(setup.rotation.value, 2)
        self.assertEqual(setup.rotation.unit, "rpm")
 
    def test_get_normfactor(self):
        setup = EC_Setup()
        setup.area = "9 km^2"
        nf = setup.get_norm_factor("area")
        self.assertEqual(nf.value, 9.0)
        self.assertEqual(nf.unit, "km^2")
        
        setup.rotation = "8.2 rpm"
        nf = setup.get_norm_factor("rotation")
        self.assertEqual(nf.value, 8.2)
        self.assertEqual(nf.unit, "rpm")
        ## Area
        setup.area = "7 m^2"
        nf = setup.get_norm_factor("area")
        self.assertAlmostEqual(nf.value, 7.0)
        self.assertEqual(nf.unit, "m^2")
        nf = setup.get_norm_factor("area_cm")
        self.assertAlmostEqual(nf.value, 70000)
        self.assertEqual(nf.unit, "cm^2")
        ## rotation
        setup.rotation = "16.0 f^2"
        nf = setup.get_norm_factor("rotation")
        self.assertAlmostEqual(nf.value, 16)
        self.assertEqual(nf.unit, "f^2")
        ## sqrt rotation
        nf = setup.get_norm_factor("sqrt_rot")
        self.assertEqual(nf.value, 4)
        self.assertEqual(nf.unit, "f")
     
        
    
  

if __name__ == '__main__':
    unittest.main()
