---
title: Arguments
parent: Package
nav_order: 100
---

# Arguments

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



## For normalization of current

| Argument        | Meaning           | Where to use  |
| ------------- |:-------------| -----:|
| AREA | normalize to geometric area using m as unit| |
| AREA_CM | normalize to geometric area using cm as unit| |
| RATE | normalize to sweep rate| CV|



## For CV_Data, CV_Datas

| Argument        | Meaning           |
| ------------- |:-------------|
| POS | Select the positive sweep| 
| NEG | Select the negative sweep| 
| AVG | Select the average sweep<br>from positive and negative sweeps| 
| DIF | Select the difference <br>between the positive and negative sweeps| 


