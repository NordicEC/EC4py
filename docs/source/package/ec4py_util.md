---
title: Quantity_Value_Unit
parent: Package
nav_order: 100
---


# class ec4py.Quantity_Value_Unit() <br>-- class to handle quantities, values and units

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
    print(area) #the result is "2 m^3"
```

## Operators
### - __Quantity_Value_Unit__ and a __scalar__
The arithmetic operators * (multiplication), / (division), ** (exponentiation) are supported between **Quantity_Value_Unit** and a float or an int.
```python
    length = QVU("10 m")
    print(length / 10) #the result is "1 m"
    print(length * 5) #the result is "5 m"
    print(length ** 3) #the result is "1000 m^3"
```
### - __Quantity_Value_Unit__ and __Quantity_Value_Unit__
Arithemtics operators between **Quantity_Value_Unit** and another **Quantity_Value_Unit** are the following: 
+ (addition), - (subtraction), * (multiplication), / (division)
please note that:
- for addition and subtraction, the unit must be the same. 
```python
    length = QVU("1 m")
    area = QVU("2 m^2")
    length+area # this results in error as both units must be the same.
    volume = length*area
    print(volume) #the result is "2 m^3"
```


## Methods and properties

### Quantity_Value_Unit.__value__
The value of a quantity:
```python
    length = QVU("5.3 m")
    print(length.value) #the result is "5.3"
    length.value = 23
    print(length.value) #the result is "23"
    print(length) #the result is "23 m"
```

### Quantity_Value_Unit.**unit**
The unit of a quantity:
```python
    length = QVU("1 m")
    print(length.unit) #the result is "m"
    volume = QVU(4,"m^3","v")
    print(length.unit) #the result is "m^3"
```

### Quantity_Value_Unit.**quantity**
The name of a quantity:

```python
    length = QVU(5,"m","d")
    print(length.quantity) #the result is "d"
```

### Quantity_Value_Unit.__set_quantity(new_quantity_label:str)__
Manually set the quantity name after the class has been initialized.
```python
   length = QVU(5,"m","d")
   length.set_quantity("len")
   print(length.quantity) #the result is "len"
```

### Quantity_Value_Unit.__set_unit(self, new_unit_label:str)__
Manually set the unit name after the class has been initialized.
```python
   length = QVU(5,"m","d")
   length.set_unit("cm")
   print(length.unit) #the result is "cm"
```

    
