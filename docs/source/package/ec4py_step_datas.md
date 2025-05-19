---
title: Step_Datas
parent: Package
nav_order: 1
---


# class ec4py.Step_Datas()<br> -- list class of Step data analysis and display. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)


## Basic use:

Import class:
```python
   from ec4py import Step_Datas
```
Load data set:
```python
   data = Step_Datas("List of PATH TO DATA")
   data = Step_Datas(["PATH1 TO DATA","PATH2 TO DATA",...])
```



## Initialization

### class ec4py.cv_data.CV_Data(Paths=None, args, kwargs)
```python
   data = Step_Datas() # empty object
   data = Step_Datas(["PATHs"]) # import the data from a file.
   data = Step_Datas(["PATHs TO DATA FILE"], IRCORR="R") # import the data from a file and apply iR-correction.
```

## Operators

**Step_Datas** does not support any operators.


## Methods and properties

**Step_Datas** is a list class of **Step_Datas**, which inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable. The result are returned as a list.

### Step_Datas.**plot()**

Creates a standard plot of a Step data(s), i.e. current vs time. Add [arguments](ec4py_args.md) and [keywords](ec4py_keywords.md) to easily modify the plot.
```python
   sds = Step_Datas()
   sds.plot(RHE,AREA) # plot data vs RHE and normalize the current to geometric area.
```

### Step_Datas.**get_current_at_time(time_s_:float, dt_s_:float =0 ,*args, **kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the curent at a specific time. [Arguments](ec4py_args.md) can be used to normalize the current and shift the potential.
```python
   sd = Steps_Datas()
   sd.get_current_at_time(0.1) # gets the current at 0.1V.
```

### Step_Datas.**get_voltage_at_time(i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs)**
A list of [Quantity_Value_Unit](ec4py_util.md) representation of the voltage at a specific time. 

 
### Step_Datas.**set_active_RE(new_reference_electrode=None)**
Shifts the voltage to be relative another reference electrode. None related to the experimental reference electrode. See [Arguments](ec4py_args.md)
```python
   sds = Step_Datas()
   sds.set_active_RE(RHE)
```

### Step_Datas.**norm(norm_to)**

Normalise the current to certain factors. See [Arguments](ec4py_args.md)
```python
   sds = Step_Datas()
   sds.norm(AREA) # the current is now normalized to area
```


### Step_Datas.**integrate(self, t_start:float,t_end:float, step_nr:int = -1, *args, **kwargs)**
A list [Quantity_Value_Unit](ec4py_util.md) representation of the integrated current between two time limits. Arguments can be used to normailze the current and shift the potential.
```python
   sds = Step_Datas()
   sds.integrate(0.1,1.1) # integrate the current between 0.1 and 1.1 V.
```

### Step_Datas.**Tafel(self,*args, **kwargs)**
A [Quantity_Value_Unit](ec4py_util.md) representation of the Tafel slope, i.e. the fitting of a line to the data in a Tafel plot. Use the keyword: t and td or t_min and t_max to specify the time when to sample the voltage and current in the step. Use Emax and Emin to specify potential limits for the fit.  Arguments can be used to normailze the current and shift the potential.
Keywords:
   - t : float time at which to take the data point. defaults to "last"        
   - dt : float time window to use for the average in seconds. defaults to 0
   or
   - t_min : float minimum time to use for data selection. Use this instead of "t" and "dt"
   - t_max : float maximum time to use for data selection. Use this instead of "t" and "dt"
   - Emax:float maximum voltage to use for fitting. defaults to 1000
   - Emin:float minimum voltage to use for fitting. defaults to -1000
   - step_nr (int, optional): 

