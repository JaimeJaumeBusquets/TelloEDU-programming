import cv2
from HandsTrackingModule import HandDetector
from djitellopy import tello
import time

"Parámetros"
w, h = 720, 480
lengths = []
centers = []
speed = 40
tiempoFoto = 0.0
Stop = False #Flag para detener el drone

"Conexión al Tello"
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
me.takeoff()
me.move_up(60)

detector = HandDetector(mode=False, minTrackCon=0.8, detectionCon=0.8, maxHands=2)

while True:
    img = me.get_frame_read().frame
    hands, img = detector.findHands(img) #Encontrar manos

    if hands and not Stop:
        #Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"] #List of 21 Landmark points
        centerPoint1 = hand1["center"]  #Center of the hand cx, cy

        fingers1 = detector.fingersUp(hand1) #Dedos levantados
        "Aterrizar"
        if fingers1 == [0, 1, 1, 1, 0]:
            me.land()
        else:
            pass

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            centerPoint2 = hand2["center"]

            fingers2 = detector.fingersUp(hand2)

            length, info = detector.findDistance(centerPoint1, centerPoint2) #Para acercar/alejar/derecha/izquierda
            lengthPhoto, inf = detector.findDistance(lmList1[4], lmList2[4]) #Para tomar foto

            lengths.append(length)
            centers.append(info[4]) #componente x del centro

            "Movimiento delante/detrás y derecha/izquierda"
            if len(lengths) > 1 and fingers1 == [1, 1, 1, 1, 1] and fingers2 == [1, 1, 1, 1, 1]:
                if abs(lengths[len(lengths)-1] - lengths[len(lengths)-2]) >= \
                        abs(centers[len(centers) - 1] - centers[len(centers) - 2]): #Solo quiero que haga 1 de los dos mov.
                    if lengths[len(lengths)-1] < lengths[len(lengths)-2] - 2:
                        me.send_rc_control(0, speed, 0, 0)
                    elif lengths[len(lengths)-1] > lengths[len(lengths)-2] + 2:
                        me.send_rc_control(0, -speed, 0, 0)
                    else:
                        me.send_rc_control(0, 0, 0, 0)
                else:
                    if centers[len(centers)-1] < centers[len(centers)-2] - 2:
                        me.send_rc_control(-speed, 0, 0, 0)
                    elif centers[len(centers)-1] > centers[len(centers)-2] + 2:
                        me.send_rc_control(speed, 0, 0, 0)
                    else:
                        me.send_rc_control(0, 0, 0, 0)
            else:
                pass

            "Movimiento arriba/abajo"
            if fingers1 == [0, 1, 0, 0, 0] and fingers2 == [0, 1, 0, 0, 0]:
                me.send_rc_control(0, 0, speed, 0)
            elif fingers1 == [0, 1, 1, 0, 0] and fingers2 == [0, 1, 1, 0, 0]:
                me.send_rc_control(0, 0, -speed, 0)
            else:
                pass

            "Tomar foto a los 5 segundos"
            if lengthPhoto < 20 and fingers1 == [1, 0, 0, 0, 1] and fingers2 == [1, 0, 0, 0, 1]:
                Stop = True
                tiempoFoto = int(time.time()) #momento del gesto
            else:
                pass
        else:
            me.send_rc_control(0, 0, 0, 0)
    else:
        me.send_rc_control(0, 0, 0, 0)

    if int(time.time()) == tiempoFoto + 5:
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(1)
        Stop = False

    else:
        pass

    img = cv2.resize(img, (w, h))
    cv2.imshow("Image", img)
    cv2.waitKey(1)


