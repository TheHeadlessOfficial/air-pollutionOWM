import os, sys
from PIL import Image
import requests
import time
import datetime
import json
import pprint
import linecache
# Lock file to tell conky that the script is running
lock_file = "/tmp/script_done.lock"
# Check for file lock
try:
    open(lock_file, 'w').close()
    ################################ set lat e lon
    lat = '45.373'
    lon = '11.8351'
    myAPPID = ''
    ################################ my API url today (insert it between apostrophe, DON'T delete apostrophes)
    url = 'https://api.openweathermap.org/data/2.5/air_pollution?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + myAPPID
    res = requests.get(url).json()
    data = res
    ################################ my API url forecast (insert it between apostrophe, DON'T delete apostrophes)
    url2 = 'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + myAPPID
    res2 = requests.get(url2).json()
    data2 = res2
    ################################ get your HOME name automatically
    homepath = os.environ['HOME']
    homename = homepath
    homename = homename[6:]
    ################################ set paths
    conkypath = '/.conky/'
    airfolder = 'AirPollution/'
    pathtoday = '/home/' + homename + conkypath + airfolder + 'aptoday.txt'
    pathforecast = '/home/' + homename + conkypath + airfolder + 'apforecast.txt'
    pathchoisep = '/home/' + homename + conkypath + airfolder + 'apchoisep.txt'
    pathchoisen = '/home/' + homename + conkypath + airfolder + 'apchoisen.txt'
    pathconkyg = '/home/' + homename + conkypath + airfolder + 'conkyg.txt'
    pathconkyt = '/home/' + homename + conkypath + airfolder + 'conkyt.txt'
    pathconkyp = '/home/' + homename + conkypath + airfolder + 'conkyp.txt'
    pathconkyn = '/home/' + homename + conkypath + airfolder + 'conkyn.txt'
    ################################ set variables
    color = 2
    nlist = 88 #240
    ################################ create array for FORECAST data
    aqif = []
    cof = []
    nof = []
    no2f = []
    o3f = []
    so2f = []
    pm25f = []
    pm10f = []
    nh3f = []
    dtf = []
    dtdf = []
    ################################ get data for TODAY
    lon = data['coord']['lon']
    lat = data['coord']['lat']
    aqi = data['list'][0]['main']['aqi']
    co = data['list'][0]['components']['co']
    no = data['list'][0]['components']['no']
    no2 = data['list'][0]['components']['no2']
    o3 = data['list'][0]['components']['o3']
    so2 = data['list'][0]['components']['so2']
    pm25 = data['list'][0]['components']['pm2_5']
    pm10 = data['list'][0]['components']['pm10']
    nh3 = data['list'][0]['components']['nh3']
    dt = data['list'][0]['dt']
    dtd = dt
    #                           convert dt into date
    dtd = time.strftime("%d-%b-%Y h%H:%M:%S", time.localtime(dt))
    ################################ write clean TODAY data on file
    fo = open(pathtoday, 'w')
    fo.write('{}\n'.format(lon))
    fo.write('{}\n'.format(lat))
    fo.write('{}\n'.format(aqi))
    fo.write('{}\n'.format(co))
    fo.write('{}\n'.format(no))
    fo.write('{}\n'.format(no2))
    fo.write('{}\n'.format(o3))
    fo.write('{}\n'.format(so2))
    fo.write('{}\n'.format(pm25))
    fo.write('{}\n'.format(pm10))
    fo.write('{}\n'.format(nh3))
    fo.write('{}\n'.format(dt))
    fo.write('{}\n'.format(dtd))
    fo.close()
    ################################ set next and previous days (based on 'count' variable)
    countp = -5   # max value is -5
    countn = 5    # max value is 5
    r12 = linecache.getline(pathforecast, 10)
    prevdays = []
    nextdays = []
    j = 1
    #                   select previous days
    for i in range(0, countp, -1):
        prevdays.append(int(r12) - 86400 * j)
        j = j + 1
    j = 1
    #                   select next days
    for i in range(0, countn):
        if i == 0:
            nextdays.append(int(r12) + 86400 * j)
            j = j + 1
        if i > 0:
            nextdays.append(int(r12) + 86400 * j)
            j = j + 1
    ################################ get FORECAST data for every day (5 days, before and after today, hourly)
    for i in range(0, nlist):
        aqif.append(data2['list'][i]['main']['aqi'])
        cof.append(data2['list'][i]['components']['co'])
        nof.append(data2['list'][i]['components']['no'])
        no2f.append(data2['list'][i]['components']['no2'])
        o3f.append(data2['list'][i]['components']['o3'])
        so2f.append(data2['list'][i]['components']['so2'])
        pm25f.append(data2['list'][i]['components']['pm2_5'])
        pm10f.append(data2['list'][i]['components']['pm10'])
        nh3f.append(data2['list'][i]['components']['nh3'])
        dtf.append(data2['list'][i]['dt'])
        dtdf.append(data2['list'][i]['dt'])
    ################################ write previous days on file (based on 'count' variable)
    fo = open(pathchoisep, 'w')
    for i in range(0, nlist):
        if dtf[i] in prevdays:
            fo.write('{}\n'.format(aqif[i]))
            fo.write('{}\n'.format(cof[i]))
            fo.write('{}\n'.format(nof[i]))
            fo.write('{}\n'.format(no2f[i]))
            fo.write('{}\n'.format(o3f[i]))
            fo.write('{}\n'.format(so2f[i]))
            fo.write('{}\n'.format(pm25f[i]))
            fo.write('{}\n'.format(pm10f[i]))
            fo.write('{}\n'.format(nh3f[i]))
            fo.write('{}\n'.format(dtf[i]))
            dtdf[i] = time.strftime("%d-%b-%Y h%H:%M:%S", time.localtime(dtf[i]))
            fo.write('{}\n'.format(dtdf[i]))
    fo.close()   
    ################################ write next days on file (based on 'count' variable)
    fo = open(pathchoisen, 'w')
    for i in range(0, nlist):
        if dtf[i] in nextdays:
            fo.write('{}\n'.format(aqif[i]))
            fo.write('{}\n'.format(cof[i]))
            fo.write('{}\n'.format(nof[i]))
            fo.write('{}\n'.format(no2f[i]))
            fo.write('{}\n'.format(o3f[i]))
            fo.write('{}\n'.format(so2f[i]))
            fo.write('{}\n'.format(pm25f[i]))
            fo.write('{}\n'.format(pm10f[i]))
            fo.write('{}\n'.format(nh3f[i]))
            fo.write('{}\n'.format(dtf[i]))
            dtdf[i] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(dtf[i]))
            fo.write('{}\n'.format(dtdf[i]))
    fo.close()   
    ################################ write FORECAST clean data on a file
    fo = open(pathforecast, 'w')
    for i in range(0, nlist):
        fo.write('{}\n'.format(aqif[i]))
        fo.write('{}\n'.format(cof[i]))
        fo.write('{}\n'.format(nof[i]))
        fo.write('{}\n'.format(no2f[i]))
        fo.write('{}\n'.format(o3f[i]))
        fo.write('{}\n'.format(so2f[i]))
        fo.write('{}\n'.format(pm25f[i]))
        fo.write('{}\n'.format(pm10f[i]))
        fo.write('{}\n'.format(nh3f[i]))
    #                     convert dt into date
        dtdf[i] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(dtf[i]))
        fo.write('{}\n'.format(dtf[i]))
        fo.write('{}\n'.format(dtdf[i]))
    fo.close()
    ################################ create conky statements
    #                 separator
    line = "${alignc}--------------------------------------------------------"
    #                 heading
    heading = "${color2}${font URW Gothic L:size=9}AIR POLLUTION ${font}${color}    	 ${font URW Gothic L:size=6}by OpenWeather${image $HOME" + conkypath + airfolder + "python_logo.png -p 90,0 -s 15x15}"
    heading2 = "${color4}${alignc}${voffset 5}${font URW Gothic L:size=7}Air Quality Index (1=good to 5=very poor)${font}"
    heading3 = "${color2}${alignc}-------------------------"
    #                 ending
    end = "${color2}${hr 1}"
    #                 today section (2nd group for onecallapi size goto290)
    today1 = "${alignc}${color}${font URW Gothic L:bold:size=8}${execpi 900 sed -n '13p' $HOME" + conkypath + airfolder + "aptoday.txt |cut -c1-18} ${color2}${alignc}${font}AQI: ${color}${execpi 900 sed -n '3p' $HOME" + conkypath + airfolder + "aptoday.txt}"
    today2 = "${color2}CO: ${color}${execpi 900 sed -n '4p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '8p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3"
    today3 = "${color2}NO: ${color}${execpi 900 sed -n '5p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '9p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3"
    today4 = "${color2}NO2: ${color}${execpi 900 sed -n '6p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '10p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3"
    today5 = "${color2}O3: ${color}${execpi 900 sed -n '7p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '11	p' $HOME" + conkypath + airfolder + "aptoday.txt} μg/m3"
    #                 previous days
    prev1a = "${alignc}${color}${execpi 900 sed -n '11p' $HOME" + conkypath + airfolder + "apchoisep.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '1p' $HOME" + conkypath + airfolder + "apchoisep.txt}"
    prev1b = "${color2}CO: ${color}${execpi 900 sed -n '2p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '6p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev1c = "${color2}NO: ${color}${execpi 900 sed -n '3p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '7p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev1d = "${color2}NO2: ${color}${execpi 900 sed -n '4p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '8p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev1e = "${color2}O3: ${color}${execpi 900 sed -n '5p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '9p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev2a = "${alignc}${color}${execpi 900 sed -n '22p' $HOME" + conkypath + airfolder + "apchoisep.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '12p' $HOME" + conkypath + airfolder + "apchoisep.txt}"
    prev2b = "${color2}CO: ${color}${execpi 900 sed -n '13p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '17p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev2c = "${color2}NO: ${color}${execpi 900 sed -n '14p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '18p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev2d = "${color2}NO2: ${color}${execpi 900 sed -n '15p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '19p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev2e = "${color2}O3: ${color}${execpi 900 sed -n '16p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '20p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev3a = "${alignc}${color}${execpi 900 sed -n '33p' $HOME" + conkypath + airfolder + "apchoisep.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '23p' $HOME" + conkypath + airfolder + "apchoisep.txt}"
    prev3b = "${color2}CO: ${color}${execpi 900 sed -n '24p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '28p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev3c = "${color2}NO: ${color}${execpi 900 sed -n '25p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '29p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev3d = "${color2}NO2: ${color}${execpi 900 sed -n '26p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '30p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev3e = "${color2}O3: ${color}${execpi 900 sed -n '27p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '31p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev4a = "${alignc}${color}${execpi 900 sed -n '44p' $HOME" + conkypath + airfolder + "apchoisep.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '34p' $HOME" + conkypath + airfolder + "apchoisep.txt}"
    prev4b = "${color2}CO: ${color}${execpi 900 sed -n '35p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '39p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev4c = "${color2}NO: ${color}${execpi 900 sed -n '36p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '40p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev4d = "${color2}NO2: ${color}${execpi 900 sed -n '37p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '41p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev4e = "${color2}O3: ${color}${execpi 900 sed -n '38p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '42p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev5a = "${alignc}${color}${execpi 900 sed -n '55p' $HOME" + conkypath + airfolder + "apchoisep.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '45p' $HOME" + conkypath + airfolder + "apchoisep.txt}"
    prev5b = "${color2}CO: ${color}${execpi 900 sed -n '46p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '50p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev5c = "${color2}NO: ${color}${execpi 900 sed -n '47p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '51p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev5d = "${color2}NO2: ${color}${execpi 900 sed -n '48p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '52p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    prev5e = "${color2}O3: ${color}${execpi 900 sed -n '49p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '53p' $HOME" + conkypath + airfolder + "apchoisep.txt} μg/m3"
    #                 next days
    next1a = "${alignc}${color}${execpi 900 sed -n '11p' $HOME" + conkypath + airfolder + "apchoisen.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '1p' $HOME" + conkypath + airfolder + "apchoisen.txt}"
    next1b = "${color2}CO: ${color}${execpi 900 sed -n '2p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '6p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next1c = "${color2}NO: ${color}${execpi 900 sed -n '3p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '7p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next1d = "${color2}NO2: ${color}${execpi 900 sed -n '4p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '8p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next1e = "${color2}O3: ${color}${execpi 900 sed -n '5p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '9p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next2a = "${alignc}${color}${execpi 900 sed -n '22p' $HOME" + conkypath + airfolder + "apchoisen.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '12p' $HOME" + conkypath + airfolder + "apchoisen.txt}"
    next2b = "${color2}CO: ${color}${execpi 900 sed -n '13p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '17p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next2c = "${color2}NO: ${color}${execpi 900 sed -n '14p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '18p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next2d = "${color2}NO2: ${color}${execpi 900 sed -n '15p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '19p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next2e = "${color2}O3: ${color}${execpi 900 sed -n '16p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '20p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next3a = "${alignc}${color}${execpi 900 sed -n '33p' $HOME" + conkypath + airfolder + "apchoisen.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '23p' $HOME" + conkypath + airfolder + "apchoisen.txt}"
    next3b = "${color2}CO: ${color}${execpi 900 sed -n '24p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '28p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next3c = "${color2}NO: ${color}${execpi 900 sed -n '25p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '29p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next3d = "${color2}NO2: ${color}${execpi 900 sed -n '26p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '30p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next3e = "${color2}O3: ${color}${execpi 900 sed -n '27p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '31p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next4a = "${alignc}${color}${execpi 900 sed -n '44p' $HOME" + conkypath + airfolder + "apchoisen.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '34p' $HOME" + conkypath + airfolder + "apchoisen.txt}"
    next4b = "${color2}CO: ${color}${execpi 900 sed -n '35p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '39p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next4c = "${color2}NO: ${color}${execpi 900 sed -n '36p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '40p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next4d = "${color2}NO2: ${color}${execpi 900 sed -n '37p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '41p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next4e = "${color2}O3: ${color}${execpi 900 sed -n '38p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '42p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next5a = "${alignc}${color}${execpi 900 sed -n '55p' $HOME" + conkypath + airfolder + "apchoisen.txt |cut -c1-18} ${color2}${alignc}AQI: ${color}${execpi 900 sed -n '45p' $HOME" + conkypath + airfolder + "apchoisen.txt}"
    next5b = "${color2}CO: ${color}${execpi 900 sed -n '46p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}SO2: ${color}${execpi 900 sed -n '50p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next5c = "${color2}NO: ${color}${execpi 900 sed -n '47p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM2.5: ${color}${execpi 900 sed -n '51p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next5d = "${color2}NO2: ${color}${execpi 900 sed -n '48p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}PM10: ${color}${execpi 900 sed -n '52p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    next5e = "${color2}O3: ${color}${execpi 900 sed -n '49p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3${color2}${goto 130}NH3: ${color}${execpi 900 sed -n '53p' $HOME" + conkypath + airfolder + "apchoisen.txt} μg/m3"
    #                 write general conky statements on file
    fo = open(pathconkyg, 'w')
    fo.write('{}\n'.format(heading))
    fo.write('{}\n'.format(heading2))
    fo.write('{}\n'.format(heading3))
    fo.write('{}\n'.format(end))
    fo.close()
    #                 write TODAY conky statements on file
    fo = open(pathconkyt, 'w')
    fo.write('{}\n'.format(today1))
    fo.write('{}\n'.format(today2))
    fo.write('{}\n'.format(today3))
    fo.write('{}\n'.format(today4))
    fo.write('{}\n'.format(today5))
    fo.write('{}\n'.format(line))
    fo.close()
    #                 write PREVIOUS DAYS conky statements on file
    fo = open(pathconkyp, 'w')
    fo.write('{}\n'.format(prev1a))
    fo.write('{}\n'.format(prev1b))
    fo.write('{}\n'.format(prev1c))
    fo.write('{}\n'.format(prev1d))
    fo.write('{}\n'.format(prev1e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(prev2a))
    fo.write('{}\n'.format(prev2b))
    fo.write('{}\n'.format(prev2c))
    fo.write('{}\n'.format(prev2d))
    fo.write('{}\n'.format(prev2e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(prev3a))
    fo.write('{}\n'.format(prev3b))
    fo.write('{}\n'.format(prev3c))
    fo.write('{}\n'.format(prev3d))
    fo.write('{}\n'.format(prev3e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(prev4a))
    fo.write('{}\n'.format(prev4b))
    fo.write('{}\n'.format(prev4c))
    fo.write('{}\n'.format(prev4d))
    fo.write('{}\n'.format(prev4e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(prev5a))
    fo.write('{}\n'.format(prev5b))
    fo.write('{}\n'.format(prev5c))
    fo.write('{}\n'.format(prev5d))
    fo.write('{}\n'.format(prev5e))
    fo.write('{}\n'.format(line))
    fo.close()
    #                 write NEXT DAYS conky statements on file
    fo = open(pathconkyn, 'w')
    fo.write('{}\n'.format(next1a))
    fo.write('{}\n'.format(next1b))
    fo.write('{}\n'.format(next1c))
    fo.write('{}\n'.format(next1d))
    fo.write('{}\n'.format(next1e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(next2a))
    fo.write('{}\n'.format(next2b))
    fo.write('{}\n'.format(next2c))
    fo.write('{}\n'.format(next2d))
    fo.write('{}\n'.format(next2e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(next3a))
    fo.write('{}\n'.format(next3b))
    fo.write('{}\n'.format(next3c))
    fo.write('{}\n'.format(next3d))
    fo.write('{}\n'.format(next3e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(next4a))
    fo.write('{}\n'.format(next4b))
    fo.write('{}\n'.format(next4c))
    fo.write('{}\n'.format(next4d))
    fo.write('{}\n'.format(next4e))
    fo.write('{}\n'.format(line))
    fo.write('{}\n'.format(next5a))
    fo.write('{}\n'.format(next5b))
    fo.write('{}\n'.format(next5c))
    fo.write('{}\n'.format(next5d))
    fo.write('{}\n'.format(next5e))
    fo.close()
except Exception as e:
    # Manage exceptions (optional)
    filelockerror = (f"Error during script execution: {e}")
finally:
    # remove lock file
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass  # file already removed

