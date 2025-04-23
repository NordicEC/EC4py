
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
#"import inc_dec    # "The code to test
import numpy as np
from pathlib import Path

import pytest

# C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test\test_step_data.py


def test_set_area():
        setup = EC_Setup()
        with pytest.raises(Exception) as context:
             setup.area = 5.0
        #self.assertTrue('This is broken' in context.exception)
        #self.assertRaises(ValueError, setup.area = 5, "3.0 m^2")
        setup.set_area(5.0)
        assert setup.area.value == 5
        setup2= EC_Setup()
        setup2.set_area("3.0 m")
        assert setup2.area.value == 3
        assert(setup2.area.unit == "m")
        assert(setup2.area.quantity == "A")

if __name__ == '__main__':
    pytest 
