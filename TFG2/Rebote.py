from djitellopy import TelloSwarm
from time import sleep
import math

swarm = TelloSwarm.fromIps([
    "XXX.XXX.X.XXX",
    "XXX.XXX.X.XXX",
])

swarm.connect()


for tello in swarm:
    print(tello.get_battery())

swarm.takeoff()
sleep(2)


############# PARAMETERS #############
speed = 15
lado = 150 #Lado en cm del cuadrado
margen = 5 #margen de 5 cm antes de llegar a pared
x, y = margen + 0.5, margen + 0.5 #Posición inicial del drone1 en el cuadrado
x2, y2 = 149.5 - margen, margen + 0.5 #Posición inicial del drone2 en el cuadrado
Distancia = x2 - x
Colision = False
Inicio = True
points = [(x, y)] #Lista de posiciones drone1
points2 = [(x2, y2)] #Lista de posiciones drone2

fSpeed = 16.5 #Velocidad lineal real
interval = 0.25  #Intervalo de tiempo

dInterval = fSpeed * interval  #Distancia recorrida durante un intervalo

lr, fb = speed, speed
lr2, fb2 = -speed, speed
a = 45 #ángulo de mov. inicial drone1
a2 = 135 #ángulo de mov. inicial drone2

"""Movimiento """
def Movimiento(Colision):
    global x, y, lr, fb, lado, a, pared
    d = dInterval
    pared = False
    if Colision:
        "Si hay Colisión, el drone va a girar 180º"
        print("Colision!!")
        lr = -lr
        fb = -fb
        a = a + 180
    else:
        "Si no esta cerca de pared sigue"
        if (0 + margen) < x < (lado - margen) and (0 + margen) < y < (lado - margen):
           pass
        else:
            pared = True
            print("Pared en drone1")
            "Se aplican los angulos de rebote dependiendo de la pared"
            if x <= 0 + margen:
                lr = speed
                a = (90 - a) + 90
            elif x >= lado - margen:
                lr = -speed
                a = (90 - a) + 90
            if y <= 0 + margen:
                fb = speed
                a = (0 - a)
            elif y >= lado - margen:
                fb = -speed
                a = (0 - a)

    # Sumatorio de las posiciones
    x += (d * math.cos(math.radians(a)))
    y += (d * math.sin(math.radians(a)))
    x = round(x, 2) #Redondeamos a 2 decimales
    y = round(y, 2)

    return [lr, fb, x, y, a, pared]


def Movimiento2(Colision):
    global x2, y2, lr2, fb2, lado, a2, pared2
    d = dInterval
    pared2 = False

    if Colision:
        lr2 = -lr2
        fb2 = -fb2
        a2 = a2 + 180
    else:
        if (0 + margen) < x2 < (lado - margen) and (0 + margen) < y2 < (lado - margen):
            pass
        else:
            print("Pared en drone2")
            pared2 = True
            if x2 <= 0 + margen:
                lr2 = speed
                a2 = (90 - a2) + 90
            elif x2 >= lado - margen:
                lr2 = -speed
                a2 = (90 - a2) + 90
            if y2 <= 0 + margen:
                fb2 = speed
                a2 = (0 - a2)
            elif y2 >= lado - margen:
                fb2 = -speed
                a2 = (0 - a2)

    # Sumatorio de las posiciones
    x2 += (d * math.cos(math.radians(a2)))
    y2 += (d * math.sin(math.radians(a2)))
    x2 = round(x2, 2)
    y2 = round(y2, 2)

    return [lr2, fb2, x2, y2, a2, pared2]

def DistanciaDrones(points, points2):

    "Fórmula distancia entre dos puntos de un plano"
    distancia = math.sqrt((points2[-1][0] - points[-1][0])**2 + (points2[-1][1] - points[-1][1])**2)

    return distancia


while True:
    vals = Movimiento(Colision)
    vals2 = Movimiento2(Colision)

    if vals[5] or vals2[5] or Colision or Inicio:

        swarm.tellos[0].send_rc_control(vals[0], vals[1], 0, 0)
        swarm.tellos[1].send_rc_control(vals2[0], vals2[1], 0, 0)

    else:
        pass

    Inicio = False

    points.append((vals[2], vals[3]))
    points2.append((vals2[2], vals2[3]))
    Distancia = round(DistanciaDrones(points, points2), 2)

    print("Pos drone1: " + str(points[-1]) + " Pos drone2: " + str(points2[-1]) + " Distancia: " + str(Distancia) + " Colision: " + str(Colision) + " RC1: (" + str(vals[0]) + ", " + str(vals[1]) + ")" + " RC2: (" + str(vals2[0]) + ", " + str(vals2[1]) + ")")

    if Distancia <= 30:
        Colision = True
    else:
        Colision = False

    sleep(interval)
