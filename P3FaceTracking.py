import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 20, 0)
time.sleep(1.2)

"Definición parámetros"
w, h = 360, 240
fbRange = [4500, 4800] #Rango de áreas donde el drone no avanzará o retrocederá
pid = [0.4, 0.4, 0] #0.4 P, 0.4 D, 0 I
pid2 = [0.008, 0.008, 0] #0.008 P, 0.008 D, 0 I
pError = 0
pErrorFB = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  #Detecta objetos y los retorna como una lista de rectángulos.

    myFaceListC = [] #Creación lista de centros de caras
    myFaceListArea = [] #Creación lista de áreas

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2) #Rectángulo rojo que marque la cara
        cx = x + w//2
        cy = y + h//2
        area = w*h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED) #Circulo verde que marque el centro de la cara
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea)) #Únicamente queremos la cara más cercana
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(me, info, w, pid, pid2, pError, pErrorFB):
    area = info[1]
    x, y = info[0]
    fb = 0
    ud = 0

    "Cálculo de la yaw speed dependiendo del error de centrado actual y anterior"
    error = x - w//2 #Que lejos esta el centro de la cara del centro de la imagen
    speed = pid[0] * error + pid[1]*(error - pError)
    speed = int(np.clip(speed, -50, 50)) #min. fijado a -50 y max. a 50

    "Cálculo de la fb speed dependiendo del error de area actual y anterior"
    if area < fbRange[0]:
        errorFB = fbRange[0] - area
    elif area > fbRange[1]:
        errorFB = fbRange[1] - area
    else:
        errorFB = 0

    speedFB = pid2[0] * errorFB + pid2[1]*(errorFB - pErrorFB)
    speedFB = int(np.clip(speedFB, -50, 50))

    if x == 0:
        speed = 0
        error = 0
        speedFB = 0

    me.send_rc_control(0, speedFB, 0, speed)
    return error, errorFB

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h)) #Queremos el tamaño de la imagen igual que el definido (w, h) para calcular el centrado
    img, info = findFace(img)
    pError, pErrorFB = trackFace(me, info, w, pid, pid2, pError, pErrorFB)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
