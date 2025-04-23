---
title: Step_Data
parent: Package
nav_order: 1
---


# class ec4py.Step_Data()<br> -- Step data analysis and display. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)



## Basic use:

Import class:
```python
   from ec4py import Step_Data
```
Load data set:
```python
   data = Step_Data("PATH TO DATA")
   current = data.i #current array
   E = data.E # voltage array
   time = data.Time # time array
```
## Initialization

### class ec4py.lsv_data.LSV_Data(Path=None, args, kwargs)

```python
   data = Step_Data() # empty object
   data = Step_Data("PATH TO DATA FILE") # import the data from a file.
   data = Step_Data("PATH TO DATA FILE", IRCORR="R") # import the data from a file and apply iR-correction.
```


## Operators

**Step_Data** does not support any operators.

## Methods and properties

**Step_Data** inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable.


### Step_Data.**plot()**

Creates a standard plot of a Step data, i.e. current vs time. 
```python
   st = Step_Data()
   st.plot() 
```

