import math

def Movimiento(Colision, dInterval, speed, x, y, a, lr, fb):
    d = dInterval
    lado = 150
    pared = False

    if Colision:
        print("Colision!!")
        lr = -lr
        fb = -fb
        a = a + 180
    else:
        if 0 < x < lado and 0 < y < lado:
           pass
        else:
            pared = True
            if x <= 0:
                lr = speed
                a = (90 - a) + 90
            elif x >= lado:
                lr = -speed
                a = (90 - a) + 90
            if y <= 0:
                fb = speed
                a = (0 - a)
            elif y >= lado:
                fb = -speed
                a = (0 - a)

    # Sumatorio de las posiciones
    x += (d * math.cos(math.radians(a)))
    y += (d * math.sin(math.radians(a)))
    x = round(x, 2) #Redondeamos a 2 decimales
    y = round(y, 2)

    return [lr, fb, x, y, a, pared]

def Movimiento2(Colision, dInterval, speed,x2, y2, a2, lr2, fb2):
    lado = 150
    d = dInterval
    pared2 = False

    if Colision:
        lr2 = -lr2
        fb2 = -fb2
        a2 = a2 + 180
    else:
        if 0 < x2 < lado and 0 < y2 < lado:
            pass
        else:
            pared2 = True
            if x2 <= 0:
                lr2 = speed
                a2 = (90 - a2) + 90
            elif x2 >= lado:
                lr2 = -speed
                a2 = (90 - a2) + 90
            if y2 <= 0:
                fb2 = speed
                a2 = (0 - a2)
            elif y2 >= lado:
                fb2 = -speed
                a2 = (0 - a2)

    # Sumatorio de las posiciones
    x2 += (d * math.cos(math.radians(a2)))
    y2 += (d * math.sin(math.radians(a2)))
    x2 = round(x2, 2) #Redondeamos a 2 decimales
    y2 = round(y2, 2)

    return [lr2, fb2, x2, y2, a2, pared2]

def DistanciaDrones(points, points2):

    "Fórmula distancia entre dos puntos de un plano"
    distancia = math.sqrt((points2[-1][0] - points[-1][0])**2 + (points2[-1][1] - points[-1][1])**2)

    return distancia