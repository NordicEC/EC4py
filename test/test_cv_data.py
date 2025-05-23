
from ec4py import CV_Data,RHE,POS,NEG

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

######################################################################################
class test_CV_Data_arithmetics( unittest.TestCase ):
    def test_s1_add(self):
        data = CV_Data()
        data.i_p = data.E*2
        data.i_n = data.E+2
        data.add(data)
        self.assertTrue(np.allclose(data.i_p, data.E*4,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data.i_n, data.E*2+4,  atol=1e-10, rtol=1e-10))
        data2 =data+data+data
        self.assertTrue(np.allclose(data2.i_p, data.E*4*3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, (data.i_n)*3,  atol=1e-10, rtol=1e-10))
        ###add a number
        data2 =data+4
      #  print(data.i_p+4)
      #  print(data2.i_p)
        self.assertTrue(np.allclose(data2.i_p, data.i_p+4,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n+4,  atol=1e-10, rtol=1e-10))
        ###add a list
        data2 =data+[3,6]
        self.assertTrue(np.allclose(data2.i_p, data.i_p+3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n+6,  atol=1e-10, rtol=1e-10))
        with self.assertRaises(ValueError):
            data2 =data+[3]
        with self.assertRaises(ValueError):
            data2 =data+[3,1,4]

        
    def test_s2_sub(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        data.sub(data)
        self.assertTrue(np.allclose(data.i_p, data.E*0,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data.i_n, data.E*0,  atol=1e-10, rtol=1e-10))
        ### sub multiple cvs
        data.i_p = data.E
        data.i_n = data.E+2
        data2 =data-data-data
        self.assertTrue(np.allclose(data2.i_p, data.i_p*-1,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n*-1,  atol=1e-10, rtol=1e-10))
        ###sub a number
        data2 =data-3
        self.assertTrue(np.allclose(data2.i_p, data.i_p-3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n-3,  atol=1e-10, rtol=1e-10))
        ###sub a list
        data2 =data-[3,6]
        self.assertTrue(np.allclose(data2.i_p, data.i_p-3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n-6,  atol=1e-10, rtol=1e-10))
        with self.assertRaises(ValueError):
            data2 =data-[3]
        with self.assertRaises(ValueError):
            data2 =data-[3,1,4]
            
    def test_a3_mul(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        data.mul(3)
        self.assertTrue(np.allclose(data.i_p, data.E*3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data.i_n, (data.E+2)*3,  atol=1e-10, rtol=1e-10))
        ### sub multiple cvs
        data.i_p = data.E
        data.i_n = data.E+2
        data2 =data*2
        self.assertTrue(np.allclose(data2.i_p, data.i_p*2,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n*2,  atol=1e-10, rtol=1e-10))
        ###sub a number
        with self.assertRaises(TypeError):
            data*data
        
    def test_a4_div(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        data.div(3)
        self.assertTrue(np.allclose(data.i_p, data.E/3,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data.i_n, (data.E+2)/3,  atol=1e-10, rtol=1e-10))
        ### sub multiple cvs
        data.i_p = data.E
        data.i_n = data.E+2
        data2 =data/2
        self.assertTrue(np.allclose(data2.i_p, data.i_p/2,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data2.i_n, data.i_n/2,  atol=1e-10, rtol=1e-10))
        ###sub a number
        #with self.assertRaises(TypeError):
        #    atesting = data/data
            
#############################################################

class test_CV_Data( unittest.TestCase ):
    
    def test_check_files_exists(self):
        self.assertTrue(paths[0].exists)
        
    def test_load_a_file(self):
        data = CV_Data(paths[0])
        self.assertFalse(data.name == "")
        
    def test_RHE_Shift(self):
        data = CV_Data(paths[0])
        self.assertFalse(data.name == "")
        
    def test_get_sweep(self):
        data = CV_Data()
        data.i_p = data.E*2
        data.i_n = data.E*-3
        lsv_p = data.get_sweep(POS)
        self.assertTrue(np.allclose(data.i_p,lsv_p.i,  atol=1e-10, rtol=1e-10))
       
        lsv_n = data.get_sweep(NEG)
        self.assertTrue(np.allclose(data.i_n,lsv_n.i,  atol=1e-10, rtol=1e-10))

        lsv_avg = data.get_sweep("AVG")
        self.assertTrue(np.allclose((data.i_p+data.i_n)/2,lsv_avg.i,  atol=1e-10, rtol=1e-10))

        lsv_d = data.get_sweep("dif")
        self.assertTrue(np.allclose((data.i_p-data.i_n),lsv_d.i,  atol=1e-5, rtol=1e-5))

    def test_set_i_at_E_to_zero(self):
        data = CV_Data()
        data.i_p = np.ones(len(data.E)) 
        data.i_n = np.ones(len(data.E))*2 
        data.set_i_at_E_to_zero(-2.5)
        self.assertTrue(np.allclose(data.i_p, data.E*0,  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data.i_n, data.E*0,  atol=1e-10, rtol=1e-10))
          
    def test_Tafel(self):
        data = CV_Data(path_to_dataSetFolder/ "CV_153559_ 3.tdms")
        k = data.Tafel([-0.2,0],-0.6)
        self.assertEqual(k[0].unit,"V/dec")
        v =k[0].value
        v=np.abs(k[0].value)*1000
        self.assertTrue(v>40 and v<140)
        
    def test_Tafel_LSV(self):
        data = CV_Data(path_to_dataSetFolder/ "CV_153559_ 3.tdms")
        lsv_p = data.get_sweep(POS)
        k = data.Tafel([-0.2,0],-0.6)
        k_p = lsv_p.Tafel([-0.2,0],-0.6)
        self.assertEqual(k[0].unit,"V/dec")
        v =k[0].value
        v=np.abs(k[0].value)*1000
        self.assertTrue(v>40 and v<140)
        self.assertEqual(k_p.unit,"V/dec")
        v_p =k_p.value
        v_p=np.abs(k_p.value)*1000
        self.assertAlmostEqual(v_p,v,places=0)
        self.assertTrue(v_p>40 and v_p<140)
        
    
    def test_Tafel_RHE(self):
        data = CV_Data(path_to_dataSetFolder/ "CV_153559_ 3.tdms")
        data.set_RHE(-0.9)
        k = data.Tafel([0.8,0.9],0,7,RHE)
        self.assertEqual(k[0].unit,"V/dec")
        v =k[0].value
        v=np.abs(k[0].value)*1000
        #print(v)
        # self.assertEqual(v,6)

        self.assertTrue(v>40 and v<140)
    
    
  

if __name__ == '__main__':
    unittest.main()
