# -*- coding: utf-8 -*-
"""
TODO:
    Deal with masked arrays / empty data


@author: Patrick
"""
import netCDF4 as nc
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pylab as plt

def get_nc_dods(startDate,nbdcId=46092,endDate=dt.datetime.now(),save=False):
    ''' Retreive netcdf files from the dods thredds server
    
    Args:
        nbdcId (int): The id of the ndbc bouy, defaults to 46092, the MBARI M1 
            bouy
        startDate (datetime object): The start date value. Defaults to None.
        endDate (datetime object): The end date value. Defaults to now. Maybe
            dangerous, due to long records
        save (boolean): If True save a .nc locally. ADD THIS LATER
    Returns:
        pandas dataframe: True if successful, False otherwise.


    Raises:
        AttributeError: Need some sort of error or when can't retrieve a file
            from server. DEAL WITH LATER
    '''   
    print "Running get_nc_dods"
    yearList = yearsArray(startDate.year,endDate.year)
    for ix, year in enumerate(yearList):
        url = buildQueryString(year,nbdcId)
        data = nc.Dataset(url)
        #Create a pandas dataframe
        if ix == 0:
            df = pd.DataFrame(columns=data.variables.keys())
            for col in df.columns:
                tempData = data[col]
                # fill shorter data
                if tempData.shape == (1,):
                    colsize = df[df.columns[0]].shape[0] # tuple of the dimensions of the variable data
                    df[col] = tempData[0].repeat(colsize)
                else:
                    df[col] = tempData[:].flatten()
        else:
            tempdf = pd.DataFrame(columns=data.variables.keys())
            for col in tempdf.columns:
                tempData = data[col]
                # fill shorter data
                if tempData.shape == (1,):
                    colsize = tempdf[tempdf.columns[0]].shape[0] # tuple of the dimensions of the variable data
                    tempdf[col] = tempData[0].repeat(colsize)
                else:
                    tempdf[col] = tempData[:].flatten()
            df = df + tempdf
    return df, data

def yearsArray(startYear,endYear):
    #Return a array of years between the start and end years
    numYears = endYear - startYear + 1
    return np.linspace(startYear,endYear,numYears)
    
def buildQueryString(year,nbdcId):
    #Return URL string that points to the correct .nc file
    return "http://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/" + str(nbdcId) + "/" + str(nbdcId) +"h" + str(int(year))  +".nc"

montereyBayBouysIds =  {"MBARI_M1" : 46092,
                    "OffShore_wave" :46114,
                    "OffShore_ares" :46042,
                    "Canyon_wave" :46236,
                    "Hopkines_wave" : 46240,
                    }
bouy = montereyBayBouysIds['MBARI_M1']                        
startDate = dt.datetime(2015,1,1)
data, netData = get_nc_dods(startDate,endDate=dt.datetime(2015,12,1),nbdcId=bouy)

