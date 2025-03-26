---
title: Example 4 - Levich Analysis using LSVs
parent: CV_Datas
grand_parent: Examples
---
# Example 3: class CV_Datas and LSV_Datas - Levich Analysis

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
   from ec4py import *
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
   datas.plot(LEGEND.ROT)
```

![Plot of CVs](./cv_datas_ex4_fig1.png)

## Select the average sweep and plot the data

```python
   LSVs = datas.get_sweep(AVG)
   LSVs.plot(LEGEND.ROT, savefig="cv_datas_ex3_fig2.png")
```

![Plot of CVs](./cv_datas_ex4_fig2.png)


## Levich Analysis

```python
   Epot = -0.5
   slopes = datas.Levich(Epot)
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_datas_ex4_fig3.png)

## Levich Analysis when normalizing the current to area


```python

   Epot = -0.5
   slopes = datas.Levich(Epot, AREA_CM)
   print(slopes[0] )
   print(slopes[1] )
```

![Plot of CVs](./cv_datas_ex4_fig4.png)
