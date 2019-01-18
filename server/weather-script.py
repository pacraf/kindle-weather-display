# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import codecs
import datetime
from pyowm import OWM , timeutils


API_key = 'xxxxxxxxxxxxxxxx'
owm = OWM(API_key)
#obs = owm.weather_at_id(xxxx)
#w=obs.get_weather()

fc = owm.three_hours_forecast_at_id(7532706)

f=fc.get_forecast()
f.get_reception_time('iso')
f.get_location()

lst =f.get_weathers()

# for weather in f:
#     print(weather.get_reference_time('iso'),weather.get_status(), weather.get_temperature('celsius'))

today = timeutils.now()
#today_12 = today.replace(hour=12)
#today_12 = today
if fc.when_starts('date').hour < 10 :
    today_12 = today.replace(hour=12)
else:
    today_12 = today.replace(hour=fc.when_starts('date').hour)

#today_22 = today.replace(hour=22)
if fc.when_starts('date').hour < 20 :
    today_22 = today.replace(hour=22)
else:
    today_22 = today.replace(hour=fc.when_starts('date').hour)

day_two_12 = timeutils.tomorrow(12,00)
day_two_22 = timeutils.tomorrow(22,00)
day_three_12 = timeutils._timedelta_days(2).replace(hour=12)
day_three_22 = timeutils._timedelta_days(2).replace(hour=22)
day_four_12 = timeutils._timedelta_days(3).replace(hour=12)
day_four_22 = timeutils._timedelta_days(3).replace(hour=22)

icons = [None]*4
icons = [fc.get_weather_at(today_12).get_weather_icon_name(),fc.get_weather_at(day_two_12).get_weather_icon_name(),fc.get_weather_at(day_three_12).get_weather_icon_name(),fc.get_weather_at(day_four_12).get_weather_icon_name()]

icons_text = [None]*4
icons_text = [fc.get_weather_at(today_12).get_status(),fc.get_weather_at(day_two_12).get_status(),fc.get_weather_at(day_three_12).get_status(),fc.get_weather_at(day_four_12).get_status()]


highs = [None]*4
highs = [fc.get_weather_at(today_12).get_temperature('celsius').get('temp_max'),fc.get_weather_at(day_two_12).get_temperature('celsius').get('temp_max'),fc.get_weather_at(day_three_12).get_temperature('celsius').get('temp_max'),fc.get_weather_at(day_four_12).get_temperature('celsius').get('temp_max')]
for i in range(len(highs)):
    highs[i]= int(round(highs[i],0))

lows = [None]*4
lows = [fc.get_weather_at(today_22).get_temperature('celsius').get('temp_min'),fc.get_weather_at(day_two_22).get_temperature('celsius').get('temp_min'),fc.get_weather_at(day_three_22).get_temperature('celsius').get('temp_min'),fc.get_weather_at(day_four_22).get_temperature('celsius').get('temp_min')]
for i in range(len(lows)):
    lows[i]= int(round(lows[i],0))
print fc.when_starts('date')
print (icons_text)
print (icons)
print (highs)
print (lows)

#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('owm-weather-script-preprocess.svg', 'r', encoding='utf-8').read()

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['PoniedziaĹ‚ek', 'Wtorek', 'Ĺšroda', 'Czwartek', 'PiÄ…tunio', 'Sobcia', 'Niedzielka']
output = output.replace('DAY_ONE',days_of_week[today_22.weekday()] + '   ' + timeutils.now().strftime("%d/%m/%y")).replace('DAY_TWO',days_of_week[day_two_12.weekday()]).replace('DAY_THREE',days_of_week[day_three_12.weekday()]).replace('DAY_FOUR',days_of_week[day_four_12.weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

