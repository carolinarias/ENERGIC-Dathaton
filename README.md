# ENERGIC-Datathon

Here you can find the python scripts used for the ENERGIC - Datathon http://vgibox.eu/activities/datathon-challenge/ . Please check: http://landcover.como.polimi.it/datathon/pages/methodology.html first.

here you'll find:

<strong>data_acquisition:</strong><br>
<code>wunderapi.js</code>: download data from weather underground api <br>

<strong>data_processing </strong>: <br>
<code>wunder.py</code>: weather underground data preprocessing <br>
<code>ts_cellid_onev.py</code>: telecom Italy open data preprocessing <br>
<code>exploration.py</code>: telecom Italy open data statistical exploration <br>
<code>preanova.py</code>: merging of telecom data and temperature data for anova analysis.<br>

<strong>analysis </strong>: <br>
<code>twowayanova.R</code>: Two way ANOVA with unequal sample sizes <br>

<strong>data </strong>: <br>
<i>cellid_wunder2013stations</i>: table relating Milano grid cells id with weather underground stations<br>
<i>stationsdata.zip</i>: weather data extracted from weather underground API nov - dic 2013<br>
<i>stationsdata_aggregated.zip</i>: csv files of weather data aggregated by hour (mean) dic 2013<br>
<i>data_dic.csv</i>: one csv file with weather data aggregated by hour (mean) dic 2013 <br>
<p>Large files. Download follwing the dropbox link:</p>
<i>datamerged_dic.csv</i>: one csv file with weather data aggregated by hour (mean), together with Milano grid cells id. dic 2013 <br>
https://www.dropbox.com/s/ku3qvxi1v25zn80/datamerged_dic.csv?dl=0<br>
<i>callsout_dic.csv</i>: one csv file with outgoing calls in the city of Milano during dic 2013<br>
https://www.dropbox.com/s/8tsvmb8vl5zr25e/callsout_dic.tsv?dl=0<br>
<i>callsout_normal_dic.csv</i>: one csv file with outgoing calls in the city of Milano during dic 2013, normalized (log(x)) <br>
https://www.dropbox.com/s/p54x3955ql86m0e/callout_normal_dic.csv?dl=0<br>
<i>anovadata.csv</i>: one csv file with outgoing calls in the city of Milano during dic 2013, classified by day type (weekends and workdays) and temperature levels (high, medium, maximum) <br>
https://www.dropbox.com/s/mbm5p2cfefuci7v/anovadata.csv?dl=0<br>

