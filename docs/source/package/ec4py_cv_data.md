---
title: CV_Data
parent: Package
nav_order: 1
---


# class ec4py.CV_Data() -- CV data analysis and display. 

## Basic use:

Import class:
```python
   from ec4py import CV_Data
```
Load data set:
```python
   data = CV_Data("PATH TO DATA")
```


## General properties

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


  
  
