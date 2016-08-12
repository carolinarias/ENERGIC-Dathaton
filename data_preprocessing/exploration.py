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
import matplotlib
matplotlib.style.use('ggplot')
import scipy
from scipy import stats



data_path = 'your path'

#Importing data
callsout = pandas.read_table(data_path + 'callsout_dic.tsv', sep='\t', names=['date_time','cellid','calls_out'], header=None )

# Setting date_time as data frame index
callsout = callsout.sort(columns='date_time', axis=0, ascending=True)
callsout = callsout.reset_index(drop=True)

#some info on the data
callsout.info()

#creating time index
callsout = callsout.set_index(pandas.DatetimeIndex(callsout['date_time']))

#------------------------------#
# STATISTICS AND PLOTS
#------------------------------#
#calculate statistics
statistics = callsout['calls_out'].describe()
#count    7.677681e+06
#mean     1.322562e+00
#std      2.175737e+00
#min     -1.296900e+01
#25%     -6.975566e-02
#50%      1.626751e+00
#75%      2.936448e+00
#max      7.860609e+00
#Name: calls_out, dtype: float64

#saving the statistics in a csv file
statistics.to_csv(data_path + 'callsoutstats.csv', sep=',')
#simple plot
line = callsout['calls_out'].plot(kind='line',logy=False, title = 'Outgoing calls Dic 2013', figsize=(20,5))
#density plot
density = callsout['calls_out'].plot(kind='density',logy=False, title = 'Outgoing calls Dic 2013. Density Plot')
#histogram
histplot = callsout['calls_out'].plot(kind='hist',logy=False,title = 'Outgoing calls Dic 2013. Histogram') 
#boxplot
boxplot = callsout['calls_out'].plot(kind='box',logy=False,title = 'Outgoing calls Dic 2013. Boxplot')
#dataframe to series

#------------------------------#
# NORMALIZING DATA
#------------------------------#
#setting values cero to 0.1: log (0) = undefined
callsout = callsout.replace(0, 0.1)
#callsout = callsout.replace(0, numpy.nan)

#Transforming data into log 
callsoutlog = numpy.log(callsout['calls_out'])
callsout['calls_out'] = callsoutlog
#Cheking normality
histplot = callsout['calls_out'].plot(kind='hist',logy=False, title = 'Outgoing calls Dic 2013 Normalized [log(x)]. Histogram')

#---------------------------------------------------#
# Cheking OUTLIERS 
#---------------------------------------------------#
#standard deviaton of data
std = callsout['calls_out'].std()
#Interquartile range
iqr = 1.35 * std
#25% quartile
q1 = statistics.ix['25%']
#75% quartile
q3 = statistics.ix['75%']
#inferior outer fence limit
inf_out_lim = q1 - (3 * iqr)
#superior outer fence limit
sup_out_lim = q3 + (3 * iqr)

#detecting mayor outliers
callsout['i_outliers'] = callsout['calls_out'].apply(lambda x: 'inf_major_outlier' if x<inf_out_lim else 'NI')
callsout['s_outliers'] = callsout['calls_out'].apply(lambda x: 'sup_major_outlier' if x>sup_out_lim else 'NI')

#pivot table to count the number of ouliers
pandas.pivot_table(callsout, values='calls_out', columns=['i_outliers', 's_outliers'], aggfunc=numpy.count_nonzero)
#i_outliers         s_outliers
#NI                 NI            7676044.0
#inf_major_outlier  NI               1637.0
#dtype: float64
#------------------------------------------
#no sup outliers cause the max value is < sup = 11.74 . inf_major_outlier = 1637
callsout.drop(['i_outliers','s_outliers'],inplace=True,axis=1) 

#create a new dataset without the outliers
callsout['callsout_out'] = callsout['calls_out'].apply(lambda x: numpy.nan if x<inf_out_lim else x)
#check the new dataset
callsout['callsout_out'].describe()
#count    7.676044e+06
#mean     1.324923e+00
#std      2.169920e+00
#min     -8.880377e+00
#25%               NaN
#50%               NaN
#75%               NaN
#max      7.860609e+00
#Name: callsout_out, dtype: float64
histout = callsout['callsout_out'].plot(kind='hist',logy=False, title = 'Outgoing calls Dic 2013 Normalized [log(x)] and no outliers. Histogram')
lineout = callsout['callsout_out'].plot(kind='line',logy=False, title = 'Outgoing calls Dic 2013 Normalized [log(x)] and no outliers')

#saving file into a csv
callsout.to_csv(path_or_buf = data_path + 'callout_normal_dic.csv', sep=',')


print 'enjoy! bye'
