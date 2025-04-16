import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
from ec4py.ec_datas_util import EC_Datas_base
from ec4py import AREA, AREA_CM, MASS

#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path
 #import pytest
import pytest

#@pytest.fixture
def  rn(value):
    return round(value*1000000)/1000000

@pytest.fixture
def  help_quantities_add(datasType_with_a_length):
    datas = datasType_with_a_length
    for data in datas:
        data.set_area("2 m^2" )
        data.set_area("1 m^2" )
        data.set_mass("3 g")
        data.set_mass("2 g")    


def untithelp_quantities_single(testClassObj:unittest.TestCase, data):
    data.set_area("2 m^2" )
    testClassObj.assertEqual(data.area.quantity, "A")
    testClassObj.assertEqual(data.area.value, 2)
    testClassObj.assertEqual(data.area.unit, "m^2")
    data.set_mass("4 g")
    testClassObj.assertEqual(data.mass.quantity, "m")
    testClassObj.assertEqual(data.mass.value, 4)
    testClassObj.assertEqual(data.mass.unit, "g")
    
    testClassObj.assertEqual(data.loading.quantity, "L")
    testClassObj.assertEqual(data.loading.value, 2)
    testClassObj.assertEqual(data.loading.unit, "g m^-2")
    


 
def unithelp_quantities_add(testClassObj:unittest.TestCase, datasType_with_a_length):
    datas = datasType_with_a_length
    
    for data in datas:
        data.set_area("2 m^2" )
        data.set_mass("2 g")
        untithelp_quantities_single(testClassObj, data)
    
    length = len(datasType_with_a_length)
    area = datas.area
    testClassObj.assertEqual(len(area), length)    
    for a in area:
        testClassObj.assertEqual(a.quantity, "A")
    #mass
    mass = datas.mass
    #mass
    testClassObj.assertEqual(len(mass), length)    
    for a in mass:
        testClassObj.assertEqual(a.quantity, "m")
    
    for data in datas:
        data.set_loading("1 g m^-2" )
    loading = datas.loading
    
    testClassObj.assertEqual(len(loading), length)    
    for a in loading:
        testClassObj.assertEqual(a.quantity, "L")
    
        


#@pytest.fixture
def pop_and_len(testClassObj:unittest.TestCase, datasType,value1,value2):
    datas = datasType
    datas.append(value1)
    datas.append(value2)
    testClassObj.assertEqual(len(datas), 2)
    testClassObj.assertEqual(datas[0], value1)
    testClassObj.assertEqual(datas[1], value2)
    datas.pop(1)
    testClassObj.assertEqual(len(datas), 1)