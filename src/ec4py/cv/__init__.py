"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from __future__ import annotations

from .cv_data import CV_Data
from .cv_datas import CV_Datas

__all__ = [
           "CV_Data","CV_Datas",
           ]
