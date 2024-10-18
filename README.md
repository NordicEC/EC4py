The intention
---------------
This is a package to treat electrochemical data in order to extract key values such as ECSA and Tafel slopes. Specifically, its aim is to make the data analysis as quick and easy as possible. 

#  EC4py Docs
    https://nordicec.github.io/EC4py/
# Using EC4py

Get the stable version of EC4py from the Python package index with

```bash
pip install EC4py
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
    ** Plot

*   Treats cyclic voltammetry(CV) data:
    * subtraction, addition
    * back ground subtraction 
    * Levich analysis
    * Koutechy-Levich analysis

