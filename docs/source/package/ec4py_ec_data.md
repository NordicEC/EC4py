---
title: EC_Data
parent: Package
nav_order: 1
---



# class ec4py.EC_Data()<br> -- Base class. 

- [Basic use](#basic-use)
- [Initialization](#initialization)
- [Operators](#operators)
- [Methods and properties](#methods-and-properties)


## Basic use:

Import class:
```python
   from ec4py import EC_Data
```

Load data set:
```python
   data = EC_Data("PATH TO DATA")
   data.plot("E","i")
```


## Initialization

### class ec4py.ec_data.EC_Data(path = None, args, kwargs)
```python
   data = EC_Data() # empty object
   data = EC_Data("PATH TO DATA FILE") # import the data from a file.
```

## Operators

No operators are supported.

## Methods and properties

**EC_Data** inherit from [EC_Setup](ec4py_ec_setup.md) and all properties and function are obtainable.

### EC_Data.plot(self, x_channel: str, y_channel: str, *args,**kwargs)

Creates a scatter plot based on the selected channels.  
```python
   data = EC_Data() # empty object
   data.plot("E","i") # import the data from a file.
```


