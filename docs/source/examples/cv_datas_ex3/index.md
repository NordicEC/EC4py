---
title: Example 3 - Levich Analysis
parent: CV_Datas
grand_parent: Examples
---
# Example 3: class CV_Datas - Levich Analysis

## Download dataset


Start by downloading a test file from github:
   [CV_151512_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_151512_%203.tdms)
   [CV_151725_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_151725_%203.tdms)
   [CV_153036_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_153036_%203.tdms)
   [CV_152150_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_152150_%203.tdms)
   [CV_152403_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_152403_%203.tdms)
   [CV_152635_ 3.tdms](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/CV_152635_%203.tdms)

and save it an appropriate folder.

## Import the class:

```python
   from ec4py import CV_Data
```
## Load a file:



```python
   paths = [
   "CV_151512_ 3.tdms",
   "CV_151725_ 3.tdms",
   "CV_153036_ 3.tdms",
   "CV_152150_ 3.tdms",
   "CV_152403_ 3.tdms",
   "CV_152635_ 3.tdms",
]
   datas = CV_Datas(paths)
```

## Datas

```python
   datas.plot(legend="rot")
```

![Plot of CVs](./cv_datas_ex3_fig1.png)

## Plot of data normalized to the square root of rotation.

```python
   datas.plot("sqrt_rot",legend="rot")
```

![Plot of CVs](./cv_datas_ex3_fig2.png)


## Levich Analysis

```python
   Epot = -0.5
   slopes = datas.Levich(Epot)
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_datas_ex3_fig3.png)

## Levich Analysis when normalizing the current to area


```python
   Epot = -0.5
   slopes = datas.Levich(Epot, "area_cm")
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_datas_ex3_fig4.png)
