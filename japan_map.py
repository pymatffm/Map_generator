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

class Japan_Map:
        def __init__(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):   
            self.plot_Japan_map(lat_array, lon_array, intersting_satellites, dphi, dlambda) 


           def plot_Japan_map(self, lat_array, lon_array, intersting_satellites, dphi, dlambda):
            #Japan boundary
            south, north = 32, 45
            west, east = 132.5, 151
            center = [(east+west)/2, (north+south)/2]
            
            m = Basemap(llcrnrlon=west, llcrnrlat=south, urcrnrlon=east, urcrnrlat=north,
                        resolution='h', area_thresh = 0.1, projection='tmerc', lat_ts=0,
                        lon_0=center[0], lat_0=center[1])
            
            # Plot features
            m.drawcoastlines()
            m.drawparallels(np.arange(-81., 81., 2),labels=[1,0,0,0], linewidth=0.0)    #-81., 81., 4
            m.drawmeridians(np.arange(-180., 181., 4),labels=[0,0,0,1], linewidth=0.0) #-180., 181., 10
            m.shadedrelief()               

            
            if 'iDerry_iMac' in self.pathList:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='r')
            else:
                m.readshapefile(r'<your_path>', name='PB2002_plates', drawbounds=False, color='orange')
            
            plate_names = []
            for plate_dict in m.PB2002_plates_info:
                plate_names.append(plate_dict['PlateName'])
            
            plates_of_interest = ['Okhotsk', 'Philippine Sea', 'Pacific', 'Eurasia', 'North America'] #Kermadec #Pacific #Australia
            for info, shape in zip(m.PB2002_plates_info, m.PB2002_plates): 
                if info['PlateName'] in plates_of_interest:
                    x, y = zip(*shape)
                    m.plot(x, y, marker=None, color='sandybrown')

            m.drawmapscale(146.3, 33.2, 145, 40, 500, barstyle='fancy', fontcolor='whitesmoke', fillcolor1='whitesmoke', fillcolor2='silver')

            earthquake_index_original = 973 # Japan MIZU=973/2772
        
            eq_longitude_values = []
            eq_latitude_values = []
            satellite_list = []
            
            start = [0, 0, 0, 0, 0, 0, 0, 0]
            end = [6480, 10800, 10800, 10800, 10080, 9360, 10800, 7200]
            
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
                prn = 'G%s' % d_replace
                satellite_list.append(prn)
                # Plot the points on the map
                plt.plot(x,y,'-', color='blue', zorder=7)
                print "plot_Japan_map: Track plotted for PRN{0}".format(intersting_satellites[i]+1)
        
            #Plotting exact points on the ground track where earthquake occurs 
            m.scatter(eq_longitude_values, eq_latitude_values, s=40, marker='*', color='r', zorder=10)
            for i, (x, y) in enumerate(zip(eq_longitude_values, eq_latitude_values), start=0):
                plt.annotate(str(satellite_list[i]), (x,y), xytext=(2, 2), textcoords='offset points', color='k', fontsize=9, zorder=9)
        
            # Plot points and text
            lons, lats = [142.372, 139.840, dlambda, 145.5, 133, 136.2, 138.9, 146.1, 139.0], [38.297, 35.653, dphi, 36.0, 39, 42, 43.5, 41.1, 33.3] 

            x, y = m(lons, lats)
            x_offsets = [26000, 20000]
            y_offsets = [-25000, 12000]
            m.scatter(x[1], y[1], s=60, marker='s', color='k') #For the capital square symbol for Tokyo
            m.scatter(x[2], y[2], s=100, marker='^', color='k')
            plt.text(x[2] +x_offsets[1], y[2] +y_offsets[1], 'mizu', style='italic', color='k', fontsize=15)
            plt.text(x[1] +x_offsets[1], y[1] +y_offsets[1], 'Tokyo', color='k', fontsize=15, zorder=3)
            plt.text(x[3], y[3], 'Pacific\n Ocean', style='italic', color='dodgerblue', fontsize=17, zorder=8)
            plt.text(x[4], y[4], 'Sea of\nJapan', style='italic', color='dodgerblue', fontsize=17, zorder=8)
            
            plt.text(x[5], y[5], 'Eurasian\n  Plate', fontsize=11)
            plt.text(x[6], y[6], 'North\nAmerican\nPlate', fontsize=11)
            plt.text(x[7], y[7], 'Pacific\n  Plate', fontsize=11)
            plt.text(x[8], y[8], 'Philippine\n Sea Plate', fontsize=10)
            
            #Beachball plotting
            ax = plt.gca()
            b = beach([193, 9, 78], facecolor='red', xy=(x[0], y[0]), width=70000, linewidth=1, alpha=0.85)
            b.set_zorder(10)
            ax.add_collection(b)
            
            if 'iMac' in self.pathList:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            else:
                plt.savefig(r'<your_path>', bbox_inches="tight")
            plt.close()
            print "Japan Map generated"
