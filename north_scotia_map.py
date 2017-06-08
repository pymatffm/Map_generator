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

class NSRT_Map:
        def __init__(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):   
            self.plot_NSRT_map(lat_array, lon_array, intersting_satellites, dphi, dlambda) 


         def plot_NSRT_map(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):
            # Set map boundaries
            south, north = -67, -50
            west, east = -52, -25
            center = [(east+west)/2, (north+south)/2]
            
            m = Basemap(llcrnrlon=west, llcrnrlat=south, urcrnrlon=east, urcrnrlat=north,
                        resolution='h', area_thresh = 0.1, projection='tmerc', lat_ts=0,
                        lon_0=center[0], lat_0=center[1]) 
            
            # Plot features
            m.drawcoastlines()
            m.drawparallels(np.arange(-81., 81., 4),labels=[1,0,0,0], linewidth=0.0)  
            m.drawmeridians(np.arange(-180., 181., 10),labels=[0,0,0,1], linewidth=0.0)
            m.shadedrelief()
            
            
            if 'iDerry_iMac' in self.pathList:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='r')
            else:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='r')
            
            plate_names = []
            for plate_dict in m.PB2002_plates_info:
                plate_names.append(plate_dict['PlateName'])
            
            plates_of_interest = ['Scotia', 'Sandwich', 'Antarctica'] #South America #Antartica
            for info, shape in zip(m.PB2002_plates_info, m.PB2002_plates): 
                if info['PlateName'] in plates_of_interest:
                    x, y = zip(*shape)
                    m.plot(x, y, marker=None, color='sandybrown')
            
            
            m.drawmapscale(-45.0, -66.2, center[0], center[1], 500, barstyle='fancy',  fontcolor='whitesmoke', fillcolor1='whitesmoke', fillcolor2='silver')
           
            earthquake_index_original = 5542 # SSRT EQ at 9:04 UT
            # Plot ground tracks
        
            eq_longitude_values = []
            eq_latitude_values = []
            satellite_list = []
            
            start = [0, 3960, 5480, 1440]
            end = [10800, 10800, 10800, 10800]
            
            
            for i in range(len(intersting_satellites)):
                spec_sv_lam = lon_array[: ,i]
                spec_sv_phi = lat_array[: ,i]
                
                #Code added here to splice arrays depending on when the satellites were tracked. Use VTEC plots (time axes) for reference
                spec_sv_lam = spec_sv_lam[start[i]:end[i]]
                spec_sv_phi = spec_sv_phi[start[i]:end[i]]    
                  
                # Find index of EQ once the splice has happened:
                earthquake_index = earthquake_index_original - start[i]
                #earthquake_index = 973
                
                track_len = len(spec_sv_lam)
                
                earthquake_long = spec_sv_lam[earthquake_index]
                earthquake_lat = spec_sv_phi[earthquake_index]
                
                longitude_values = []
                latitude_values = []
                for j in range(track_len):
                    latitude = spec_sv_phi[j]
                    longitude = spec_sv_lam[j]
                    latitude_values.append(latitude)
                    longitude_values.append(longitude)
                # Convert latitude and longitude to coordinates X and Y
                x, y = m(longitude_values, latitude_values)
                x_eq, y_eq = m(earthquake_long, earthquake_lat)
                eq_longitude_values.append(x_eq)
                eq_latitude_values.append(y_eq)
        
                d = intersting_satellites[i] +1
                d_replace = str(d).zfill(2)
                prn = 'E%s' % d_replace
                satellite_list.append(prn)
                # Plot the points on the map
                plt.plot(x,y,'-', color='b', zorder=7) #burlywood
                print "plot_NSRT_map: Track plotted for PRN{0}".format(intersting_satellites[i]+1)
        
            #Plotting exact points on the ground track where earthquake occurs 
            m.scatter(eq_longitude_values, eq_latitude_values, s=40, marker='*', color='r', zorder=10)
            for i, (x, y) in enumerate(zip(eq_longitude_values, eq_latitude_values), start=0):
                plt.annotate(str(satellite_list[i]), (x,y), xytext=(2, 2), textcoords='offset points', color='k', fontsize=9, zorder=9) #whitesmoke
     
            # Plot points and text
            lons, lats =  [-31.877, dlambda, -42.5, -32.2, -31.9, -29.7, -33.6], [-55.285, dphi, -58.8, -62.2, -54.5, -58.2, -58.0]# KRSA/KEPA

            x, y = m(lons, lats)
            x_offsets = [26000, 20000]
            y_offsets = [-25000, 12000]
            
            m.scatter(x[1], y[1], s=100, marker='^', color='k')
            plt.text(x[2], y[2], 'Scotia Sea', style='italic', fontsize=17)
            plt.text(x[1] +x_offsets[1], y[1] +y_offsets[1], 'krsa', style='italic', color='k', fontsize=15)
            plt.text(x[3], y[3], 'Antarctic\n  Plate', fontsize=11)
            plt.text(x[4], y[4], 'South America\n      Plate', fontsize=11)
            plt.text(x[5], y[5], 'Sandwich\n  Plate', fontsize=11)
            plt.text(x[6], y[6], 'Scotia\n  Plate', fontsize=11)
            
            ax = plt.gca()
            b = beach([301, 62, 84], facecolor='orange', xy=(x[0], y[0]), width=70000, linewidth=1, alpha=0.85)
            b.set_zorder(10)
            ax.add_collection(b)
            #plt.show()
        
            if 'iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "NSRT map created."