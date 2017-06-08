#!/usr/bin/env python
#*-* coding: utf-8 *-*
from __builtin__ import file
import os.path
import sys
import datetime
import math
import pandas as pd
import numpy as np
import scipy as sp
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import constants as cs
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from obspy.imaging.mopad_wrapper import beach

class Ionospheric_Pierce_Point:
        def __init__(self, dphi, dlambda, elevation_array, azimuth_array):   
            ele_shape = elevation_array.shape
            epoch_length = ele_shape[0]

            ### MANUALLY SET. Should be PRN number MINUS 1 ###
            intersting_satellites = [7,21]
            ##################################################

            self.lat_array, self.lon_array = self.loop_through_points(epoch_length, intersting_satellites) 


        def loop_through_points(self, epoch_length, intersting_satellites)
            intersting_satellites_len = len(intersting_satellites)
            lat_array = np.empty((epoch_length, intersting_satellites_len), dtype=np.float64) * np.NaN
            lon_array = np.empty((epoch_length, intersting_satellites_len), dtype=np.float64) * np.NaN
            
            for i in range(len(intersting_satellites)):
                ele_series = elevation_array[:, intersting_satellites[i]]
                azi_series = azimuth_array[:, intersting_satellites[i]]
                for j in range(epoch_length):
                    print "MODULE map_generation.py   i: {0}, j: {1}".format(i, j)
                    ele = ele_series[j]
                    azi = azi_series[j]
                    lat_pp_deg, long_pp_deg = self.ionospheric_pierce_point(dphi, dlambda, ele, azi)
                    lat_array[j, i] = lat_pp_deg
                    lon_array[j, i] = long_pp_deg

            return lat_array, lon_array
           

        # Referenced from https://www.easa.europa.eu/system/files/dfu/ETSO.Dev_.C145_5_v11.pdf
        def ionospheric_pierce_point(self, dphi, dlambda, ele, azi):
            Re = 6378136.3 # Earth ellipsoid in meters
            h = cs.SHELL_HEIGHT * 10**3 # Height of pierce point meters, and where maximum electron density is assumed
            coeff = Re / (Re + h)
            lat_rx = dphi
            long_rx = dlambda
            
            # Degrees to radians conversions
            ele_rad = np.deg2rad(ele)
            azi_rad = np.deg2rad(azi)
            lat_rx_rad = np.deg2rad(lat_rx)
            long_rx_rad = np.deg2rad(long_rx)
            
            psi_pp = (np.pi / 2) - ele_rad - np.arcsin(coeff * np.cos(ele_rad)) # Earth central angle between user and the Eart projection of the pierce point, in radians
            psi_pp_deg = np.rad2deg(psi_pp)
            lat_pp = np.arcsin(np.sin(lat_rx_rad)*np.cos(psi_pp) +
            np.cos(lat_rx_rad)*np.sin(psi_pp)*np.cos(azi_rad)) # in radians
            
            if (lat_rx > 70 and ((np.tan(psi_pp)*np.cos(azi_rad)) > np.tan((np.pi/2) - lat_rx_rad))) or (lat_rx < -70 and ((np.tan(psi_pp)*np.cos(azi_rad + np.pi)) > np.tan((np.pi/2) + lat_rx_rad))):
                long_pp = long_rx_rad + np.pi - np.arcsin((np.sin(psi_pp)*np.sin(azi_rad)) / np.cos(lat_pp))
            else:
                long_pp = long_rx_rad + np.arcsin((np.sin(psi_pp)*np.sin(azi_rad)) / np.cos(lat_pp))
            
            lat_pp_deg = np.rad2deg(lat_pp)
            long_pp_deg = np.rad2deg(long_pp)

            return lat_pp_deg, long_pp_deg
        
        