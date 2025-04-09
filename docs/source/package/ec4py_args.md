---
title: Arguments
parent: Package
nav_order: 100
---

# Arguments

EC4py defines some global string constants, that can be used as arguments to functions to adjust their behavior.  

These string constants can be imported:

```python
   from ec4py import *
```
Here below follows all the string constants and their meaning when used as an argument to a function.

## For adjusting the reference electrode

| Argument        | Meaning           | Where to use  |
| ------------- |:-------------| -----:|
| RHE | express potential relative the RHE potential| |
| SHE | express potential relative the SHE potential| |


## For normalization of current

| Argument        | Meaning           | Where to use  |
| ------------- |:-------------| -----:|
| AREA | normalize to geometric area using m as unit| |
| AREA_CM | normalize to geometric area using cm as unit| |
| RATE | normalize to sweep rate| CV|
| SQRT_RATE | normalize to the square root of sweep rate| CV|
| ROT | normalize to rotations rate| |
| SQRT_ROT | normalize to square root of the rotations rate||




## For plotting, LEGEND

| Argument        | Meaning for the legend of a graph     |
| ------------- |:-------------|
| LEGEND.NONE  |  removes legend | 
| LEGEND.NAME  | the name of the file|
| LEGEND.RATE  | sweep rate| 
| LEGEND.AREA  | geometric area |
| LEGEND.ROT  |  rotation rate | 
| LEGEND.DATE  |  date |
| LEGEND.DATE  |  time |
| LEGEND.VSTART  |  Start potential of a CV |
| LEGEND.V1  |  First vertex of a CV sweep |
| LEGEND.V2  |  Second vertex of a CV sweep |
| LEGEND.MWE_CH  |  Multi-working electrode channel |


## For CV_Data, CV_Datas

| Argument        | Meaning           |
| ------------- |:-------------|
| POS | Select the positive sweep| 
| NEG | Select the negative sweep| 
| AVG | Select the average sweep<br>from positive and negative sweeps| 
| DIF | Select the difference <br>between the positive and negative sweeps| 


