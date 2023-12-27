import matplotlib.pyplot as plt
import numpy as np


def plot2(data, location):
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


