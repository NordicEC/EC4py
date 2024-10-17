---
title: Example 2 - Tafel Analysis
parent: CV_Datas
grand_parent: Examples
---
# Example 2: class CV_Datas - Tafel Analysis

## Download dataset


Start by downloading a test file from github:

[CV_152635_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_152635_%203.tdms)

[CV_153036_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_153036_%203.tdms)
and save it an appropriate folder.

## Import the class:

```python
   from ec4py import CV_Datas
```
## Load a file:


```python
   data = CV_Data(["CV_152635_ 3.tdms","CV_153036_ 3.tdms"])
```


## Tafel Analysis

```python
   slopes = data.Tafel(Tafel_Range,-0.4)
   print(slopes[0][0], slopes[0][1])
   print(slopes[1][0], slopes[1][1] )
```

![Plot of CV](./cv_data_ex2_fig1.png)


## Tafel Analysis using diffusion limit correction

```python
Edl=-0.5
slopes = data.Tafel(Tafel_Range,Edl)
print(slopes[0][0], slopes[0][1])
print(slopes[1][0], slopes[1][1] )
```

![Plot of CVs](./cv_data_ex2_fig2.png)

## Tafel Analysis using diffusion limit correction

