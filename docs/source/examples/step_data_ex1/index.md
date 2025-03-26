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
   from ec4py import Step_Data, AREA
```
## Load a file:



```python
   data = Step_Data("Steps_125706.tdms")
```


## Plot file

Plots the data an shows that there are 11 step.

```python
   data.plot()
   print(data.nr_of_steps)
```

![Plot of Step](./step_data_ex1_fig1.png)

## Plot the different steps on a relative time axis
The data is also normalized to

```python

p = None
for x in range(2,data.nr_of_steps):
    line, p=data[x].plot("Time","i", AREA, plot=p )
```

![Plot of Step](./step_data_ex1_fig2.png)

![Plot of Step](./step_data_ex1_fig1.png)
