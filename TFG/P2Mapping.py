from djitellopy import tello
import KeyPressModule as kp
import numpy as np
import cv2
import math
from time import sleep

############# PARAMETERS #############
fSpeed = 16.5/10  #Velocidad lineal reeal
aSpeed = 36  #Velocidad angular real
interval = 0.25  #Intervalo de tiempo

dInterval = fSpeed * interval  #Distancia recorrida durante un intervalo
aInterval = aSpeed * interval  #Grados girados durante un intervalo
x, y = 500, 500 #x0 y0
a = 0
yaw = 0

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0, 0), (0, 0)]

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    aspeed = 50 #Velocidad angular teórica
    speed = 15  #Velocidad lineal teórica
    global x, y, yaw, a
    d = 0

    if kp.getKey("LEFT") and kp.getKey("UP"):
        a = 135
        fb = speed
        lr = -speed
        d = dInterval
    elif kp.getKey("RIGHT") and kp.getKey("UP"):
        a = 45
        fb = speed
        lr = speed
        d = dInterval
    elif kp.getKey("LEFT") and kp.getKey("DOWN"):
        a = 225
        fb = -speed
        lr = -speed
        d = dInterval
    elif kp.getKey("RIGHT") and kp.getKey("DOWN"):
        a = 315
        fb = -speed
        lr = speed
        d = dInterval

    else:

        if kp.getKey("LEFT"):
            lr = -speed
            d = dInterval
            a = 180

        elif kp.getKey("RIGHT"):
            lr = speed
            d = dInterval
            a = 360

        if kp.getKey("UP"):
            fb = speed
            d = dInterval
            a = 90

        elif kp.getKey("DOWN"):
            fb = -speed
            d = dInterval
            a = 270

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        print("Entro")
        yv = -aspeed
        yaw += aInterval

    elif kp.getKey("d"):
        yv = aspeed
        yaw -= aInterval

    if kp.getKey("q"): me.land()
    if kp.getKey("e"): me.takeoff()
    sleep(interval)

    #Sumatorio de las posiciones
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(-1 * d * math.sin(math.radians(a)))
    print(a)

    return[lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED) #Circulos rojos para cada punto

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED) #Circulo verde para posición actual
    cv2.putText(img, f'({(points[-1][0]- 500)/100},{(points[-1][1]- 500)/100})m',
                (points[-1][0]+10, points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8) #Creación imagen negra (mapa) como matriz de 0
    # y valores iran de 0 a 256 (2^8) como integers sin signo.
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]): #Solo dibuja si se mueve
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)



