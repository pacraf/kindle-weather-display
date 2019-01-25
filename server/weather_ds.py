# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import forecastio
import codecs
import datetime
import feedparser


api_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
lat = 50.999
lng = 18.999
lang = 'pl'
units = 'si'
current_time = datetime.datetime.now()
forecast = forecastio.load_forecast(api_key, lat, lng,time=None, units='si',lang='pl',)
#vapi_key, lat, lng)
#time=current_time, units='si', lang='pl', 0, None)

by_hour = forecast.hourly()
by_day = forecast.daily()

today = datetime.date.today()

icons = [None]*4
icons = [by_day.data[0].icon,by_day.data[1].icon,by_day.data[2].icon,by_day.data[3].icon]




highs = [None]*4
highs = [by_day.data[0].temperatureMax,by_day.data[1].temperatureMax,by_day.data[2].temperatureMax,by_day.data[3].temperatureMax]
for i in range(len(highs)):
    highs[i]= int(round(highs[i],0))

lows = [None]*4
lows = [by_day.data[0].temperatureMin,by_day.data[1].temperatureMin,by_day.data[2].temperatureMin,by_day.data[3].temperatureMin]
for i in range(len(lows)):
    lows[i]= int(round(lows[i],0))

#for hourly_data_point in by_hour.data:
#    print hourly_data_point

#for daily_data_point in by_day.data:
#    print daily_data_point


print (icons)
print (highs)
print (lows)
#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('ds-weather-script-preprocess.svg', 'r', encoding='utf-8').read()

#insert decription
output = output.replace('D1_DESCRIPTION',by_day.summary)
# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['PoniedziaĹ‚ek', 'Wtorek', 'Ĺšroda', 'Czwartek', 'PiÄ…tunio', 'Sobcia', 'Niedzielka']
output = output.replace('DAY_ONE',days_of_week[today.weekday()] + '   ' + by_day.data[1].time.strftime("%d/%m/%y")).replace('DAY_TWO',days_of_week[by_day.data[2].time.weekday()]).replace('DAY_THREE',days_of_week[by_day.data[3].time.weekday()]).replace('DAY_FOUR',days_of_week[by_day.data[4].time.weekday()])

#insert Atom Warning
#output = output.replace('ATOM:',atom[0]).replace('ATOM1:',atom[1]).replace('ATOM2:',atom[2])

#insert time stamp
output = output.replace('GEN_TIME',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)


