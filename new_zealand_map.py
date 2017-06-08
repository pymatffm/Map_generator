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

class New_Zealand_Map:
        def __init__(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):   
            self.plot_NZ_map(lat_array, lon_array, intersting_satellites, dphi, dlambda) 


           def plot_NZ_map(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):
            # Set map boundaries
            south, north = -48, -34
            west, east = 165, 179
            center = [(east+west)/2, (north+south)/2]
            
            m = Basemap(llcrnrlon=west, llcrnrlat=south, urcrnrlon=east, urcrnrlat=north,
                        resolution='c', area_thresh = 0.1, projection='tmerc', lat_ts=0,
                        lon_0=center[0], lat_0=center[1]) 
            
            # Plot features
            m.drawparallels(np.arange(-81., 81., 2),labels=[1,0,0,0], linewidth=0.0)    #-81., 81., 4
            m.drawmeridians(np.arange(-180., 181., 4),labels=[0,0,0,1], linewidth=0.0) #-180., 181., 10
            m.shadedrelief()
            
            if 'iMac' in self.pathList:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='r')
            else:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='r')
            
            
            plate_names = []
            for plate_dict in m.PB2002_plates_info:
                plate_names.append(plate_dict['PlateName'])
    
            print plate_names
            plates_of_interest = ['Pacific'] #Kermadec #Pacific #Australia
            for info, shape in zip(m.PB2002_plates_info, m.PB2002_plates): 
                if info['PlateName'] in plates_of_interest:
                    x, y = zip(*shape)
                    m.plot(x, y, marker=None, color='r')

            m.drawmapscale(176.5, -47.2, 174, -41, 500, barstyle='fancy', fontcolor='whitesmoke', fillcolor1='whitesmoke', fillcolor2='silver')

            earthquake_index_original = 1324 # Kaikoura EQ at 11:02 UT
            # Plot ground tracks
        
            eq_longitude_values = []
            eq_latitude_values = []
            satellite_list = []
            
            start = [1224, 1220]
            end = [1440, 1440]
            
            
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
                print "plot_NZ_map: Track plotted for PRN{0}".format(intersting_satellites[i]+1)
        
            #Plotting exact points on the ground track where earthquake occurs 
            m.scatter(eq_longitude_values, eq_latitude_values, s=40, marker='*', color='r', zorder=10)
            for i, (x, y) in enumerate(zip(eq_longitude_values, eq_latitude_values), start=0):
                plt.annotate(str(satellite_list[i]), (x,y), xytext=(2, 2), textcoords='offset points', color='k', fontsize=9, zorder=9) #whitesmoke
        
            # Plot points and text
            lons, lats = [170.9843, 174.8058, 173.4336, 173.5336, 172.2664, 171.8062, 174.8343, 171.5753, 174.7633, 168, 173.5, 173.077], \
                        [-42.7129, -41.3233, -41.1836, -42.4256, -42.7833, -41.7447, -36.6028, -43.5914, -36.8485, -38, -46, -42.757] 
                        
            gnss_sites = ['hoik', 'wgtn', 'nlsn', 'kaik', 'lkta', 'west', 'auck', 'meth']

            x, y = m(lons, lats)
            x_offsets = [-135000, 20000, -125000, 20000, 2000, -143000, -145000, -154000]
            y_offsets = [12000, 10000, 12000, 10000, -80000, 12000, 12000, 12000]
            
            for gnss_stn in range(len(gnss_sites)):
                m.scatter(x[gnss_stn], y[gnss_stn], s=100, marker='^', color='k', zorder=4)
                plt.text(x[gnss_stn] +x_offsets[gnss_stn], y[gnss_stn] +y_offsets[gnss_stn], gnss_sites[gnss_stn], style='italic', color='k', fontsize=13)
            
            m.scatter(x[8], y[8], s=50, marker='o', color='k', zorder=3) 
            plt.text(x[8] +x_offsets[1], y[8] +y_offsets[1], 'Auckland', color='k', fontsize=15, zorder=3)
            plt.text(x[9], y[9], 'Tasman\n   Sea', style='italic', color='dodgerblue', fontsize=17, zorder=8)
            plt.text(x[10], y[10], 'South Pacific\n    Ocean', style='italic', color='dodgerblue', fontsize=17, zorder=8)

            ax = plt.gca()
            b = beach([354, 61, 64], facecolor='y', xy=(x[11], y[11]), width=70000, linewidth=1, alpha=0.85)
            
            b.set_zorder(10)
            ax.add_collection(b)
            #plt.show()
        
            if 'iDerry_iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "New Zealand Map generated"
        
        