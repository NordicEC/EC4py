The intention
---------------
This is a package to be used to treat electrochemical data in order to extract key values such as ECSA and Tafel slopes. Specifically, its aim is to make the data analysis as quick, transparemt and easy as possible. 

#  EC4py Docs
The documentation can be found here:
    [https://nordicec.github.io/EC4py](https://nordicec.github.io/EC4py/)
    
# Using EC4py

Get the stable version of EC4py from the Python package index with

```bash
python -m pip install EC4py --upgrade
```
or in a jupyter notebook
```jupyther
%pip install EC4py --upgrade
```




A simple example
---------------
.. code:: python
    
    from EC4py import EC_Data

    data = EC_Data("FILE PATH")
    data.plot("E","i")

Features
--------

* Read TDMS files.
    * Plot

*   Treats cyclic voltammetry(CV) data:
    * subtraction, addition
    * back ground subtraction 
    * Levich analysis
    * Koutechy-Levich analysis

