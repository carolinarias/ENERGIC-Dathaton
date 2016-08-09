#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
TELECOM DATA PREPROCESSING AND EXPLORATION

File name: exploration.py 
Description: This script makes data exploration for telecom Open data 2013.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""

import pandas
import numpy
import scipy
from scipy import stats


data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/wundermap/nov_dic_2013/csv/'

#Importing data
callsout = pandas.read_table('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/ts_cellid_variable/calls_out.txt', names=['date_time','cellid','calls_out'], header=None )

# Setting date_time as data frame index
callsout = callsout.sort(columns='date_time', axis=0, ascending=True)
callsout = callsout.reset_index(drop=True)

#-date time index
rng = pandas.date_range(start='2013-10-31 23:00:00', periods=1488, freq='H')
#some info on the data
callsout.info()

#creating temporal indexes
callsout = callsout.set_index(pandas.DatetimeIndex(callsout['date_time']))

#------------------------------#
# STATISTICS AND PLOTS
#------------------------------#
statistics = callsout.describe()
stats.to_csv(path_or_buf = data_path + 'datamergedstats.csv', sep=',')
lineplot = callsout['calls_out'].plot(kind='density',logy=False, figsize=(20,5))
histplot = callsout['calls_out'].plot(kind='hist',logy=False, figsize=(20,5))
#histplot2 = callsout.hist('calls_out', bins=500, figsize=(20,5))
boxplot = callsout['calls_out'].plot(kind='box',logy=False, figsize=(20,5))
histplot = callsout['calls_out'].plot(kind='line',logy=False, figsize=(20,5))

#------------------------------#
# NORMALIZING DATA
#------------------------------#

#setting values cero to NAN 
callsout = callsout.replace(0, 0.1)
calloutlog = callsout['callsout']
#callsout = callsout.replace(0, numpy.nan)

#-Transforming data into log 
callsout['calls_out']= numpy.log(callsout['calls_out'])

#Normality test
#histogram to check normality
histplot = callsout.plot(kind='hist',logy=False, figsize=(20,5))
#boxplot to check for outliers
boxplot = callsout.plot(kind='box',logy=False, figsize=(20,5))

scipy.stats.normaltest(callsout, axis=0)
#NormaltestResult(statistic=803869.62940951809, pvalue=0.0)
scipy.stats.shapiro(callsout, a=None, reta=False)
#(0.9956305623054504, 0.0)
scipy.stats.anderson(callsout, dist='norm')
#AndersonResult(statistic=87569.946015860885, critical_values=array([ 0.576,  0.656,  0.787,  0.918,  1.092]), significance_level=array([ 15. ,  10. ,   5. ,   2.5,   1. ]))
#AndersonResult(statistic=0.27488219365477562, critical_values=array([ 0.576,  0.656,  0.787,  0.918,  1.092]), significance_level=array([ 15. ,  10. ,   5. ,   2.5,   1. ]))
scipy.stats.t.fit(callsout)

callsout.to_csv(path_or_buf = data_path + 'callout_normal_dic.csv', sep=',')

print 'enjoy! bye'
