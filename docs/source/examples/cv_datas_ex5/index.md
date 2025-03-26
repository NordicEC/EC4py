---
title: Example 5 - Rate Analysis using of CVs
parent: CV_Datas
grand_parent: Examples
---
# Example 5: class CV_Datas and LSV_Datas - RATE Analysis

The aim is to extract the capacitance from the surface.

## Download dataset


Start by downloading the files in the folder from github:
   [Folder](https://github.com/nordicec/EC4py/blob/d3e8f22b518bb23777ccfd42bf2175177df4b272/test_data/CV/Pt_vs_rate)

and save it an appropriate folder.

## Import the class:

```python
   from ec4py import CV_Data
```
## Load a file:



```python
   paths =[x for x in dirPath.glob("CV_*.tdms")]
   #load in the files
   datas = CV_Datas(paths)
```

## Show the raw data

```python
   datas.plot(LEGEND.RATE)
```

![Plot of CVs](./cv_datas_ex5_fig1.png)

## Rate Analysis
Analyse the current at a specific voltage using the RHE-potential.
```python
   datas.RateAnalysis(0.5,RHE)
```

![Rate Analysis](./cv_datas_ex5_fig2.png)




## Observe the offset
It can be seen in the graph above that the there is an offset in the data. The current offset can be visualized by plotting the average of the positive and negative scan.

```python
   datas.plot(AVG,RHE,RATE,LEGEND.RATE)
```

![Plot of CVs](./cv_datas_ex5_fig3.png)

## Rate Analysis of the difference
A technique to remove any offset is to take the difference between positive and negative scan(DIF). 

```python

datas.RateAnalysis(0.45,RHE,DIF,savefig="cv_datas_ex5_fig4.png")
```

![Plot of CVs](./cv_datas_ex5_fig4.png)
