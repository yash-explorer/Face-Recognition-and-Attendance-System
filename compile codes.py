
#                        PROJECT COMPLETED 100%              PROJECT BY YASH GIRADKAR



# Libraries Imported
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
import csv
import pymongo


path='image attendance'  #folder with sample images
images = []
classnames = []
mylist=os.listdir(path)
print(mylist) #get names
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])
print(classnames)
#print(help(face_recognition.face_encodings))


# Function to get Encodings of the sample faces
def find_encodings(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img,None)[0]
        encodelist.append(encode)
    print(encodelist)
    np.savetxt("data.csv",encodelist,delimiter=",")
    return encodelist

# Function to mark attendance
def mark_attendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList =f.readlines()
        namelist=[]
        for line in myDataList:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            date = str(now.date())
            f.writelines(f'\n{name},{dtstring},{date}')







encodelistknown = find_encodings(images) #Function Call
print(len(encodelistknown))
print(("Encoding Complete"))



cap=cv2.VideoCapture(0)

# Video Capture Start
while True:
    success, img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame =  face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches= face_recognition.compare_faces(encodelistknown,encodeFace)
        faceDist= face_recognition.face_distance(encodelistknown,encodeFace)
        print(faceDist)

        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            mark_attendance(name) # Call Function
        else:
            name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('webcam',img)
    k=cv2.waitKey(1) & 0xFF
    # press 'q' to exit
    if k == ord('q'):
        break
print("sucessfully terminated program")

df = pd.read_csv('Attendance.csv')
df=df.T
#dictionary as a document
dict = df.to_dict()

print(dict)

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb+srv://yash1:yash1@cluster0.txq9fum.mongodb.net/test")
# use database named "organisation"
#mydb = myclient["beginer"]
mydb = myclient["test"]

# use collection named "developers"
mycol = mydb["pain"]



# insert a document to the collection
x = mycol.insert_many(dict.values())

# id returned by insert_many not working
#print("Document inserted with id: ", x.inserted_id)

print("\nDocuments in pain collection\n----------------------------------")
# print all the documents in the collection
for x in mycol.find():
    print(x)


#now clear csv file
filename = "Attendance.csv"

# Read the data from the file
with open(filename, 'r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

# Remove all but the first row
data = [data[0]]

# Write the modified data back to the file
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)



#Yash Giradkar