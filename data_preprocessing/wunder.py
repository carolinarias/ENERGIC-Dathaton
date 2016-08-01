#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
WEATHER UNDERGROUND DATA PREPROCESSING

File name: 
Description: This script takes the stations data coming from the weather underground API, makes some preprocessing 
and cleanning to finally map the data with the telecom Italia Milano GRID.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
import pandas
import matplotlib.pyplot as plt
import numpy
import scipy
import csv, numpy, time
import os
import glob
from fitter import Fitter
from scipy import stats

#------------------------------#
# glosary
#------------------------------#

#st1: ILOMBARD131, 1512 records
#st2: ILOMBARD204, 1512 records
#st3:LOMBARD208, 1512 records
#st4: ILOMBARD245, 336 records
#st5: ILOMBARD38, 1512 records
#st6: ILOMBARD77, 1512 records
#st7: IMILANOM4, 1512 records
#st8: IMILANOM7, 1512 records
#st9: IMILANOR2, 1512 records
#st10: IMONZABR2, 1512 records
#rawdata:original data from weather underground


#------------------------------#
# DATA PREPROCESSING
#------------------------------#

#path to original csv files
data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/wundermap/nov_dic_2013/csv/'
#path for csv files aggregated by hour
data_path_aggregated = data_path + 'aggregated/'
data_path_nov = data_path_aggregated + 'Nov/'
data_path_dic = data_path_aggregated + 'Dic/'
#path for final big csv file
data_path_out = data_path + 'out/'
data_files = glob.glob(data_path + '*.csv')

if not os.path.exists(data_path_aggregated):
    os.makedirs(data_path_aggregated)
    
if not os.path.exists(data_path_out):
    os.makedirs(data_path_out)

#December
for data_file in data_files:
        
    with open(data_file, 'rb') as data_file:
         
        #converting csv file into a dataframe          
        rawdata = pandas.read_table(data_file, sep=',', names=['lat','lng','name','ts','tmp','hum','prec','heat'], header=0) 
        #leaving only the columns of interest
        rawdata.drop(['lat','lng','hum','heat'],inplace=True,axis=1)           
        #extracting the station name from the data, it is useful to name the output csv files 
        stationcolumn = rawdata['name']
        stationname = stationcolumn[1]
        #Data Cleaning: eliminating the extrange values -573, and others from data
        rawdata.loc[rawdata['tmp'] < -20, 'tmp'] = numpy.nan
        #Data Cleaning: eliminating the negative values of precipitation from data
        rawdata.loc[rawdata['prec'] < 0, 'prec'] = numpy.nan
        # set the datetime as index
        rawdata = rawdata.set_index(pandas.DatetimeIndex(rawdata['ts'])) 
        # calculate the mean value of all variables each hour
        stationdata = rawdata.resample('H').mean()
        # adding the station name column to the data: after resample, this column is eliminated
        stationdata['name'] = stationname
        #extracting data of December
        stationdata = stationdata.ix['2013-12']
        # saving the aggregated new csv files
        stationdata.to_csv(path_or_buf = data_path_dic + stationname + '_dic.csv', sep=',')

            
# merging all created csv into one csv (data_dic.csv) for December
with open(data_path_out + 'data_dic.csv', 'a') as out_file:
    for csv_file in glob.glob(data_path_dic + '*.csv'):
        line_num = 0
        for line in open(csv_file, 'r'):
            if line_num is 0:
                print 'Skipping header'
            else:
                out_file.write(line)
            line_num = line_num + 1
        print line_num
    
#------------------------------#
# DATA MAPPING INTO MILANO GRID
#------------------------------#
# importing the table that relates cell id from milano grid to the stations data
cellid = pandas.read_table('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/wundermap/nov_dic_2013/cellid_wunder2013stations.csv',sep=',', names=['cellid','latcellid','longcellid','latst','longst','name'], header=0 )
# importing the data
data = pandas.read_table(data_path_out + 'data_dic.csv', sep=',', names=['ts','tmp','prec','name'], header=0)
# merging the two data frames
datamerged = cellid.merge(data, on='name')
# leave just 
datamerged.drop(['prec','latcellid','longcellid','latst','longst'],inplace=True,axis=1) 
# save merged data into a csv          
datamerged.to_csv(path_or_buf = data_path_out + 'datamerged_dic.csv', sep=',')


#------------------------------#
# DATA SUBSETTING BY TIME
#------------------------------#
# set the timestamp as index
datamerged = datamerged.set_index(pandas.DatetimeIndex(datamerged['ts']))#it takes at least 30 min to execute
datamerged_1ts = datamerged.ix['2013-12-31 23:00:00']



#------------------------------#
# STATISTICS
#------------------------------#

stats = datamerged.describe()
stats.to_csv(path_or_buf = data_path_aggregated + 'datamergedstats.csv', sep=',')
lineplot = datamerged['tmp'].plot(kind='scatter',logy=False, figsize=(20,5))
histplot = datamerged['tmp'].plot(kind='hist',logy=False, figsize=(20,5))
boxplot = datamerged['tmp'].plot(kind='box',logy=False, figsize=(20,5))

