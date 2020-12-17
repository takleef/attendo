import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from tkinter import *
# import mysql.connector

# mydb = mysql.connector.connect(
  # host="localhost",
  # user="Attendo",
  # password="teamattendo@vit567",
  # database="csv_db 6"
# )

# mycursor = mydb.cursor()

window = tk.Tk()
window.title("Attendo")
window.iconbitmap('.data/icon.ico')
window.configure(background='navajo white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


canvaslogo=Canvas(window, width=200, height=180, bg="black", highlightthickness=0)
canvaslogo.pack()
logo1 = tk.PhotoImage(file=".data/logo.ppm")
canvaslogo.create_image(0,0, anchor=NW, image=logo1)
#logoimage = tk.Label(
    #window, image=logo1).pack(side="center")
#logoimage.place(x=0, y=0)

#logo = tk.Label(
    #text="ATTENDO",
    #bg="black", fg="deep sky blue", font=('times', 40, 'bold'))
#logo.place(x=530,y=0)

message = tk.Label(
    text="Developors : Yash Jungade | Kartik Bodhankar | Shubham Dalvi | Raj Khetale\nMentor : Prof. Nisy Mathew | Deptartment of Electronics VIT",
    bg="navajo white", fg="navy", font=('times', 10, 'bold'))
message.place(x=430,y=620)

message1 = tk.Label(
    text="Face Recognition Attendance System",
    bg="navajo white", fg="red", width=30,
    font=('times', 40, 'bold'))
message1.place(x=170, y=180)

message2 = tk.Label(
    window, text="Vidyalankar Institute of Technology",
    bg="navajo white", fg="navy", width=40,
    height=2, font=('times', 30, 'bold'))

message2.place(x=170, y=245)

message3 = tk.Label(
    window, text="Welcome\nHave A Good Day!",
    bg="navajo white", fg="navy", width=40,
    height=2, font=('times', 30, 'bold'))

message3.place(x=170, y=405)

#from PIL import ImageGrab

path = '.users'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    print('Encoding...')
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('.csv/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            nameList.append(entry[1])
        if name not in nameList or x not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{x},{dtString}')
            # sql = "INSERT INTO `attendance` (`Name`,`Date`,`Time`) VALUES (%s,%s,%s)"
            # val = (row.Name, row.x, row.dtstring)
            # mycursor.execute(sql, val)
            # print(mycursor)
            # mydb.commit()

now = datetime.now()
x = now.strftime('%d %B %Y')

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
#def captureScreen(bbox=(300,300,690+300,530+300)):
#   capScr = np.array(ImageGrab.grab(bbox))
#  capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
# return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

def Recognize():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            if np.any (faceDis < 0.5):
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    print("Welcome "+name+"\nHave A Good Day!")
                    message4 = tk.Label(
                        window, text=str(name),
                        bg="navajo white", fg="red",
                        width="40",
                        font=('times', 30, 'bold'))

                    message4.place(x=170, y=350)

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (50, 50, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 0, 0), 2)
                    markAttendance(name)
                else:
                    print('Unknown Face')
        cv2.imshow('Face Recognition Attendance System', img)
        cv2.waitKey(1)
        c = cv2.waitKey(1)
        if c == 27 or c == 10:
            break
            cv2.destroyAllWindows()
            cap.release()

        # if ord(getch(a)):
             # cv2.waitKey(2000)
             # cv2.destroyAllWindows()
             # cap.release()

recognizeButton = tk.Button(window, text="Recognize",
                     command=Recognize, fg="navy", bg="khaki",
                     width=20, height=3, activebackground="khaki",
                     font=('times', 15, ' bold '))
recognizeButton.place(x=520, y=525)

window.mainloop()