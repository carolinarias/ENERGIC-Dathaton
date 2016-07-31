//Nodejs requirements files
var express = require('express');
var app = express();
var Curl = require('node-libcurl').Curl;

var json2csv = require('json2csv');
var fs = require('fs');

//Default values

//Fields of the CSV to create
var fields = ['lat', 'lng', 'name', 'date', 'tmp', 'hum', 'prec', 'heatindex'];

//Initialize the observations to null
var obs = null;

//Set the init date to download the files with WunderAPI
var InitDate = new Date("10/31/2013");


//Function to increase one day and return in in the WunderAPI format
function getDay() {
    var dayPlus = 86400000;
    InitDate.setMilliseconds(dayPlus);
    var year = InitDate.getFullYear();
    var day = InitDate.getDate();
    if (day < 10) {
        day = "0" + day;
    }
    var month = InitDate.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }

    return (String(year) + String(month) + String(day));
}

index = 0;
stationIndex = 0;

var csv = [];

//Function to query WunderAPI inserting the available stations and their position
function query() {
    a = ["ILOMBARD77", "ILOMBARD208", "IMILANOM4", "ILOMBARD204", "IMILANOM7", "ILOMBARD123", "ILOMBARD38", "IMONZABR2", "ILOMBARD145", "ILOMBARD131", "IMILANOR2", "ILOMBARD156", "ILOMBARD23", "ILOMBARD229", "ILOMBARD245"]
    coord = [
        ["45.393116", "9.284693"],
        ["45.489471", "9.337339"],
        ["45.497990", "9.240542"],
        ["45.453648", "9.133364"],
        ["45.447182", "9.127700"],
        ["45.528805", "9.397827"],
        ["45.597855", "9.260246"],
        ["45.607300", "9.236262"],
        ["45.600391", "9.422575"],
        ["45.513386", "9.005838"],
        ["45.489208", "8.969536"],
        ["45.655838", "9.307959"],
        ["45.653057", "9.199204"],
        ["45.664894", "9.160927"],
        ["45.636318", "9.076327"]
    ];

    date = getDay();


    var station = a[stationIndex];

    var link = "api.wunderground.com/api/780649e537edea33/history_" + date + "/q/pws:" + station + ".json";

    var curl = new Curl();
    curl.setOpt('URL', link);
    curl.setOpt('FOLLOWLOCATION', true);
    curl.on('end', function(statusCode, body, headers) {
        try {
            var obs = JSON.parse(body).history.observations;

            for (var x = 0; x < obs.length; x++) {

                var y = obs[x].date.year;
                var m = obs[x].date.mon;
                var d = obs[x].date.mday;
                var time = new Date(m + "/" + d + "/" + y);
                time.setHours(obs[x].date.hour);
                time.setMinutes(obs[x].date.min);
                time = time.toISOString();


                obj = {
                    "lat": coord[stationIndex][0],
                    "lng": coord[stationIndex][1],
                    "name": station,
                    "date": time,
                    "tmp": obs[x].tempm,
                    "hum": obs[x].hum,
                    "prec": obs[x].precip_totalm,
                    "heatindex": obs[x].heatindexm
                };

                csv.push(obj);
            }
            console.log(date);
            if (index < 62) {

                query();
                index++;
            } else if (stationIndex < a.length) {
                index = 0;
                save(csv, station);
                csv = [];
                InitDate = new Date("10/31/2013");
                stationIndex++;
                query();
            } else {

            }
        } catch (e) {
            console.log(e);
            query();
        }
    });
    curl.on('error', curl.close.bind(curl));
    curl.perform();


}

//function to create a CSV after one station has finished to be queried
function save(csv, station) {
    json2csv({
        data: csv,
        fields: fields
    }, function(err, csv) {
        if (err) console.log(err);
        fs.writeFile('csv/' + station + '.csv', csv, function(err) {
            if (err) throw err;
            console.log('file saved');
        });
    });
}

//Calling to the main function, that will call itself after each station
query();

//Running node.js app
app.listen(3000, function() {
    console.log('Example app listening on port 3000!');
});
