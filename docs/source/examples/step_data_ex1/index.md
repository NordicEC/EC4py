---
title: Example 1 
parent: Step_Data
grand_parent: Examples
---
# Example 1: class Step_Data - Basics


## Download dataset


Start by downloading a test file from github:

[Steps_125706.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/Step/Rotation/Steps_125706.tdms)

and save it an appropriate folder.

## Import the class:

```python
   from ec4py import Step_Data
```
## Load a file:



```python
   data = Step_Data("Steps_125706.tdms")
```


## Plot file

```python
   data.plot()
```

![Plot of Step](./step_data_ex1_fig1.png)

