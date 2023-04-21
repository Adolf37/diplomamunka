#jol elkapott parameterek
#i.distance < 43
#if (n) % (fps+7) ==0:

import sqlite3
import cv2
import os.path
import os
import numpy as np 
from matplotlib import pyplot as plt

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(empId):
    vide_id = empId
    nev = ''
    try:
        sqliteConnection = sqlite3.connect('diplomamunka.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from videok where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0])
            video_bin = row[1]
            nev = row[2]
            
            print("Storing employee image and resume on disk \n")
            videoPath = "./" + nev + ".mp4"
            writeTofile(video_bin, videoPath)
            

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

    return (vide_id, nev)

def orb_sim(img1,img2):
    img1_g = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2_g = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    
    #detect keypoints and descriptors
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    #define the brutefore matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    #perform matches
    matches = bf.match(desc_a,desc_b)
    
    #looking for similar regions with distance < 50
    #goes from 0 to 100
    similar_regions = [i for i in matches if i.distance < 43]
    if len(matches) == 0:
        return 0
    return len(similar_regions)/len(matches)


path = './_elobe.mp4'
path2 = "./video60s.mp4"
check_file = os.path.isfile(path)
check_file2 = os.path.isfile(path2)

def allokepekVideobol(id, videoFile):
    if not os.path.exists('ImagesFromVideo'):
        os.makedirs('ImagesFromVideo')

    cam = cv2.VideoCapture('./' + videoFile + '.mp4')
    fps = int(cam.get(cv2.CAP_PROP_FPS))
    print(fps)
    n = 0
    i=0

    r,img1 = cam.read()
    #resize = cv2.resize(image, (#x-axis dimensions, #y-axis dimensions))
    ugyanaz = 0

    while True:
        
        ret, frame = cam.read()

        if ret:
            if (n) % (fps+7) ==0:
                similarity = orb_sim(img1, frame)
                similarity2 = "{:.2f}".format(similarity)
                print(similarity)

                if similarity >= 0.99:
                    if ugyanaz != 1:
                        path = "./ImagesFromVideo/id_" + str(id) + "_" + str(i) + ".jpg"
                        cv2.imwrite(path,img1)
                        ugyanaz = 1
                        i = i + 1
                else:
                    ugyanaz = 0  
                    
                #cv2.putText(frame,"Orb Similarity:" + str(similarity2),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Video',frame)
                cv2.imshow('Elozo',img1)

                diff = cv2.subtract(img1,frame)
                #cv2.imshow('Diff',diff)

                img1 = frame
                

            n = n + 1
            if cv2.waitKey(33) == 27:
                break

        else:
            break 

    cam.release()
    cv2.destroyAllWindows()


if check_file and check_file2:
    print('Megvan a video')
    allokepekVideobol(1,path.replace('.mp4',''))
    allokepekVideobol(2, path2.replace('.mp4', ''))
    
else:
    print('Video lekerese...')
    video_id, video_name = readBlobData(1)
    allokepekVideobol(video_id,video_name)
    print('Video lekerve, feldolgozas...')

    video_id,video_name = readBlobData(2)
    allokepekVideobol(video_id,video_name)
    print('Video lekerve, feldolgozas...')

    
    
    





