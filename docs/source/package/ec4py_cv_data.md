---
title: CV_Data
parent: Package
nav_order: 1
---



# class ec4py.CV_Data()<br> -- CV data analysis and display. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)


## Basic use:

Import class:
```python
   from ec4py import CV_Data
```
Load data set:
```python
   data = CV_Data("PATH TO DATA")
```


## Initialization

### class ec4py.cv_data.CV_Data(Path=None, args, kwargs)
```python
   data = CV_Data() # empty object
   data = CV_Data("PATH TO DATA FILE") # import the data from a file.
   data = CV_Data("PATH TO DATA FILE", IRCOMP="R") # import the data from a file and apply iR-compensation.
```

## Operators

### CV_Data and a scalar

The arithmetic operators * (multiplication) and / (division) are supported between **CV_Data** and a float or an int. The result is always a new **CV_Data**
```python
   new_CV = CV_Data()*5  # the resulting CV has current of positive and negative sweep multiplied by 5
   new_CV = CV_Data()/5  # the current of positive and negative sweep are divided by 5
```
### CV_Data and CV_Data

Arithemtics operators between **CV_Data** and another **CV_Data** are the following: 
+ (addition) and - (subtraction)
```python
   cv1 = CV_Data()
   cv2 = CV_Data()
   new_CV1 = cv1+cv2
   new_CV2 = cv1-cv2
```

## Methods and properties

**CV_Data** inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable.

### CV_Data.**plot()**

Creates a standard plot of a CV data, i.e. current vs potental. The plot() support


### CV_Data.**get_i_at_E(E:float, direction:str = "all",*args, **kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the curent at a specific voltage. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.
```python
   cv1 = CV_Data()
   cv1.get_i_at_E(0.1) # gets the current at 0.1V.
```

### CV_Data.**get_E_at_i(i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage at a specific current. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.

### CV_Data.**get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a maximum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   cv1 = CV_Data()
   cv1.get_E_of_max_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### CV_Data.**get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a minimum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   cv1 = CV_Data()
   cv1.get_E_of_min_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### CV_Data.**get_sweep(sweep:str)**
A [LSV](ec4_py_lsv.md) representation of the selected sweep: POS, NEG, AVG & DIF. See also [Arguments](ec4py_args.md#for-cv_data-cv_datas)
```python
   cv1 = CV_Data()
   lsv = cv1.get_sweep(AVG) # returns the average of positive and negative sweeps.
```

### CV_Data.**set_active_RE(new_reference_electrode=None)**
Shifts the voltage to be relative another reference electrode.See [Arguments](ec4py_args.md#for-adjusting-the-reference-electrode). None related to the experimental reference electrode. 
```python
   cv1 = CV_Data()
   cv1.set_active_RE(RHE)
```

### CV_Data.**norm(norm_to)**

Normalise the current to certain factors. See [Arguments](ec4py_args.md#for-normalization-of-current)
```python
   cv1 = CV_Data()
   cv1.norm(AREA) # the current is now normalized to area
```

### CV_Data.**conv(ec_data: EC_Data, *args, ** kwargs)**
Convert a [EC_Data](ec4py_ec_data.md) to CV_Data.



### CV_Data.**integrate(self, start_E:float, end_E:float, *args, **kwargs)**
 A [Quantity_Value_Unit](ec4py_util.md) representation of the integrated current between two voltage limits. [Arguments](ec4py_args.md) can be used to normailze the current and shift the potential.
```python
   cv1 = CV_Data()
   cv1.integrate(0.1,1.1) # integrate the current between 0.1 and 1.1 V.
```


