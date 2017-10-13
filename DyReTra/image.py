import cv2
import numpy as np
import json
import math

from jsonParser import parseClusterData

colors = [
    [60, 100, 100, 60, 255, 255, 30],
    [22, 255, 241, 22, 255, 243, 10],
    [0, 255, 236, 0, 255, 237, 10],
    [0, 255, 160, 0, 255, 165, 10]
]

# Recieves the snapshot to process it and extracts meaningful data out of the image
# @param {Dictionary} Configuration data of working cluster
# @param {String} Image name
# @returns {List} List of Integers signifying Traffic Density

def getTrafficData(json_data, image = "default.png"):
    roads = parseClusterData(json_data)

    # Reads the Image and converts it to matrix
    snapshot = cv2.imread("trafficSnaps/" + image , -1)

    # Tries to convert the imaged to HSV from BGR
    try:
        snapshot_hsv = cv2.cvtColor(snapshot, cv2.COLOR_BGR2HSV)
    except Exception as e:
        print("CV2 Failure")
        exit()

    snapshot_res = []
    road_data = []

    for color in colors:
        frame = snapshot
        hsv = snapshot_hsv

        lower_limit = np.array([color[0] - color[6], color[1], color[2]])
        upper_limit = np.array([color[3] + color[6], color[4], color[5]])

        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        minLineLength = 50
        maxLineGap = 50

        # Uses Hough Lines Analysis to Detect Lines

        lines = cv2.HoughLinesP(gray, 5, np.pi / 180, 1000, minLineLength=minLineLength, maxLineGap=maxLineGap)
        snapshot_res.append(lines)

    # print (snapshot_res)

    # Iteration to extract data
    
    for road in roads:
        print(road)
        if road[0] - road[2] == 0:
            road_th = 90
            road_d = road[0]
        else:
            road_m = ((road[1] - road[3]) / (road[0] - road[2]))
            road_th = math.degrees(math.atan(road_m))
            road_d = (road_m * road[0] - road[1]) / math.sqrt(road_m ** 2 + 1)

        road_sig = -1

        for color_i in range(0, len(snapshot_res)):
            if snapshot_res[color_i] is not None :
                for cv_temp in snapshot_res[color_i]:
                    cv_road = cv_temp[0]

                    if cv_road[0] - cv_road[2] == 0:
                        cv_road_th = 90
                        cv_road_d = cv_road[0]
                    else:
                        cv_road_m = ((cv_road[1] - cv_road[3]) / (cv_road[0] - cv_road[2]))
                        cv_road_th = math.degrees(math.atan(cv_road_m))
                        cv_road_d = (cv_road_m * cv_road[0] - cv_road[1]) / math.sqrt(cv_road_m ** 2 + 1)

                    # Tests the proximity of Lines

                    if math.fabs(cv_road_th - road_th) < 5 and math.fabs(cv_road_d - road_d) == 0:
                        road_sig = color_i
        road_data.append(road_sig)
    # print(road_data)
    return road_data
