---
title: CV_Datas
parent: Package
nav_order: 1
---


# class ec4py.CV_Datas()<br> -- list class of CV data analysis and display. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)


## Basic use:

Import class:
```python
   from ec4py import CV_Datas
```
Load data set:
```python
   data = CV_Datas("List of PATH TO DATA")
   data = CV_Datas(["PATH1 TO DATA","PATH2 TO DATA",...])
```



## Initialization

### class ec4py.cv_data.CV_Data(Paths=None, args, kwargs)
```python
   data = CV_Datas() # empty object
   data = CV_Datas(["PATHs"]) # import the data from a file.
   data = CV_Datas(["PATHs TO DATA FILE"], IRCOMP="R") # import the data from a file and apply iR-compensation.
```

## Operators

Using a operator to **CV_Datas** awalys result in a new dataset. 
```python
   new_CVs = CV_Datas()*5  # the resulting CV has current of positive and negative sweep multiplied by 5
   new_CVs = CV_Datas()/5  # the current of positive and negative sweep are divided by 5
```

### CV_Datas and singular object.

As  **CV_Datas**  is a list class of [CV_Data](ec4py_cv_datas), the same operators are supported between  **CV_Datas** and a scalar object. The operattion is applied to each containing data set in **CV_Datas**

The arithmetic operators + (addition), - (subtraction), * (multiplication) and / (division) are supported between **CV_Datas** and a scalar number. The result is always a new **CV_Datas**

### CV_Datas and CV_Datas

Arithemtics operators between **CV_Datas** and another **CV_Datas** are 
+ (addition) and - (subtraction). Both objects must contain the same number of datasets. 
```python
   cv1 = CV_Data()
   cv2 = CV_Data()
   new_CV1 = cv1+cv2
   new_CV2 = cv1-cv2
```

## Methods and properties

**CV_Datas** is a list class of **CV_Datas**, which inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable. The result are returned as a list.

### CV_Datas.**plot()**

Creates a standard plot of a CV data(s), i.e. current vs potental. Add [arguments](ec4py_args.md) and [keywords](ec4py_keywords.md) to easily modify the plot.
```python
   cvs = CV_Data()
   cvs.plot(RHE,AREA) # plot data vs RHE and normalize the current to geometric area.
```

### CV_Datas.**get_i_at_E(E:float, direction:str = "all",*args, **kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the curent at a specific voltage. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.
```python
   cvs = CV_Data()
   cvs.get_i_at_E(0.1) # gets the current at 0.1V.
```

### CV_Data.**get_E_at_i(i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage at a specific current. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.

### CV_Datas.**get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a maximum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   cvs = CV_Data()
   cvs.get_E_of_max_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### CV_Datas.**get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a minimum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   cvs = CV_Data()
   cvs.get_E_of_min_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### CV_Datas.**get_sweep(sweep:str)**
A [LSVs](ec4_py_lsvs.md) representation of the selected sweep: POS, NEG, AVG & DIF.See [Arguments](ec4py_args.md#for-cv_data-cv_datas)
```python
   cvs = CV_Datas()
   lsvs = cvs.get_sweep(AVG) # returns the average of positive and negative sweeps.
```

### CV_Datas.**set_active_RE(new_reference_electrode=None)**
Shifts the voltage to be relative another reference electrode. None related to the experimental reference electrode. See [Arguments](ec4py_args.md)
```python
   cvs = CV_Datas()
   cvs.set_active_RE(RHE)
```

### CV_Datas.**norm(norm_to)**

Normalise the current to certain factors. See [Arguments](ec4py_args.md)
```python
   cvs = CV_Datas()
   cvs.norm(AREA) # the current is now normalized to area
```


### CV_Datas.**integrate(self, start_E:float, end_E:float, *args, **kwargs)**
 A list [Quantity_Value_Unit](ec4py_util.md) representation of the integrated current between two voltage limits. Arguments can be used to normailze the current and shift the potential.
```python
   cv1 = CV_Data()
   cv1.integrate(0.1,1.1) # integrate the current between 0.1 and 1.1 V.
```


