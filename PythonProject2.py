import cv2 as cv2
import numpy as np
import xlsxwriter

# To start camera/camera

capVideo = cv2.VideoCapture('video.mp4')
capVideo.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capVideo.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

lineLength = 600
#lets code an algo
history =100
threshold = 200

carAlgo = cv2.createBackgroundSubtractorMOG2(history, threshold)
min_rectangle_with =80
min_rectangle_hight =80

workbook = xlsxwriter.Workbook('arbaj.xlsx')
worksheet = workbook.add_worksheet()



def centerPoint(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


detectVehcle = []

offest =6
count1 =0

while True:


    ret, frame1 = capVideo.read()
    width = int(capVideo.get(3))
    height = int(capVideo.get(4))




    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3),5)
    img_sub = carAlgo.apply(blur)
    dillat = cv2.dilate(img_sub, np.ones((5,5)))
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dillData = cv2.morphologyEx(dillat, cv2.MORPH_CLOSE, kernal)
    dillData = cv2.morphologyEx(dillData, cv2.MORPH_CLOSE, kernal)
    countVehcal, h=  cv2.findContours(dillData, cv2.RETR_TREE, cv2. CHAIN_APPROX_SIMPLE)

    #If we pass dilladat in (imshow then it will provide grey effect)
    #to draw a line on the videoView
    cv2.line(frame1,(25, lineLength), (1400, lineLength), (255,127,0),3)

    for (i,c) in enumerate (countVehcal):
        #w=width , z= hight;
        (x,y,w,h) = cv2.boundingRect(c)
        vd_count = (w>=min_rectangle_with) and (h>=min_rectangle_hight)
        if not vd_count:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame1, "Vehicle"+str(count1), (x,y-20),  cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4 )
        count = centerPoint(x, y, w, h)
        detectVehcle.append(count)

        cv2.circle(frame1, count, 4, (0, 0, 255), -1)


        for(x,y) in detectVehcle:
            if y<(lineLength+offest) and y>(lineLength-offest):
                count1+= 1
                cv2.line(frame1,(25, lineLength), (1400, lineLength), (0,127,255),3)
                detectVehcle.remove((x,y))
                txt = "Vehical Counter:"+str(count1)
                print(txt)

                #To print value in excel sheet
                row_num = 0
                # for key in str(count):
                #     worksheet.write(key)
                #     worksheet.write_row(row_num)
                #     row_num += 1




    cv2.putText(frame1,"Vehical "+ str(count1), (450,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),4)



    cv2.imshow('Vehical Count', frame1)

    if cv2.waitKey(1)==13:

        break

cv2. destroyAllWindows()
capVideo.release()