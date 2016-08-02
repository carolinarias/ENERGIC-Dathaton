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
import matplotlib.pyplot as plt
import numpy
import scipy
from outliers import smirnov_grubbs as grubbs
from fitter import Fitter
from scipy import stats


variables = ['Sms in', 'Sms out', 'Callsin', 'Callsout','Internet'] 

#Importing data
callsout = pandas.read_table('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/ts_cellid_variable/calls_out.txt', names=['date_time','cellid','calls_out'], header=None )
#path: where you have your temperature data
temp = pandas.read_table('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/wundermap/nov_dic_2013/csv/datamerged_dic.csv', names=['date_time','cellid','internet'], header=None )

#cellids of the different land use types
id_urban = pandas.read_csv('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/dusaf/11.txt', names=['cellid'], header=None)
id_proc = pandas.read_csv('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/dusaf/12.txt', names=['cellid'], header=None)
id_mine = pandas.read_csv('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/dusaf/13.txt', names=['cellid'], header=None)
id_green = pandas.read_csv('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/dusaf/14.txt', names=['cellid'], header=None)

#--------------------------- -----------------------------------------------------------

#sort by time stamp
print 'files read' 
smsin = smsin.sort(columns='date_time', axis=0, ascending=True)
smsin = smsin.reset_index(drop=True)

smsout = smsout.sort(columns='date_time', axis=0, ascending=True)
smsout = smsout.reset_index(drop=True)

callsin = callsin.sort(columns='date_time', axis=0, ascending=True)
callsin = callsin.reset_index(drop=True)

callsout = callsout.sort(columns='date_time', axis=0, ascending=True)
callsout = callsout.reset_index(drop=True)

internet = internet.sort(columns='date_time', axis=0, ascending=True)
internet = internet.reset_index(drop=True)


#indexing by cellid, this allow to get the rows (subset) of the cell ids that we need
smsin = smsin.set_index(smsin['cellid'])
smsout = smsout.set_index(smsout['cellid'])
callsin = callsin.set_index(callsin['cellid'])
callsout = callsout.set_index(callsout['cellid'])

#subsetting data by land use
#11
smsin_urban = smsin.loc[id_urban['cellid'],:]#select the rows with id from "id_urban" and all columns (.loc[row_indexer,col_indexer])

#12
#13
#14


#subsetting data by date ( workdays, weekends, saturdays and sundays)
workdays = [0,1,2,3,4]
weekends = [5,6]
saturdays = [5]
sundays = [6]
hollidays = ['2013-12-25', '2013-12-31']



smsin_urban['weekday'] = pandas.DatetimeIndex(smsin_urban['date_time']).weekday

smsin_urban.set_index(smsin_urban['weekday'], drop=True, inplace=True, verify_integrity=False)



smsin_urban_workdays = smsin_urban.loc[workdays,:]
smsin_urban_weekends = smsin_urban.loc[weekends,:]
smsin_urban_sunday = smsin_urban.loc[sundays,:]
smsin_urban_sunday = smsin_urban.loc[saturdays,:]

x = smsin_urban_workdays['date_time']
y = smsin_urban_workdays['sms_in']

trace1 = go.Scatter(x = x, y = y, marker={'color': 'red', 'symbol': 104, 'size': "10"}, mode="markers+lines")

trace1 = go.Scatter(x=[1,2,3], y=[4,5,6], marker={'color': 'red', 'symbol': 104, 'size': "10"}, mode="markers+lines",  text=["one","two","three"], name='1st Trace')
                                               
data=go.Data([trace1])
layout=go.Layout(title="First Plot", xaxis={'title':'time stamps'}, yaxis={'title':'sms in for land use 11'})
figure=go.Figure(data=data,layout=layout)
py.iplot(figure, filename='pyguide_1')



#creating temporal indexes
smsin_urban = smsin_urban.set_index(pandas.DatetimeIndex(smsin_urban['date_time']))
smsout = smsout.set_index(pandas.DatetimeIndex(smsout['date_time']))
callsin = callsin.set_index(pandas.DatetimeIndex(callsin['date_time']))
callsout = callsout.set_index(pandas.DatetimeIndex(callsout['date_time']))
internet = internet.set_index(pandas.DatetimeIndex(internet['date_time']))

smsin_urban = smsin_urban.set_index(pandas.DatetimeIndex(smsin_urban['weekday']))


smsin_urban['weekday'] = pandas.DatetimeIndex(smsin_urban['date_time']).weekday

#subsetting data by date/time

smsin_urban['weekday'] = smsin_urban.weekday
smsin_urban_workdays = smsin_urban.ix['weekday']
test2 = pandas.DatetimeIndex.weekday()


#rain = pandas.read_table('/media/sf_2_PhD_2013_-2014/2PhD_WorkDocs/PhD_big-data/data/sms-call-internet-mi/ts_cellid_variable/rain.txt', delimiter=',', skiprows=1, names=['index','cellid','date_time','rain'], header=None, na_values='-999.0' )

#--------------------------- Setting date_time as data frame index-------------------
print 'files read' 
smsin = smsin.sort(columns='date_time', axis=0, ascending=True)
smsin = smsin.reset_index(drop=True)

smsout = smsout.sort(columns='date_time', axis=0, ascending=True)
smsout = smsout.reset_index(drop=True)

callsin = callsin.sort(columns='date_time', axis=0, ascending=True)
callsin = callsin.reset_index(drop=True)

callsout = callsout.sort(columns='date_time', axis=0, ascending=True)
callsout = callsout.reset_index(drop=True)

internet = internet.sort(columns='date_time', axis=0, ascending=True)
internet = internet.reset_index(drop=True)

rain = rain.sort(columns='date_time', axis=0, ascending=True)
rain = rain.reset_index(drop=True)

#---------------------------date time index--------------------------------------------
rng = pandas.date_range(start='2013-10-31 23:00:00', periods=1488, freq='H')
#date_time = smsin['date_time']
#date_time = pandas.to_datetime(data['date_time'])
#print rng

print 'files sorted' 
#--------------------------- Merging columns: create a big data frame with all variables--------------------------------------
columns = ['date_time','cellid']
data = smsin.merge(smsout, on=columns).merge(callsin, on=columns).merge(callsout, on=columns).merge(internet, on=columns).merge(rain, on=columns)
#data = pandas.read_table('/media/sf_2_PhD_2013_-2014/2PhD_WorkDocs/PhD_big-data/data/sms-call-internet-mi/inputs/ts_value/callsout_18-22nov.tsv', names=['date_time','variable'], header=None )
data = data.sort(columns=['date_time'], axis=0, ascending=True)
data = data.reset_index(drop=True)
data = data.drop('index', axis=1)

smsin.info()
#smsout.info()
#callsin.info()
#callsout.info()
#internet.info()
#data.info()
#rain.info()
#----------------------------Subsetting data by time-------------------
#----------------------------Aggregating data by day--------------------------------
#creating temporal indexes
smsin = smsin.set_index(pandas.DatetimeIndex(smsin['date_time']))
smsout = smsout.set_index(pandas.DatetimeIndex(smsout['date_time']))
callsin = callsin.set_index(pandas.DatetimeIndex(callsin['date_time']))
callsout = callsout.set_index(pandas.DatetimeIndex(callsout['date_time']))
internet = internet.set_index(pandas.DatetimeIndex(internet['date_time']))
rain = rain.set_index(pandas.DatetimeIndex(rain['date_time']))
print 'Date time index set'

#exporting dataframes into files
smsin.to_csv('smsin.csv')
smsout.to_csv('smsout.csv')
callsin.to_csv('callsin.csv')
callsout.to_csv('callsout.csv')
internet.to_csv('internet.csv')
df_sample = smsin[0:721000]
df_sample.to_csv('smsin_nov.csv')

#----------------------------setting values cero to NAN -------------------------------
smsin = smsin.replace(0, 0.1)
smsout = smsout.replace(0, numpy.nan)
callsin = callsin.replace(0, numpy.nan)
callsout = callsout.replace(0, numpy.nan)
internet = internet.replace(0, numpy.nan)

smsin.hist('sms_in', bins=500, figsize=(20,5))

smsin['sms_in'].plot(kind='hist',figsize=(20,5))

#----------------------------Transforming data into log -------------------------------
smsinlog = numpy.log(smsin['sms_in'])
smsoutlog = numpy.log(smsout['sms_out'])
callsinlog = numpy.log(callsin['calls_in'])
callsoutlog = numpy.log(callsout['calls_out'])
internetlog = numpy.log(internet['internet'])

smsinlog.plot(kind='hist',logy=False,figsize=(20,5))
smsinlog.plot(kind='box',logy=False,figsize=(20,5))

grubbs.test(smsinlog, alpha=0.1)
f = Fitter(smsinlog)
f.fit()
f.summary()

smsinlog.describe()



test = numpy.random.normal(1.839771, 2.003851, 14877485)
#----------------------------------------------------------

#----------------------------Normality test-------------------------------

scipy.stats.normaltest(smsinlog, axis=0)
#NormaltestResult(statistic=803869.62940951809, pvalue=0.0)
scipy.stats.shapiro(smsinlog, a=None, reta=False)
#(0.9956305623054504, 0.0)
scipy.stats.anderson(test, dist='norm')
#AndersonResult(statistic=87569.946015860885, critical_values=array([ 0.576,  0.656,  0.787,  0.918,  1.092]), significance_level=array([ 15. ,  10. ,   5. ,   2.5,   1. ]))
#AndersonResult(statistic=0.27488219365477562, critical_values=array([ 0.576,  0.656,  0.787,  0.918,  1.092]), significance_level=array([ 15. ,  10. ,   5. ,   2.5,   1. ]))
scipy.stats.t.fit(smsinlog)


#----------------------------Aggregating data by day-------------------------------

#create a series with data from all cellid and just one variable
ssmsin = smsin.iloc[:,2]
ssmsout = smsout.iloc[:,2]
scallsin = callsin.iloc[:,2]
scallsout = callsout.iloc[:,2]
sinternet = internet.iloc[:,2]

#convert the series into a list
lsmsin = ssmsin.tolist()
lsmsout = ssmsout.tolist()
lcallsin = scallsin.tolist()
lcallsout = scallsout.tolist()
linternet = sinternet.tolist()

#create a series with the list values and a date time index
smsins = pandas.Series(lsmsin,name='sms_in',index=rng)
smsouts = pandas.Series(lsmsout,name='sms_out',index=rng)
callsins = pandas.Series(lcallsin,name='calls_in',index=rng)
callsouts = pandas.Series(lcallsout,name='calls_out',index=rng)
internets = pandas.Series(linternet,name='internet',index=rng)

#Series with values for one day and one variable, all cellids
smsinday = smsin.ix['2013-11-01']
#Series with mean values of all days
smsinhr = smsin.resample('D', how='mean')

#----------------------------Select data by value-------------------------------

max_value = smsin['sms_in'].max()
max_cell = smsin[(smsin.sms_in == max_value)]
cellid = max_cell['cellid']
date = smsin[(smsin.date_time == max_value)]

#----------------------------Subsetting data by cellid-----------------------------

#Choose cellid
cellid = 5059
#Create a data frame with values for the given cellid
celldf = smsin[(smsin.cellid == cellid)]
max_value_cell = celldf['sms_in'].max()
#Create a series with all values for the given cellid ( all rows, second column)
cellseries = celldf.iloc[:,2]
#convert the series into a list
cellseries = cellseries.tolist()
#create a series with the list values and a date time index
cell = pandas.Series(cellseries,name='sms_in',index=rng)
#cell statistics
cellstat = cell.describe()
print cellstat

#Choose cellid
cellid = 5161
#Create a data frame with values for the given cellid
celldf = smsin[(smsin.cellid == cellid)]
#Create a series with all values for the given cellid ( all rows, second column)
cellseries = celldf.iloc[:,2]
#convert the series into a list
cellseries = cellseries.tolist()
#create a series with the list values and a date time index
cell = pandas.Series(cellseries,name='sms_in',index=rng)
#transform values into log
cell = cell.apply(numpy.log)


#-----------Subsetting data by cellid and time--------------------

#resample the previous series by time
cellD = cell.resample('1D', how='sum')
cellday = callsout.ix['2013-11-27', '2013-11-01']
#-------------------------------------Statistics------------------------------------

#http://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.Series.value_counts.html
print 'basic statistics'
cov = data.cov()
print cov
corr = data.corr(method='pearson',min_periods=1)
print corr
kur = smsin['variable'].kurtosis()
kurt = smsin['variable'].kurt()
skew = smsin['variable'].skew()
stats = data.describe()
smsinlog=smsin.log()
stats = data.describe()

#probability plot
scipy.stats.probplot(smsin['sms_in'], dist='norm', fit=True, plot=plt)




#
##----------------------------Plotting------------------------------------
#using plotly:
plotly.offline.plot(ssmsin)

import cufflinks as cf
import pandas as pd


smsin.plot(x='Date',kind='scatter')









#plots for all values each variable:
plotsmsin = internet['sms_in'].plot(kind='line',logy=False, figsize=(20,5))
plotsmsout = internet['sms_out'].plot(kind='line',logy=False, figsize=(20,5))
plotcallsin = internet['calls_in'].plot(kind='line',logy=False, figsize=(20,5))
plotcallsout = internet['calls_out'].plot(kind='line',logy=False, figsize=(20,5))
plotinternet = internet['internet'].plot(kind='line',logy=False, figsize=(20,5))
plotrain = rain['rain'].plot(kind='line',logy=False, figsize=(20,5))


#boxplots for all values each variable:
smsin.plot(kind='box',logy=False, figsize=(8,5))

plot = data.plot(kind='line',logy=False, figsize=(20,5))
smsin.plot(kind='box',logy=False, figsize=(8,5))
smsin.plot(kind='hist',logy=False, figsize=(8,5))
hist = smsin.hist('sms_in', bins=100, figsize=(8,5))
plt.figure();
callsout.plot(bins=40, figsize=(8,5))













#plots of values of one cell:

cell = pandas.DataFrame(cell)
cellday.plot(kind='line',logy=False, figsize=(8,5))
cellday.plot(kind='box',logy=False, figsize=(8,5))
cellday.plot(kind='hist',logy=False, figsize=(8,5))

cell.plot(kind='line',logy=False, figsize=(20,5))
cell.plot(kind='box',logy=False, figsize=(8,5))
cell.plot(kind='hist',logy=False, figsize=(8,5))

#callsout.plot(kind='hist', alpha=0.5)


print stats



# two plots together----
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
top.plot(smsin.index, smsin["sms_in"])
plt.title('Sms_in Milan, Nov - Dic 2013')

bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
bottom.bar(rain.index, rain['rain'])
plt.title('Rain in Milan, Nov - Dic 2013')

plt.gcf().set_size_inches(15,8)

#plot all variables together
data.plot(subplots = True, figsize = (8, 8));
plt.legend(loc = 'best')
plt.show()





print 'enjoy! bye'
