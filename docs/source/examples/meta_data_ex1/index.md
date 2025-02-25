---
title: Example 1
parent: CV_Data
grand_parent: Examples
---
# Example 1: class CV_data - Basics


## Download dataset


Start by downloading a test file from github:

[CV_144700_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_144700_%203.tdms)

and save it an appropriate folder.

## Import the class:

```python
   from ec4py import CV_Data
```
## Load a file:



```python
   data = CV_Data("CV_144700_3.tdms")
```


## Plot file

```python
   data.plot()
```

![Plot of CV](./cv_data_ex1_fig1.png)


## Visualize that a CV consists of two LSV

```python
   line, p = data.plot(dir="pos")
   data.plot(dir="neg", plot = p)
```

![Plot of CVs](./cv_data_ex1_fig2.png)

## Get the current at a specific potential

```python
   i_p, i_n = data.get_i_at_E(-0.4)
   print(i_p,i_n)
```
