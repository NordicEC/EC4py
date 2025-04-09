---
title: LSV_Datas
parent: Package
nav_order: 1
---


# class ec4py.LSV_Datas() <br>-- list class of LSV data. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)


## Basic use:

Import class:
```python
   from ec4py import LSV_Datas
```
Load data set:
```python
   data = LSV_Datas("List of PATH TO DATA")
   data = LSV_Datas(["PATH1 TO DATA","PATH2 TO DATA",...])
```


## Initialization

### class ec4py.lsv_data.LSV_Datas(Path=None, args, kwargs)
```python
   data = LSV_Datas() # empty object
   data = LSV_Datas(["PATHs"]) # import the data from a file.
   data = LSV_Datas(["PATHs TO DATA FILE"], IRCOMP="R") # import the data from a file and apply iR-compensation.
```

## Operators

Using a operator to **LSV_Datas** awalys result in a new dataset.

```python
   new_LSVs = LSV_Datas()*5  # For each lsv in the dataset, the current data array is multiplied by 5.
   new_LSVs = LSV_Datas()/5  # For each lsv in the dataset, the current data array is divided by 5.
```

### LSV_Datas and singular object.

As  **LSV_Datas**  is a list class of [LSV_Data](ec4py_lsv_datas), the same operators are supported between  **LSV_Datas** and a scalar object. The operattion is applied to each containing data set in **LSV_Datas**

The arithmetic operators + (addition), - (subtraction), * (multiplication) and / (division) are supported between **LSV_Datas** and a scalar number. The result is always a new **LSV_Datas**

### LSV_Datas and LSV_Datas

Arithemtics operators between **LSV_Datas** and another **LSV_Datas** are 
+ (addition) and - (subtraction). Both objects must contain the same number of datasets. 
```python
   datas1 = LSV_Datas()
   datas2 = LSV_Datas()
   new_datas1 = datas1+datas2
   new_datas2 = datas1-datas2
```

## Methods and properties

**LSV_Datas** is a list class of **LSV_Data**, which inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable. The result are returned as a list.

### LSV_Datas.**plot()**

Creates a standard plot of a LSV data(s), i.e. current vs potental. Add [arguments](ec4py_args.md) and [keywords](ec4py_keywords.md) to easily modify the plot.
```python
   datas = LSV_Data()
   datas.plot(RHE,AREA) # plot data vs RHE and normalize the current to geometric area.
```

### LSV_Datas.**get_i_at_E(E:float, direction:str = "all",*args, **kwargs)**

A list of [Quantity_Value_Unit](ec4py_util.md) representation of the curent at a specific voltage. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.
```python
   datas = LSV_Datas()
   datas.get_i_at_E(0.1) # gets the current at 0.1V.
```

### LSV_Datas.**get_E_at_i(i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs)**

A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage at a specific current. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.

### LSV_Datas.**get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs)**

A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a maximum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   datas = LSV_Datas()
   datas.get_E_of_max_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### LSV_Datas.**get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs)**

A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage where the current reaches a minimum between two voltage limits. [Arguments](ec4py_args.md) can be used to shift the potential.
```python
   datas = LSV_Datas()
   datas.get_E_of_min_i(0.1,0.5) # returns the voltage where the current reaches the max.
```

### LSV_Datas.**set_active_RE(new_reference_electrode=None)**

Shifts the voltage to be relative another reference electrode. None related to the experimental reference electrode. See [Arguments](ec4py_args.md)
```python
   datas = LSV_Datas()
   datas.set_active_RE(RHE)
```

### LSV_Datas.**norm(norm_to)**

Normalise the current to certain factors. See [Arguments](ec4py_args.md)
```python
   datas = LSV_Datas()
   datas.norm(AREA) # the current is now normalized to area
```


### LSV_Datas.**integrate(self, start_E:float, end_E:float, *args, **kwargs)**

 A list [Quantity_Value_Unit](ec4py_util.md) representation of the integrated current between two voltage limits. [Arguments](ec4py_args.md) can be used to normailze the current and shift the potential.
```python
   datas = LSV_Datas()
   datas.integrate(0.1,1.1) # integrate the current between 0.1 and 1.1 V.
```


