---
title: Example 2 - Tafel Analysis
parent: CV_Data
grand_parent: Examples
---
# Example 2: class CV_Data - Tafel Analysis

## Download dataset


Start by downloading a test file from github:

[CV_152635_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_152635_%203.tdms)

and save it an appropriate folder.

## Import the class:

```python
   from ec4py import CV_Data
```
## Load a file:



```python
   data = CV_Data("CV_152635_ 3.tdms")
```


## Plot file and add some smoothing

```python
   line,p = data.plot()
   data.plot(plot = p, y_smooth = 10)
```

![Plot of CV](./cv_data_ex2_fig1.png)


## Tafel Analysis

```python
   Tafel_Range = [-0.03,-0.15]
   slopes = data.Tafel(Tafel_Range)
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_data_ex2_fig2.png)

## Tafel Analysis using diffusion limit correction


```python
   Tafel_Range = [-0.03,-0.15]
   E_dl = -0.4
   slopes = data.Tafel(Tafel_Range,E_dl)
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_data_ex2_fig3.png)
