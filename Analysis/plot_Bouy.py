# -*- coding: utf-8 -*-
"""
TODO: Look for pickels
Plot wave data from NDBC
@author: Patrick
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
from scipy.signal import butter, lfilter, freqz
import airsea.windstress as ws
import NDBC_Bouy
pickled = True #Did you pickle an dataset already? If so True


montereyBayBouysIds =  {"MBARI_M1" : 46092,
                        "OffShore_wave" :46114,
                        "OffShore_ares" :46042,
                        "Canyon_wave" :46236,
                        "Hopkines_wave" : 46240,
                        }
bouy = montereyBayBouysIds['MBARI_M1']                        
                        
startDate = dt.datetime(2015,1,1)


if not(pickled):
    data = NDBC_Bouy.get_nc_dods(startDate,endDate=dt.datetime(2015,12,1),nbdcId=bouy)
    data.to_pickle("Data/" +str(bouy)+ "_from" + str(startDate.year))
else:
    data = pd.read_pickle('Data/46236_from2015')
    m1data = pd.read_pickle('Data/46092_from2015')
# Make datetime objects



dt_vect = np.vectorize(dt.datetime.fromtimestamp)

data['datetime'] = dt_vect(data.time[:])
data.index = data['datetime']

m1data['datetime'] = dt_vect(m1data.time[:])
m1data.index = m1data['datetime']

#

# Low pass filter the data with a buttersworth
# Based on http://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=12):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 1. / (1 * 3600)
cutoff = 1. /(3600 * 20)
order = 1
y = butter_lowpass_filter(m1data.wind_spd, cutoff, fs, order) #Return the data
#b, a = butter_lowpass(cutoff, fs, order)

# Get wind vectors
xUDir = []
yUDir = []

m1data['xSpeed'] = m1data.wind_spd * np.cos(np.deg2rad(m1data.wind_dir))
m1data['ySpeed'] = m1data.wind_spd * np.sin(np.deg2rad(m1data.wind_dir))

# Wind Stress
m1data['uWindStress'] = ws.stress(m1data.xSpeed, 10, drag='largepond', Ta=m1data.air_temperature)
m1data['vWindStress'] = ws.stress(m1data.ySpeed, 10, drag='largepond', Ta=m1data.air_temperature)
m1data['WindStress'] = ws.stress(m1data.wind_spd, 10, drag='largepond', Ta=m1data.air_temperature)

# plots
with plt.style.context(('ggplot')):
    
    fig, (ax0, ax1) = plt.subplots(2,1,sharex='all')
    fig.set_size_inches(14, 10)
    ax0.set_xlim([dt.date(2015,12,1),dt.date(2016,1,1)])
    
    ax0.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax0.xaxis.set_minor_locator(mdates.DayLocator())
    ax0.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

    #Sig Wave Height
    ax0.plot(data.datetime,data.wave_height,'-')
    ax0.set_ylim(0,6)
    ax0.set_ylabel("H$_s$, meters", fontsize= 12)
    ax0.text(ax0.get_xlim()[0]+1,ax0.get_ylim()[1]*.9,'CDIP - 156')
    
    # Wave Period
    ax1.plot(data.datetime,data.dominant_wpd,label='Dominant Period')
    ax1.plot(data.datetime,data.average_wpd,label='Average Period')
    ax1.set_ylim(0,30)
    ax1.set_ylabel("Wave Period, Sec.",fontsize= 12)
    ax1.text(ax1.get_xlim()[0]+1,ax1.get_ylim()[1]*.9,'CDIP - 156')
    ax1.legend()
    
    
    fig2, (ax2, ax3) = plt.subplots(2,1,sharex='all')
    fig2.set_size_inches(14, 10)
    ax2.set_xlim([dt.date(2015,12,1),dt.date(2016,1,1)])
    
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax2.xaxis.set_minor_locator(mdates.DayLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

    # Plot Wind Speed
    ax2.set_ylim(0,25)
    ax2.plot(m1data.datetime,m1data.wind_spd,label='Wind Speed')
    ax2.plot(m1data.datetime,y,label='20hr low pass filter')
    ax2.set_ylabel("Wind Speed\n(M/S)",fontsize= 12)
    ax2.legend()
    ax2.text(ax2.get_xlim()[0]+1,ax2.get_ylim()[1]*.9,'mbari - M1')
    # Plot SST
    
    ax3.plot(m1data.datetime,m1data.sea_surface_temperature,label='SST')
    ax3.plot(m1data.datetime,m1data.air_temperature,label='Air')
    ax3.set_ylabel("SST\n(C)",fontsize= 12)
    ax3.set_ylim(5,20)
    ax3.legend()
    ax3.text(ax3.get_xlim()[0]+1,ax3.get_ylim()[1]*.9,'mbari - M1')
    
    # Plot Wind Vectors
    fig3, (ax4,ax5) = plt.subplots(2,1,sharex='all')
    fig3.set_size_inches(14, 10)
    ax4.set_xlim([dt.date(2015,12,1),dt.date(2016,1,1)])
    ax4.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax4.xaxis.set_minor_locator(mdates.DayLocator())
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    
    ax4.plot(m1data.datetime,m1data.xSpeed,label='u')
    ax4.plot(m1data.datetime,m1data.ySpeed,label='v')
    ax4.legend()
    ax4.set_ylabel('Components of wind speed\n m/s')
    ax4.text(ax4.get_xlim()[0]+1,ax4.get_ylim()[1]*.8,'mbari - M1')
    
    ax5.plot(m1data.datetime,m1data.uWindStress,label='u - Tao')
    ax5.plot(m1data.datetime,m1data.vWindStress,label='v - Tao')
    ax5.legend()
    ax5.set_ylabel('Wind Stress\nN/m')
    ax5.text(ax5.get_xlim()[0]+1,ax5.get_ylim()[1]*.9,'mbari - M1')


