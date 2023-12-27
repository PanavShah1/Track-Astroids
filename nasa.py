# SBDB Close-Approach Data API


import math
import requests
from timezones import timezones
from month_num import convert
import numpy as np
import matplotlib.pyplot as plt

api_key_nasa = 'hfz8qUHYMu6nzUtoTdNhetcpFmMGnebYgthqDzCm'


location = 'Asia/Calcutta'
date_min = '2023-12-25' # 2023-12-10


date_max = '-'.join([date_min.split('-')[0], date_min.split('-')[1], f'{int(date_min.split("-")[2]) + 1:02}']) 
response = requests.get('https://ssd-api.jpl.nasa.gov/cad.api', params= {f'date-min': {date_min}, 'date-max': {date_max}})
   
# print(response)

data = []


time = []

if response.status_code == 200:
    track_data = response.json()
    count = track_data['count']
    data = [0 for i in range(0, count)]
    # print(track_data['fields'])
    print()

    for i in range(count):
        name = track_data['data'][i][0]
        time1 = track_data['data'][i][3]
        v_rel = track_data['data'][i][7]
        # print(v_rel)
        v_inf = track_data['data'][i][8]
        v_esc = math.sqrt(math.pow(float(v_rel), 2) - math.pow(float(v_inf), 2))
        dist_min = track_data['data'][i][5]
        #print(dist_min)
        # print(track_data['data'][i])
        # print(v_esc)

        time1 = time1.split('-')
        time1[1] = convert(time1[1])
        # print(time1)
        time='-'.join(time1)+':00'

        data[i]={'v_rel' : v_rel, 'v_inf' : v_inf, 'v_esc' : v_esc, 'dist_min' : dist_min, 'time_gmt' : time, 'name' : name}
else:
    print('Error')



def au_to_km(au):
    return round(149597870.7*float(au))
def v_esc_to_v_earth(v_esc):
    return math.sqrt(float(v_esc)*float(v_esc)*1000000+62563000) # m/s

  



for i in range(count):
    time_response = requests.post('https://timeapi.io/api/Conversion/ConvertTimeZone', json={
        "fromTimeZone": f"{location}",
        "dateTime": f"{data[i]['time_gmt']}",
        "toTimeZone": "America/Los_Angeles",
        "dstAmbiguity": ""
    })
    # print(time_response.json())
    if time_response.status_code == 200:
        track_data = time_response.json()
        data[i].update({'time' : track_data['conversionResult']['time']})

    data[i].update({'dist_min_km' : au_to_km(data[i]['dist_min'])})
    data[i].update({'v_earth' : v_esc_to_v_earth(data[i]['v_inf'])})

for i in range(count):
    print(str(i+1)+' :')
    print(f'Name : {data[i]['name']}')
    print(f"Time at which it's closest to Earth in {location} : {data[i]['time']}")
    print(f'Minimum distance from Earth : {int(data[i]['dist_min_km']):,} km')
    print(f'Speed : {float(data[i]['v_rel'])*1000:.2f} m/s')
    print(f"Speed at which it would've hit Earth : {data[i]['v_earth']:.2f} m/s")
    print()













# data = [{'v_rel': '11.1631243029374', 'v_inf': '11.152532905294', 'v_esc': 0.4861625234077133, 'dist_min': '0.0224990531551792', 'time_gmt': '2023-12-21 08:27:00', 'name': '2023 YB', 'time': '18:57', 'dist_min_km': 3365810, 'v_earth': 13672.673118438304}, {'v_rel': '13.0589694131149', 'v_inf': '13.0546255594802', 'v_esc': 0.336799101003512, 'dist_min': '0.0469784501784903', 'time_gmt': '2023-12-21 10:59:00', 'name': '2018 YJ2', 'time': '21:29', 'dist_min_km': 7027876, 'v_earth': 15263.887070410135}]

# print(data)
plt.figure(figsize=(10, 10), dpi = 100)
ax = plt.subplot(projection='polar')
r = [10, 10, 10, 10, 10, 10, 10, 10]
theta = np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315])
# ax.plot(theta, r)
ax.plot(0, 0, markersize = 12, marker = 'o', color= 'blue')
# ax.set_yticklabels([])
ax.set_xticklabels([])
# ax.arrow(0, 0, 0, 1, width= 0.1, head_width= 0.3)
ax.text(80*3.14159/180, 7, f'{location} is facing towards the right\n\nScale : 1 = 1 mil km', style='italic',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

# ax.set_rticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# ax.plot(3.14, 3, markersize = 10, marker = 'o', color= 'red')

def time_to_angle(time): #18:57
    hour, min = time.split(':')
    angle = float(hour)/24*360 + float(min)/60*15
    return angle



for i in range(len(data)):
    data[i]['angle'] = time_to_angle(data[i]['time'])*3.14159*2/360
    # print(data[i]['angle']*360/3.14159/2)
    data[i]['distance'] = data[i]['dist_min_km']/1000000
    ax.plot(data[i]['angle'], data[i]['distance'], markersize = 5, marker = 'o', color= 'red')
    ax.annotate(data[i]['name'], (data[i]['angle'], data[i]['distance']))
   


plt.show()





