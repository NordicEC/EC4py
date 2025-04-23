
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path

import pytest

# C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test\test_step_data.py




class test_EC_Setup(unittest.TestCase):

    def test_set_area(self):
        setup = EC_Setup()
        with self.assertRaises(Exception) as context:
             setup.area = 5.0
        #self.assertTrue('This is broken' in context.exception)
        #self.assertRaises(ValueError, setup.area = 5, "3.0 m^2")
        setup.set_area(5.0)
        self.assertEqual(setup.area.value, 5)
        setup2= EC_Setup()
        setup2.set_area("3.0 m")
        self.assertEqual(setup2.area.value, 3)
        self.assertEqual(setup2.area.unit, "m")
        self.assertEqual(setup2.area.quantity, "A")

    def test_set_rotation(self):
        setup = EC_Setup()
        setup.rotation = 5.0
        self.assertEqual(setup.rotation.value, 5)
        
        setup.rotation = "2.0 rpm"
        self.assertEqual(setup.rotation.value, 2)
        self.assertEqual(setup.rotation.unit, "rpm")
 
    def test_get_normfactor(self):
        setup = EC_Setup()
        setup.set_area("9 km^2")
        nf = setup.get_norm_factor("area")
        self.assertEqual(nf.value, 9.0)
        self.assertEqual(nf.unit, "km^2")
        
        setup.rotation = "8.2 rpm"
        nf = setup.get_norm_factor("rotation")
        self.assertEqual(nf.value, 8.2)
        self.assertEqual(nf.unit, "rpm")
        ## Area
        setup.set_area("7 m^2")
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
    
    def test_set_weight(self):
        setup = EC_Setup()
        self.assertEqual(setup.weight, None)
        setup.set_weight(5.0)
        self.assertEqual(setup.weight.value, 5)
        self.assertEqual(setup.weight.quantity, "m")
        setup2= EC_Setup()
        setup2.set_mass("3.0 g")
        self.assertEqual(setup2.mass.value, 3)
        self.assertEqual(setup2.mass.unit, "g")
        self.assertEqual(setup.mass.quantity, "m")
        setup3= EC_Setup()
        setup3.set_area("3.0 m^2")
        setup3.set_mass("15.0 kg")
        self.assertEqual(setup3.mass.value, 15)
        self.assertEqual(setup3.mass.unit, "kg")
        self.assertEqual(setup3.loading.value, 5)
        self.assertEqual(setup3.loading.unit, "kg m^-2")
        
    def test_set_loading(self):
        setup = EC_Setup()
        self.assertEqual(setup.loading, None)
        setup.set_loading(5.0)
        self.assertEqual(setup.loading.value, 5)
        self.assertEqual(setup.loading.quantity, "L")
        setup2= EC_Setup()
        setup2.set_loading("3.0 g cm^-2")
        self.assertEqual(setup2.loading.value, 3)
        self.assertEqual(setup2.loading.unit, "g cm^-2")	
        setup3= EC_Setup()
        setup3.set_area("3.0 m^2")
        setup3.set_loading("15.0 kg /m^2")
        self.assertEqual(setup3.loading.value, 15)
        self.assertEqual(setup3.loading.unit, "kg m^-2")
        self.assertEqual(setup3.mass.value, 15*3)
        self.assertEqual(setup3.mass.unit, "kg")
        
               
        
    
     
    def test_get_legend(self): 
        setup = EC_Setup()
        setup.setup_data._setup["Date"] = "dateDATE"
        setup.setup_data._setup["rate"] = "rate"
        setup.setup_data.name = "nameNAME"
        self.assertEqual( setup.legend(LEGEND.NAME), "nameNAME")
        self.assertEqual( setup.legend(LEGEND.DATE), "2020-01-01")
        self.assertEqual( setup.legend(LEGEND.TIME), "2020-01-01")

        self.assertEqual( setup.legend(LEGEND.RATE), "1.000 V s^-1")
        
        
  

if __name__ == '__main__':
    unittest.main()
