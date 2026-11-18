"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from __future__ import annotations

from .ec_data import EC_Data
from .ec_datas import EC_Datas
from ..ec_setup.ec_setup import RHE,SHE,RATE,SQRT_RATE, AREA,AREA_CM,ROT,SQRT_ROT, MASS, LOADING


__all__ = [
            "EC_Data","EC_Datas",
            "RHE","SHE",
            "RATE","SQRT_RATE", "AREA","AREA_CM","ROT","SQRT_ROT", "MASS", "LOADING"
           ]
