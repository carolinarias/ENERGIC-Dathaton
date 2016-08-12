"""
------------------------------------------------------------------------------------------------------------------
WEATHER UNDERGROUND AND TELECOM DATA PREPROCESSING

File name: preanova.py
Description: This script prepares the data fro the anova analisis in R.
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

data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/wundermap/nov_dic_2013/csv/'
data_path_out = data_path + 'out/'

#Importing data
#path: where you have your outgoin calls data
callsout = pandas.read_table(data_path +'callout_normal_dic.csv',  sep = ',', names=['index','ts','cellid','calls_out','callsout_out'], header=0 )#(7677681,4)
temp = pandas.read_table(data_path_out + 'datamerged_dic.csv', sep = ',', names=['index','cellid','name','ts','tmp'], header=0 ) #(731340,5)
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
first_limit = t_mean - (t_std/2)
second_limit = t_mean + (t_std/2)

#Creating ranges
temp['t_levels'] = temp['tmp'].apply(lambda x: 'low' if t_min<=x<first_limit else x)
temp['t_levels'] = temp['t_levels'].apply(lambda x: 'medium' if first_limit<=x<second_limit else x)
temp['t_levels'] = temp['t_levels'].apply(lambda x: 'high' if second_limit<=x<=t_max else x)


pandas.pivot_table(temp, values='tmp', columns=['t_levels'], aggfunc=numpy.count_nonzero)
#t_levels
#high      2471444.0
#low       2234522.0
#medium    2494215.0
#Name: tmp, dtype: float64


#---------------------------------------------------#
# CREATING TYPE OF DAYS CATEGORY : weekend, workdays
#---------------------------------------------------#
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
anovadata = pandas.merge(callsout, temp, right_index=True, left_index=True)# (731340,10)

#use a pivot table to check everthing is ok
pandas.pivot_table(anovadata, values='calls_out', columns=['d_type', 't_levels'], aggfunc=numpy.count_nonzero)
#d_type    t_levels
#weekend   high         755656.0
#          low          639396.0
#          medium       702924.0
#workdays  high        1715788.0
#          low         1600268.0
#          medium      1791291.0
#total:7205323 - 7331340 = 126017 nan values

#eliminating unnecessary columns
anovadata.drop(['cellid_y', 'ts_y','weekday','tmp','index'],inplace=True,axis=1) 

#save data into a csv
anovadata.to_csv(path_or_buf = data_path + 'anovadata.csv', sep=',')



print 'enjoy! bye'
