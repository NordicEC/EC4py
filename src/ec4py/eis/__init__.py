"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from __future__ import annotations

from .eis_data import EIS_Data
from .eis_datas import EIS_Datas

__all__ = [
           "EIS_Data","EIS_Datas",
           ]
