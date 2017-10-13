import cv2
import numpy as np
import json
import math

colors = [
    [60, 100, 100, 60, 255, 255, 30],
    [22, 255, 241, 22, 255, 243, 10],
    [0, 255, 236, 0, 255, 237, 10],
    [0, 255, 160, 0, 255, 165, 10]
]

with open('config/node_config.json') as json_file:
    roads = json.load(json_file)['roads']


snapshot = cv2.imread("inputs/traffic2.png", -1)
snapshot_hsv = cv2.cvtColor(snapshot, cv2.COLOR_BGR2HSV)
snapshot_res = []
road_data = []

for color in colors :
    frame = snapshot
    hsv = snapshot_hsv

    lower_limit = np.array([color[0] - color[6], color[1], color[2]])
    upper_limit = np.array([color[3] + color[6], color[4], color[5]])

    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    minLineLength = 50
    maxLineGap = 50
    lines = cv2.HoughLinesP(gray,5,np.pi/180,1000, minLineLength = minLineLength, maxLineGap = maxLineGap)
    snapshot_res.append(lines)

# print snapshot_res

for (road1, road2) in roads :

    if road1[0]-road1[2] == 0:
        road1_th = 90
        road1_d = road1[0]
    else:
        road1_m = ((road1[1]-road1[3])/(road1[0]-road1[2]))
        road1_th = math.degrees(math.atan(road1_m))
        road1_d = (road1_m*road1[0] - road1[1])/math.sqrt(road1_m**2 + 1)

    if road2[0]-road2[2] == 0:
        road2_th = 90
        road2_d = road2[0]
    else:
        road2_m = ((road2[1]-road2[3])/(road2[0]-road2[2]))
        road2_th = math.degrees(math.atan(road2_m))
        road2_d = (road2_m*road2[0] - road2[1])/math.sqrt(road2_m**2 + 1)

    road1_sig = -1
    road2_sig = -1

    for color_i in range(0, len(snapshot_res)) :
        road_data_temp = []
        for cv_temp in snapshot_res[color_i] :
            cv_road = cv_temp[0]

            if cv_road[0]-cv_road[2] == 0:
                cv_road_th = 90
                cv_road_d = cv_road[0]
            else:
                cv_road_m = ((cv_road[1]-cv_road[3])/(cv_road[0]-cv_road[2]))
                cv_road_th = math.degrees(math.atan(cv_road_m))
                cv_road_d = (cv_road_m*cv_road[0] - cv_road[1])/math.sqrt(cv_road_m**2 + 1)

            if math.fabs(cv_road_th - road1_th) < 5 and math.fabs(cv_road_d - road1_d) == 0 :
                road1_sig = color_i
            if math.fabs(cv_road_th - road2_th) < 5 and math.fabs(cv_road_d - road2_d) == 0 :
                road2_sig = color_i
    road_data_temp.append(road1_sig)
    road_data_temp.append(road2_sig)
    road_data.append(road_data_temp)
print road_data
