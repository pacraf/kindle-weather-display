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


highs_time = [None]*2
highs_time = [str(datetime.datetime.fromtimestamp(by_day.data[0].temperatureHighTime).strftime("%H:%M"))]

lows = [None]*4
lows = [by_day.data[0].temperatureMin,by_day.data[1].temperatureMin,by_day.data[2].temperatureMin,by_day.data[3].temperatureMin]

lows_time = [None] * 2
lows_time = [str(datetime.datetime.fromtimestamp(by_day.data[0].temperatureMinTime).strftime("%H:%M"))]

for i in range(len(lows)):
    lows[i]= int(round(lows[i],0))

alerts_list = ['']*4
for i in range(len(alerts)):
    if i > 4: break
    alerts_list[i] = alerts[i].description
#parsing atom feed from meteoalarm

d = feedparser.parse('http://www.meteoalarm.eu/ATOM/PL.xml')
k=0
atom = ['']*5
for i in range(0,len(d.entries)):
    if (d.entries[i].title.find('Raciborski'))> 1 and  (d.entries[i].title.find('Red')) > -1:
        if k < 3: atom [k] =d.entries[i].title
        k=k+1
for i in range(0,len(d.entries)):
    if (d.entries[i].title.find('Raciborski'))> 1 and  (d.entries[i].title.find('Orange')) > -1:
        if k < 3: atom [k] =d.entries[i].title
        k=k+1
for i in range(0,len(d.entries)):
    if (d.entries[i].title.find('Raciborski'))> 1 and  (d.entries[i].title.find('Yellow')) > -1:
        if k < 3: atom [k] =d.entries[i].title
        k=k+1


Precip_Probability = [None]*2
if by_day.data[0].precipProbability > 0 :
    Precip_Probability[0] = str(int(round(100*(by_day.data[0].precipProbability))))+'%'
    if int(round(100*(by_day.data[0].precipProbability))) < 40 : Precip_Probability[0] = ''

Precip_Accumulation = [None]*2
if by_day.data[0].precipAccumulation > 0 :
    Precip_Accumulation[0] = str(int(round(by_day.data[0].precipAccumulation)))+'cm'
    if int(round(by_day.data[0].precipAccumulation)) < 1 : Precip_Accumulation[0] = ''

Description = ['']*4
if by_day.summary > 0 :
    for i in range (by_day.summary.rsplit(',',2).__len__()):
        Description[i]=by_day.summary.rsplit(',',2)[i]
#WIND ICON DECISION
wind_speed =''
wind_speed = str(int(round(by_day.data[0].windSpeed)))+'m/s'

print atom[0]
print atom[1]
print atom[2]
print (icons)
print (highs)
print (lows)
#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('ds-weather-script-preprocess.svg', 'r', encoding='utf-8').read()

#insert decription
output = output.replace('D0_DESCRIPTION:',Description[0])
output = output.replace('D1_DESCRIPTION:',Description[1])
output = output.replace('PROBAB:',Precip_Probability[0])
output = output.replace('ACCUM:',Precip_Accumulation[0])
output = output.replace('HIGH_TIME:',highs_time[0])
output = output.replace('LOW_TIME:',lows_time[0])

if int(round(by_day.data[0].windSpeed)) > 10:
    output =output.replace('ICON_FIVE','wind')
    output =output.replace('xxms',wind_speed)
else:
    output = output.replace('xxms','')

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątunio', 'Sobocia', 'Niedziela']
output = output.replace('DAY_ONE:',days_of_week[today.weekday()] + '   ' + by_day.data[1].time.strftime("%d/%m")).replace('DAY_TWO',days_of_week[by_day.data[2].time.weekday()]).replace('DAY_THREE',days_of_week[by_day.data[3].time.weekday()]).replace('DAY_FOUR',days_of_week[by_day.data[4].time.weekday()])

#insert Atom Warning

#output = output.replace('ATOM:',alerts_list[0]).replace('ATOM1:',alerts_list[1]).replace('ATOM2:',alerts_list[2])
output = output.replace('ATOM:',atom[0]).replace('ATOM1:',atom[1]).replace('ATOM2:',atom[2])
#insert time stamp
output = output.replace('GEN_TIME',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

t=1
