---
title: LSV_Data
parent: Package
nav_order: 1
---


# class ec4py.LSV_Data()<br> -- LSV data analysis and display. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)

## Basic use:

Import class:
```python
   from ec4py import LSV_Data
```
Load data set:
```python
   data = LSV_Data("PATH TO DATA")
   current = data.i #current array
   E = data.E # voltage array
```
## Initialization

### class ec4py.lsv_data.LSV_Data(Path=None, args, kwargs)
```python
   data = LSV_Data() # empty object
   data = LSV_Data("PATH TO DATA FILE") # import the data from a file.
   data = LSV_Data("PATH TO DATA FILE", IRCOMP="R") # import the data from a file and apply iR-compensation.
```


## Operators

An operator used on a **LSV_Data** object always result in a new LSV **LSV_Data**.

### LSV_Data and a scalar

The arithmetic operators * (multiplication) and / (division) are supported between **LSV_Data** and a float or an int. The result is always a new **LSV_Data**
```python
   new_data = LSV_Data()*5  # the resulting LSV has its current multiplied by 5
   new_data = LSV_Data()/5  # the resulting LSV has its current divided by 5
```
### LSV_Data and LSV_Data

Arithemtics operators between **LSV_Data** and another **LSV_Data** are the following: 
+ (addition) and - (subtraction)
```python
   lsv1 = LSV_Data()
   lsv2 = LSV_Data()
   new_lsv1 = lsv1+lsv2
   new_lsv2 = lsv1-lsv2
```

## Methods and properties

**LSV_Data** inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable.


### LSV_Data.**get_i_at_E(E:float, direction:str = "all",*args, **kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the curent at a specific voltage. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.
```python
   lsv1 = LSV_Data()
   lsv1.get_i_at_E(0.1) # gets the current at 0.1V.
```

### LSV_Data.**get_E_at_i(i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage at a specific current. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.

### LSV_Data.**get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a maximum between two voltage limits. [Arguments](ec4py_args.md#for-normalization-of-current) can be used to shift the potential.
```python
   lsv1 = LSV_Data()
   lsv1.get_E_of_max_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### LSV_Data.**get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a minimum between two voltage limits. [Arguments](ec4py_args.md#for-normalization-of-current) can be used to shift the potential.
```python
   lsv1 = LSV_Data()
   lsv1.get_E_of_min_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

