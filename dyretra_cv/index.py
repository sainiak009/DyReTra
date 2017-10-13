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

# with open('config/road_config.json') as json_file:
with open('dyretra_cv/config/road_config.json') as json_file:
    roads = json.load(json_file)['roads']
    num_of_roads = len(roads)

snapshot = cv2.imread("dyretra_cv/inputs/traffic.png", -1)
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
    # cv2.imshow('snapshot', res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    minLineLength = 50
    maxLineGap = 50
    lines = cv2.HoughLinesP(gray,5,np.pi/180,500, minLineLength = minLineLength, maxLineGap = maxLineGap)
    for linest in lines:
        for x1,y1,x2,y2 in linest:
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,255),2)
    snapshot_res.append(lines)
# cv2.imshow('snapshot', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
print(snapshot_res)

exclude = []
for i in range(0, num_of_roads) :
    exclude.append(-1);

for color in range(0, len(colors)) :
    result_set = snapshot_res[color]
    # print(result_set)
    for result_line in result_set :
        result_line = result_line[0]
        # print(result_line)

        if result_line[0]-result_line[2] == 0.0:
            result_line_th = 90.0
            result_line_d = result_line[0]
        else:
            result_line_m = ((result_line[1]-result_line[3])/(result_line[0]-result_line[2]))
            result_line_th = math.degrees(math.atan2(result_line[1]-result_line[3], result_line[0]-result_line[2]))
            result_line_d = (result_line_m*result_line[0] - result_line[1])/math.sqrt(result_line_m**2 + 1)

        if result_line_th < 0.0 :
            result_line_th = 180.0 + result_line_th
        if result_line_th == 180.0 :
            result_line_th = 0.0
        # print str(result_line_th) + " and " + str(result_line_d)

        for road_index in range(0, len(roads)) :
            if exclude[road_index] != -1 :
                continue
            road = roads[road_index]

            if road[0]-road[2] == 0.0:
                road_th = 90.0
                road_d = road[0]
            else:
                road_m = ((road[1]-road[3])/(road[0]-road[2]))
                road_th = math.degrees(math.atan2(road[1]-road[3], road[0]-road[2]))
                road_d = (road_m*road[0] - road[1])/math.sqrt(road_m**2 + 1)

            if road_th < 0.0 :
                road_th = 180.0 + road_th
            if road_th == 180.0 :
                road_th = 0.0
            # print str(road_th) + " and " + str(road_d)

            if math.fabs(result_line_th - road_th) < 1.0 and math.fabs(result_line_d - road_d) < 1.0 :
                exclude[road_index] = color

print exclude
