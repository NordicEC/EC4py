"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from __future__ import annotations


from .ec_setup import RHE,SHE,RATE,SQRT_RATE, AREA,AREA_CM,ROT,SQRT_ROT, MASS, LOADING
from .ec_setup import EC_Setup

__all__ = [

            "RHE","SHE",
            "RATE","SQRT_RATE", "AREA","AREA_CM","ROT","SQRT_ROT", "MASS", "LOADING"
            ,EC_Setup
           ]
