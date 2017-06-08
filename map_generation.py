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
import ionospheric_pierce_point
import new_zealand_map
import japan_map
import south_scotia_map
import north_scotia_map
from mpl_toolkits.basemap import Basemap
from obspy.imaging.mopad_wrapper import beach

'''
This suite of classes produces:
1. Maps with projected satellite tracks according to the their locations at the Ionospheric Pierce Point (IPP)
2. Random maps to deomonstrate different map type projections.

The Station/Receiver position: dphi, dlambda
'''
class Basemap_Map:
        def __init__(self, dphi, dlambda, elevation_array, azimuth_array):   
            workspacePath = os.getcwd()
            self.pathList = workspacePath.split(os.sep)

            # These maps utilise IPPs in order to visualise projected satellite tracks.
            ### If not required then simply comment out. ###
            ipp = ionospheric_pierce_point.Ionospheric_Pierce_Point(dphi, dlambda, elevation_array, azimuth_array)
            lat_array = ipp.lat_array
            lon_array = ipp.lon_array

            new_zealand_map.New_Zealand_Map(lat_array, lon_array, intersting_satellites, dphi, dlambda)
            japan_map.Japan_Map(lat_array, lon_array, intersting_satellites, dphi, dlambda)
            south_scotia_map.plot_SSRT_map(lat_array, lon_array, intersting_satellites, dphi, dlambda)        
            north_scotia_map.NSRT_Map(lat_array, lon_array, intersting_satellites, dphi, dlambda) 
            ################################################
        
            self.plot_ortho_map(dphi, dlambda)
            self.plot_mercator_Japan_map(dphi, dlambda)
            self.funky_earth_plot(dphi, dlambda)


        def plot_ortho_map(self, dphi, dlambda):
            # lon_0, lat_0 are the center point of the projection.
            # resolution = 'l' means use low resolution coastlines.
            m = Basemap(projection='ortho', lon_0=dlambda, lat_0=dphi, resolution='l')
            lons, lats = [dlambda, 142.372], [dphi, 38.297]
            x, y = m(lons, lats)
            x_offsets = [30000]
            y_offsets = [-12000]
            m.scatter(x[1], y[1], s=100, marker='*', color='r', zorder=1)
            
            m.drawmapboundary(fill_color='cornflowerblue')
            m.drawcountries()
            m.fillcontinents(color='white',lake_color='cornflowerblue', zorder=0)
            m.drawcoastlines()
            m.drawparallels(np.arange(-90.,120.,30.))
            m.drawmeridians(np.arange(0.,420.,60.))
            
            if 'iDerry_iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "Orthographic map created."

            
            
        def plot_mercator_Japan_map(self, dphi, dlambda):
            # KEPA surroundings transverse mercator
            m = Basemap(llcrnrlon=132,llcrnrlat=32,urcrnrlon=150,urcrnrlat=46,
                        resolution='i',projection='tmerc',lon_0=141,lat_0=39)
            
            # Plot points and text
            lons, lats = [142.372, 139.840, dlambda, 142, 134], [38.297, 35.653, dphi, 33.5, 40]
            x, y = m(lons, lats)
            x_offsets = [26000, 20000]
            y_offsets = [-25000, 12000]
            m.scatter(x[0], y[0], s=100, marker='*', color='r')
            m.scatter(x[1], y[1], s=60, marker='s', color='k')
            m.scatter(x[2], y[2], s=100, marker='^', color='k')
            plt.text(x[1] +x_offsets[0], y[1] +y_offsets[0], 'Tokyo', fontsize=16)
            plt.text(x[2] +x_offsets[1], y[2] +y_offsets[1], 'mizu', style='italic', fontsize=16)
            plt.text(x[3], y[3], 'Pacific Ocean', style='italic', fontsize=15)
            plt.text(x[4], y[4], 'Sea of\nJapan', style='italic', fontsize=15)
            
            m.drawmapboundary(fill_color='cornflowerblue')
            m.drawcountries()
            m.fillcontinents(color='white',lake_color='cornflowerblue', zorder=0)
            m.drawcoastlines()
            m.drawparallels(np.arange(130,160,5.))
            m.drawmeridians(np.arange(30.,45,10.))

            if 'iDerry_iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "Mercator MIZU map created."


        def funky_earth_plot(self, dphi, dlambda):
            map = Basemap(resolution='l',
                satellite_height=3000000.,
                projection='nsper',
                lat_0 = 28., lon_0 = 117., 
                llcrnrx=500000.,llcrnry=500000.,
                urcrnrx=2700000.,
                urcrnry=2700000.
                )
                
            map.drawmapboundary(fill_color='cornflowerblue')
            map.drawcountries()
            map.fillcontinents(color='darkseagreen',lake_color='steelblue', zorder=0) 
            map.drawcoastlines()
            #map.bluemarble()
            
            # Plot point(s)
            lons, lats = [142.372, 139.840, 141.076, 141, 132], [38.297, 35.653, 39.080, 33, 40]
            x, y = map(lons, lats)
            x_offsets = [24000, 30000, 20000]
            y_offsets = [-14000, -18000, 10000]
            map.scatter(x[0], y[0], s=100, marker='*', color='r', zorder=1)
            map.scatter(x[1], y[1], s=60, marker='s', color='k', zorder=1)
            map.scatter(x[2], y[2], s=60, marker='^', color='k', zorder=1)
            plt.text(x[1] +x_offsets[1], y[1] +y_offsets[1], 'Tokyo', fontsize=14)
            plt.text(x[2] +x_offsets[2], y[2] +y_offsets[2], 'mizu', style='italic', fontsize=14)
            plt.text(x[3], y[3], 'Pacific Ocean', style='italic', fontsize=15)
            plt.text(x[4], y[4], 'Sea of\nJapan', style='italic', fontsize=15)
            
            self.clear_frame(None)
            
            if 'iDerry_iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "Funky Earth Map generated"





