import cv2
import mediapipe as mp
import math

class HandDetector:

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        """
        mode:
        Static Image Mode = False -> Si ya ha detectado, pasa a trackear y deja de detectar hasta que mintrackCon sea menor al epecificado.
        Static Image Mode = True -> Nunca deja de detectar.
        maxHands: Máx. número de manos a detectar
        detectionCon: Valor mínimo de confianza de detección.
        minTrackCon: Valor mínimo de confianza de trackeo
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.minTrackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20] #Landmarks de los extremos de cada dedo (FingersUp)
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        img: Imagen donde buscar las manos, solo funciona en modo BGR
        draw: ¿Queremos que se dibuje la detección de manos en la imagen?
        flipType: Si nuestra cámara captura en modo espejo o no
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Conversión a BGR
        self.results = self.hands.process(imgRGB) #Procesado de imágen para encontrar manos
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks: #¿Se ha detectado alguna landmark?
            for handType,handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand={}
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark): #Obtenemos el id de cada lm y su posicion (x, y)
                    px, py = int(lm.x * w), int(lm.y * h) #Pasamos de % de imagen a píxeles
                    mylmList.append([px, py])
                    xList.append(px)
                    yList.append(py)

                # Rectángulo alrededor de la mano
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else: myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) #Draw landmarks y conexiones
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2) #Draw del rectángulo
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30),cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2) #Marcar derecha o izquierda de la mano
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, myHand):
        "Recordar: self.tipIds = [4, 8, 12, 16, 20]"
        myHandType =myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            # Pulgar
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Otros 4 dedos
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img=None):
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1) #Hipotenusa
        info = (x1, y1, x2, y2, cx, cy)
        "Draw?"
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info
