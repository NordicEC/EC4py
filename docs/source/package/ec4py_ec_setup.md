---
title: EC_Setup
parent: Package
nav_order: 1
---


# class ec4py.EC_Setup() <br>-- class to handle meta data of the electrochemical data file. 

- [Basic use](#basic-use)
- [Methods and properties](#methods-and-properties)


## Basic use:

The class is a parent class of EC_Data.

## Methods and properties


### EC_Setup.__area__

A [Quantity_Value_Unit](ec4py_util.md) representation of the geometric area.
```python
   area = EC_Setup().area
```

### EC_Setup.__area_unit__

A string representation of the area unit.
```python
   area_unit = EC_Setup().area_unit
```

### EC_Setup.__rotation__

A [Quantity_Value_Unit](ec4py_util.md) representation of the rotation rate.
```python
   area_unit = EC_Setup().area_unit
```

### EC_Setup.__rate__

A [Quantity_Value_Unit](ec4py_util.md) representation of the sweep rate in the case of voltammetry data.
```python
   rate = EC_Setup().rate
```

### EC_Setup.__weight__

A [Quantity_Value_Unit](ec4py_util.md) representation of the catalyst weight.
```python
   m = EC_Setup().weight
```

### EC_Setup.__loading__

A [Quantity_Value_Unit](ec4py_util.md) representation of the catalyst loading.
```python
   loading = EC_Setup().loading
```

### EC_Setup.__pressure__

A [Quantity_Value_Unit](ec4py_util.md) representation of the pressure of the system.
```python
   loading = EC_Setup().loading
```

### EC_Setup.__temp0__

A [Quantity_Value_Unit](ec4py_util.md) representation of the temperature of the system.
```python
   loading = EC_Setup().loading
```

### EC_Setup.__RE__

A string representation of name of the reference electrode.
```python
   reference_electrode = EC_Setup().RE
```

### EC_Setup.__is_MWE__

A bool representation if the data file comes from a multi working electrode.
```python
   is_MWE = EC_Setup().is_MWE
```
