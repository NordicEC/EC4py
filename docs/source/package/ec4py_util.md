---
title: Quantity_Value_Unit
parent: Package
nav_order: 1
---


# class ec4py.Quantity_Value_Unit() -- class to handle quantities, values and units.. 

## Basic use:
Importing the class:
```python
   from ec4py import Quantity_Value_Unit as QVU
```

Give a quantity a value and a unit.
```python
    length1 = QVU("1 m")
    length2 = QVU("2 m")
    area = length1*length2
    print(area)
```
This results in "2 m^2"

## Operators
The main arithmetic operators are + (addition), - (subtraction), * (multiplication), / (division), ** (exponentiation) are supported between **Quantity_Value_Unit** and a float or an int.

Arithemtics operators between **Quantity_Value_Unit** and another **Quantity_Value_Unit**, please note that:
- for addition and subtraction, the unit must be the same. 
```python
    length = QVU("1 m")
    area = QVU("2 m^2")
    length+area # this results in error as both units must be the same.
    volume = length*area
    print(volume) #the result is "2 m^3"
```


## Methods and properties¶


EC_Setup.*area*
A Quantity representation of the geometric area.
```python
   area = EC_Setup().area
```

EC_Setup.*area*
A Quantity representation of the area.
```python
   area = EC_Setup().area
```
