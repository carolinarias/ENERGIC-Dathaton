#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
WEATHER UNDERGROUND AND TELECOM DATA PREPROCESSING

File name: preanova.py
Description: This script prepares the data fro the anova analisis in R.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 09/08/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
import pandas


data_path = #'your path'
#Importing data
#path: where you have your outgoin calls data
callsout = pandas.read_table(data_path,  sep = ',', names=['date_time','ts','cellid','calls_out'], header=0 )
callsout.drop(['date_time'],inplace=True,axis=1) 
#path: where you have your temperature data
temp = pandas.read_table(data_path, sep = ',', names=['index','cellid','name','ts','tmp'], header=0 )
#eliminating unnecessary columns
temp.drop(['index','name'],inplace=True,axis=1) 

#---------------------------------------------------#
# CREATING TEMPERATURE RANGES : high, medium, low
#---------------------------------------------------#
temp['tmp'].describe()
#you should obtain:
#count    7.205323e+06
#mean     4.989688e+00
#std      3.369172e+00
#min     -4.316667e+00
#25%               NaN
#50%               NaN
#75%               NaN
#max      1.534000e+01
#Name: tmp, dtype: float64
t_max = temp['tmp'].max()
t_min = temp['tmp'].min()
t_mean = temp['tmp'].mean()
t_std = temp['tmp'].std()
#high: max - second_limit; low: min -first_limit; medium: first_limit - second_limit
first_limit = t_mean - 2*t_std
second_limit = t_mean + 2*t_std

#Creating ranges
temp['t_levels'] = temp['tmp'].apply(lambda x: 'low' if t_min<x<first_limit else x)
temp['t_levels'] = temp['t_levels'].apply(lambda x: 'medium' if first_limit<x<second_limit else x)
temp['t_levels'] = temp['t_levels'].apply(lambda x: 'high' if second_limit<x<t_max else x)

#---------------------------------------------------#
# CREATING TYPE OF DAYS CATEGORY : weekend, workdays
#---------------------------------------------------#

#setting ts as date_time index
callsout['ts'] = pandas.to_datetime(callsout['ts'])
#creating a column with codes of weekdays weekday = [0,1,2,3,4]; weekends = [5,6]
callsout['weekday'] = pandas.DatetimeIndex(callsout['ts']).weekday
#callsout['weekday'] = callsout['ts'].dayofweek
#Creating ranges
callsout['d_type'] = callsout['weekday'].apply(lambda x: 'weekend' if x == 5 or x==6 else 'workdays')

#---------------------------------------------------#
# MERGING outgoing calls table and temperature table 
#---------------------------------------------------#
anovadata = pandas.merge(callsout, temp, right_index=True, left_index=True)
#anovadata = temp.merge(callsout, on=['ts'])
#anovadata = callsout.merge(temp, on=['ts'])
anovadata.drop(['cellid_y', 'ts_y','weekday','tmp'],inplace=True,axis=1) 
anovadata.to_csv(path_or_buf = data_path + 'anovadata.csv', sep=',')



print 'enjoy! bye'
