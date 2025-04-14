
from ec4py import LSV_Data, LSV_Datas,RHE,POS,NEG

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

class test_lsv_datas_basic( unittest.TestCase ):
    
    def test_lsvs_voltammogram(self):
        data = LSV_Data()
        datas = LSV_Datas()
        datas.append(data)
        l = len(datas)
        self.assertEqual(l,1)
        
    def test_add(self):
        data = LSV_Data()
        data.i = data.E*2
        datab = data+0
        datas = LSV_Datas()
        datas.append(data)
        datas.append(datab)
        datas.add(2)
        for d in datas:
            self.assertTrue(np.allclose(d.i, d.E*2+2,  atol=1e-10, rtol=1e-10))
        datas2 =datas+datas
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i*2,  atol=1e-10, rtol=1e-10))
        datas2 =datas+2
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i+2,  atol=1e-10, rtol=1e-10))
        datas2 =datas+data
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i+data.i,  atol=1e-10, rtol=1e-10))
        
        ###add a list
        off=[2,3]
        datas2 =datas+off
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i+off[d],  atol=1e-10, rtol=1e-10))
        
        
        with self.assertRaises(ValueError):
            data2 =datas+[3]
        with self.assertRaises(ValueError):
            data2 =datas+[3,1,4]

        
    def test_sub(self):
        data = LSV_Data()
        data.i = data.E
        datab = data+0
        datas = LSV_Datas()
        datas.append(data)
        datas.append(datab)
        datas.sub(2)
        for d in datas:
            self.assertTrue(np.allclose(d.i, d.E-2,  atol=1e-10, rtol=1e-10))
        datas2 =datas-datas
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i*0,  atol=1e-10, rtol=1e-10))
        datas2 =datas-2
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i-2,  atol=1e-10, rtol=1e-10))
        datas2 =datas-data*2
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i-data.i*2,  atol=1e-10, rtol=1e-10))
        ###sub a list
        off=[2,3]
        datas2 =datas-off
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i-off[d],  atol=1e-10, rtol=1e-10))
        with self.assertRaises(ValueError):
            datas2 =datas-[3]
        with self.assertRaises(ValueError):
            datas2 =datas-[3,1,4]    
  
    def test_mul(self):
        data = LSV_Data()
        data.i = data.E*2
        datab = data+0
        datas = LSV_Datas()
        datas.append(data)
        datas.append(datab)
        datas.mul(2)
        for d in datas:
            self.assertTrue(np.allclose(d.i, d.E*4,  atol=1e-10, rtol=1e-10))
        datas2=datas*3
        for d in range(len(datas2)):    
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i*3,  atol=1e-10, rtol=1e-10))
        
        off=[2,3]
        datas2 =datas*off
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i*off[d],  atol=1e-10, rtol=1e-10))
        
     ###add a list
        with self.assertRaises(ValueError):
            data2 =datas*[3]
        with self.assertRaises(ValueError):
            data2 =datas*[3,1,4]  
        with self.assertRaises(TypeError):
            data2 =datas*datas  
        
    def test_div(self):
        data = LSV_Data()
        data.i = data.E*2
        datab = data+0
        datas = LSV_Datas()
        datas.append(data)
        datas.append(datab)
        datas.div(2)
        for d in datas:
            self.assertTrue(np.allclose(d.i, d.E,  atol=1e-10, rtol=1e-10))
        datas2=datas/(3.2)
        for d in range(len(datas2)):    
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i/3.2,  atol=1e-10, rtol=1e-10))
        datas2=datas/(3)
        for d in range(len(datas2)):    
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i/3,  atol=1e-10, rtol=1e-10))
        
        off=[2,3]
        datas2 =datas/off
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i, datas[d].i/off[d],  atol=1e-10, rtol=1e-10))
        
     ###add a list
        with self.assertRaises(ValueError):
            data2 =datas*[3]
        with self.assertRaises(ValueError):
            data2 =datas*[3,1,4]  
        with self.assertRaises(TypeError):
            data2 =datas*datas  
        


        
    def test_lsv_tafel(self):
        data = LSV_Data()
        tafel=100.0
        data.i = np.pow(10,data.E/tafel)
        slope=data.Tafel([0,1])
        self.assertAlmostEqual(tafel,slope.value)
        tafel=-60.0
        data.i = np.pow(10,data.E/tafel)
        slope=data.Tafel([0,1])
        self.assertAlmostEqual(tafel,slope.value)
        self.assertEqual("V/dec",slope.unit)


class test_LSV_Data_arrays(unittest.TestCase):
    def test_pop_and_len(self):
        from test_ec_datas_util import pop_and_len
        pop_and_len(self, LSV_Datas(), LSV_Data(),LSV_Data())

class test_lsv_datas( unittest.TestCase ):

    def test_check_files_exists(self):
        self.assertTrue(paths[0].exists)
        
    def test_load_a_file(self):
        data = LSV_Data(paths[0])
        self.assertFalse(data.name == "")
        
    def test_RHE_Shift(self):
        data = LSV_Data(paths[0])
        self.assertFalse(data.name == "")
        

    def test_integrate(self):
        data = LSV_Data()
        data.i = np.ones(len(data.E))
        q = data.integrate(0,1)
        self.assertAlmostEqual(float(q),1)
        q = data.integrate(-1,1)
        self.assertAlmostEqual(float(q),2)
        self.assertEqual(str(q),"2.000e+00 C")
        
    def test_set_i_at_E_to_zero(self):
        data = LSV_Data()
        data.i = np.ones(len(data.E)) 
        datas = LSV_Datas()
        datas.append(data)
        datas.append(data.copy())
        datas.set_i_at_E_to_zero(-2.5)
        for d in datas:
            self.assertTrue(np.allclose(d.i, d.E*0,  atol=1e-10, rtol=1e-10))

          
     
  

if __name__ == '__main__':
    unittest.main()
