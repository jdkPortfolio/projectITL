import cv2
import time
from csv import writer
import pandas as pd


led_red = 13
led_amber = 12
led_green = 11

led_red_ = 10
led_amber_ = 9
led_green_ = 8
port = 'COM12'

# timing based on vehicle volumes
def calculate_delays(countAB, countC, objectPerSecond):
    boon = ''
    delayAB = countAB * objectPerSecond
    delayC = countC * objectPerSecond

    if delayAB < 10:
        delayAB = 10
    if delayAB > 30:
        delayAB = 30
    if delayC < 10:
        delayC = 10
    if delayC > 30:
        delayC = 30
    if delayC == 0:
        delayC = 5
    if delayAB == 0:
        delayAB = 5
    if delayAB > delayC:
        boon = 0
    if delayC > delayAB:
        boon = 2
    if delayAB == delayC:
        boon = 1
    if delayAB == 10 and delayC > 10:
        delayC = 50
    if delayC == 10 and delayAB > 10:
        delayAB = 50
    if delayAB > 10 and delayAB < 30 and delayC > 10:
        delayC = 60 - delayAB
    if delayC > 10 and delayC < 30 and delayAB > 10:
        delayAB = 60 - delayC

    return delayAB, delayC, boon


def count_vehicles(terminate, cam):
    #loading video of traffic
    cap = cv2.VideoCapture(cam)

    #object detector used to extract moving objects
    #history attribute increases precision of object detection
    #varthreshold reduces false positives
    object_detector = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=100)

    vehicle_counter = 0
    #looping 
    while True:
        #creating object reading the video
        ret, frame = cap.read()

        #extraction of region of interest
        height, width, _ = frame.shape
        region = frame[300:500,50:600]
        #creating mask that shows the objects that are required
        mask = object_detector.apply(frame)

        #cleaning mask, removing shadows
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        
        #extracting boundaries of the moving objects from mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #iterating through the contours
        detections = []
        for cnt in contours:
            #calculating area and eliminating small elements
            area = cv2.contourArea(cnt)
            #drawing contours on objects
            
            if area > 750:
                #cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                #extracting values for drawing rectangle on object
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)

                detections.append([x,y,w,h])

                #middle points
                xMid = int((x + (x+w))/2)
                yMid = int((y + (y+h))/2)
                cv2.circle(frame, (xMid, yMid), 5, (0, 255, 0), 5 )

                if yMid > 600 and yMid < 620:
                    vehicle_counter += 1
        
        # box_ids = tracker.update(detections)
        # for box_id in box_ids:
        #     x, y, w, h, id = box_id
        #     vehicle_counter = vehicle_counter + 1


        #showing threshold line
        cv2.line(frame, (70,600), (600, 600), (0,0,255), 2)#red line
        # showing vehicle counting 
        # cv2.putText(frame, 'Total Vehicles : {}'.format(vehicle_counter), (250, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        #showing frame
        cv2.imshow('Frame', frame)
        
        
        # cv2.imshow('Mask', mask)
        # #showing region of interest
        # cv2.imshow('Region', region)   


        #using a key to break loop eg. esc
        key = cv2.waitKey(30)
        sec = time.localtime().tm_sec
        # print(terminate)
        if sec == terminate:
            sec = time.localtime().tm_sec
            break

    cap.release()
    cv2.destroyAllWindows()

    vehicle_counter = int((vehicle_counter/3.3)*2)

    return vehicle_counter


def controller(board, index, delay_endsAB, delay_endC, endCcam, endABcam):
    #high to green
    # board.digital[led_green].write(1)
    terminate = time.localtime().tm_sec + delay_endsAB[index]
    if terminate > 59:
        terminate = terminate - 60
    endsCcount = count_vehicles(terminate, endCcam)
    # endsCcount = int((endsCcount/3.3)*2.7)
    # return endsCcount
    #low to green
    # board.digital[led_green].write(0)
    #high to amber
    # board.digital[led_amber].write(1)
    # time.sleep(2)
    # #    #low to amber
    # board.digital[led_amber].write(0)
    # #    #high to red
    # board.digital[led_red].write(1)
    #     low to red_
    # board.digital[led_red_].write(0)
    #     #high to green_
    # board.digital[led_green_].write(1)
    terminate = time.localtime().tm_sec + delay_endC[index]
    if terminate > 59:
        terminate = terminate - 60
    #counting vehicles
    endsABcount = count_vehicles(terminate, endABcam)
    # endsABcount = int((endsABcount/3.3)*2.7)
    #     #low to green_
    # board.digital[led_green_].write(0)
    #     #high to amber_
    # board.digital[led_amber_].write(1)
    # time.sleep(5)
    #     #low to amber_
    # board.digital[led_amber_].write(0)
    #     #high to red_
    # board.digital[led_red_].write(1)
    #low to red
    # board.digital[led_red].write(0)

    return endsABcount, endsCcount

def logTrafficStats(file, endC, endAB, endCdelay, endABdelay, boon):
    hour = time.localtime().tm_hour
    data = pd.DataFrame([[hour, endC, endAB, endCdelay, endABdelay, boon]], columns = ['hour', 'endC', 'endAB', 'endCdelay', 'endABdelay', 'preffered'])

    # with pd.ExcelWriter('data.xlsx', mode='a', if_sheet_exists='replace') as writer:
    #     data.to_excel(writer, sheet_name='Sheet1')
    data.to_csv('data.csv', mode='a', index=False, header=None)
    

## term = time.localtime().tm_sec + 30
## val = count_vehicles(term, 'A.mp4')
## print(val)