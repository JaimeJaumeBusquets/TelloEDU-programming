"Para la creación de la app"
from kivy.app import App
from kivy.lang import Builder
"Desarrollo de diferentes ventanas"
from kivy.uix.screenmanager import Screen, ScreenManager
"Función PopUp"
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
"Para el Tello EDU"
from tellopy import tello, swarm
from time import sleep
"VideoStream"
import cv2
from kivy.clock import Clock
import time
from kivy.graphics.texture import Texture
"Facetracking"
import numpy as np
"Rebote"
import ColisionModule as cm

me = tello.Tello()
speed = 30

comandas = open("Comandas.txt", 'w') #Vaciamos comandas anteriores
IPs = open("Ips.txt", 'w')

"Interacciones entre ventanas"
class WindowManager(ScreenManager):
    pass

"Configuración Plan de Vuelo"
class PlanVuelo(Screen):

    def info(self):
        content = BoxLayout(orientation="vertical")
        pop = Popup(title="INFORMACIÓN", content=content, size_hint=(1, 0.5), auto_dismiss=False)
        texto = Label(text="""  Para crear el plan de vuelo indique por orden cronológico las comandas que desea enviar al drone.
    Piense que la primera comanda debe ser despegar y la última aterrizar.
    El rango de distancias disponible es de 20-500 cm y el rango de rotaciones es de 1-360º.""",
                      text_size=(self.width, None))
        boton = Button(text="OK", size_hint=(0.3, 0.3),
                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=pop.dismiss)
        content.add_widget(texto)  # Se añade el Label al BoxLayout
        content.add_widget(boton)  # Se añade el botón al BoxLayout
        pop.open()

    def Comandas(self):

        comandas = open("Comandas.txt", 'a') #para añadir (a)

        if self.ids.plandelante.state == "down":
            if 20 <= int(self.ids.plandelantetexto.text) <= 500:
                comanda = "forward " + self.ids.plandelantetexto.text
                self.ids.plandelantetexto.text = "" #TextInput vacio al haber pulsado
                comandas.write(comanda + "\n")
            else:
                self.ids.plandelantetexto.text = "Error"

        if self.ids.plandetras.state == "down":
            if 20 <= int(self.ids.plandetrastexto.text) <= 500:
                comanda = "back " + self.ids.plandetrastexto.text
                self.ids.plandetrastexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.plandetrastexto.text = "Error"

        if self.ids.planderecha.state == "down":
            if 20 <= int(self.ids.planderechatexto.text) <= 500:
                comanda = "right " + self.ids.planderechatexto.text
                self.ids.planderechatexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planderechatexto.text = "Error"

        if self.ids.planizquierda.state == "down":
            if 20 <= int(self.ids.planizquierdatexto.text) <= 500:
                comanda = "left " + self.ids.planizquierdatexto.text
                self.ids.planizquierdatexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planizquierdatexto.text = "Error"

        if self.ids.planarriba.state == "down":
            if 20 <= int(self.ids.planarribatexto.text) <= 500:
                comanda = "up " + self.ids.planarribatexto.text
                self.ids.planarribatexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planarribatexto.text = "Error"

        if self.ids.planabajo.state == "down":
            if 20 <= int(self.ids.planabajotexto.text) <= 500:
                comanda = "down " + self.ids.planabajotexto.text
                self.ids.planabajotexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planabajotexto.text = "Error"

        if self.ids.planhorario.state == "down":
            if 1 <= int(self.ids.planhorariotexto.text) <= 360:
                comanda = "cw " + self.ids.planhorariotexto.text
                self.ids.planhorariotexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planhorariotexto.text = "Error"

        if self.ids.planantihorario.state == "down":
            if 1 <= int(self.ids.planantihorariotexto.text) <= 360:
                comanda = "ccw " + self.ids.planantihorariotexto.text
                self.ids.planantihorariotexto.text = ""
                comandas.write(comanda + "\n")
            else:
                self.ids.planantihorariotexto.text = "Error"

        if self.ids.plandespegue.state == "down":
            comanda = "takeoff"
            comandas.write(comanda + "\n")

        if self.ids.planaterrizaje.state == "down":
            comanda = "land"
            comandas.write(comanda + "\n")

        if self.ids.planelimina.state == "down":
            comandas = open("Comandas.txt", 'r') #Cambiamos a modo lectura
            lineas = comandas.readlines() #Lista con todas las lineas
            comandas = open("Comandas.txt", 'w') #Cambiamos a modo escritura
            linea = lineas[-1] #Seleccionamos última linea
            lineas.remove(linea) #La eliminamos
            for linea in lineas:
                comandas.write(linea) #Reescribimos todas las otras lineas

        if self.ids.planvuela.state == "down":
            comandas = open("Comandas.txt", 'r')
            lineas = comandas.readlines()
            i = 0

            while i < len(lineas):

                if me.get_speed_x() <= 0 and me.get_speed_y() <= 0 and me.get_speed_z() <= 0:
                    comanda = lineas[i].rstrip()
                    me.send_command_with_return(comanda)
                    i = i + 1
                    #sleep(2) #Para cuando se pare no envie 2 comandas a la vez

                else:
                    pass

        comandas = open("Comandas.txt", 'r')  # Cambiamos a modo lectura
        lineas = comandas.readlines()  # Lista con todas las lineas

        self.ids.labelcomandas.text = "Comandas: " + str(lineas)

"Conexión"
class ConexionWindow(Screen):

    def pressedConexion(self):

        me.connect()
        #me.streamon()

        content = BoxLayout(orientation="vertical")
        pop = Popup(title="CONEXIÓN REALIZADA CON ÉXITO", content=content, size_hint=(0.7, 0.3),  auto_dismiss=False)
        texto = Label(text="Nivel de batería al: " + str(me.get_battery()) + "%")
        boton = Button(text="OK", size_hint=(0.3, 0.3),
                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=pop.dismiss)
        content.add_widget(texto) #Se añade el Label al BoxLayout
        content.add_widget(boton) #Se añade el botón al BoxLayout
        pop.open()

    def pressedConexionSwarm(self):

        content = BoxLayout(orientation="vertical")
        pop = Popup(title="CONEXIÓN MODO AP", content=content, size_hint=(1, 0.5), auto_dismiss=False)
        texto = Label(text="""  Realice el siguiente proceso con cada Tello EDU:
        1º- Conectarse indivualmente al drone/n"
        2º- Indicar parámetros de la red Wi-Fi/n"
        3º- Cambiar su modo a Access Point/n"
    Para terminar, indique una a una las direcciones IP asociadas a cada aeronave. """,
                      text_size=(self.width, None))
        boton = Button(text="OK", size_hint=(0.3, 0.3),
                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=pop.dismiss)
        content.add_widget(texto)  # Se añade el Label al BoxLayout
        content.add_widget(boton)  # Se añade el botón al BoxLayout
        pop.open()

"Conexion drones en modo AP al router"
class SwarmConexion(Screen):
    def APConexion(self):
        me.connect()
        ssid = self.ids.idwifi.text
        password = self.ids.passwifi.text
        print(ssid, password)
        me.connect_to_wifi(ssid, password)

        content = BoxLayout(orientation="vertical")
        pop = Popup(title="Modo AP", content=content, size_hint=(1, 0.3), auto_dismiss=False)
        texto = Label(text="Modo Access Point establecido, conéctese al siguiente drone y realice el mismo proceso")
        boton = Button(text="OK", size_hint=(0.3, 0.3),
                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=pop.dismiss)
        content.add_widget(texto)  # Se añade el Label al BoxLayout
        content.add_widget(boton)  # Se añade el botón al BoxLayout
        pop.open()

    def SetIps(self):
        Ips = open("Ips.txt", 'a')
        Ip = self.ids.ip.text
        self.ids.ip.text = ""  # TextInput vacio al haber pulsado
        Ips.write(Ip + "\n")

"Control del Enjambre"
class SwarmControl(Screen):

    def pressedConexion(self):
        Ips = open("Ips.txt", 'r')
        Ipsstr = [linea.rstrip() for linea in Ips]
        print(Ipsstr)

        self.Enjambre = swarm.TelloSwarm.fromIps(Ipsstr)
        self.Enjambre.connect()

        for tello in self.Enjambre:
            print(tello.get_battery())

    def Despegue(self):
        self.Enjambre.takeoff()
        #self.Enjambre.move_up(25)

    def Aterrizaje(self):
        self.Enjambre.land()

    def Cuadrado(self):

        "Primer drone de la lista de Ips colocado a la derecha"
        self.Enjambre.tellos[0].send_rc_control(0, 0, -25, 0)  # Drone der baja
        time.sleep(2)
        self.Enjambre.tellos[1].send_rc_control(0, 0, 25, 0)  # Drone izq sube
        time.sleep(2)

        self.Enjambre.parallel(lambda i, tello: tello.send_rc_control(25 * (-1) ** i, 0, 0, 0))  # movs laterales
        time.sleep(4)

        self.Enjambre.tellos[0].send_rc_control(0, 0, 25, 0)  # Drone der sube
        self.Enjambre.tellos[1].send_rc_control(0, 0, 0, 0)  # Drone izq para
        time.sleep(4)

        self.Enjambre.tellos[0].send_rc_control(0, 0, 0, 0)  # Drone der para
        self.Enjambre.tellos[1].send_rc_control(0, 0, -25, 0)  # Drone izq baja
        time.sleep(4)

        self.Enjambre.parallel(lambda i, tello: tello.send_rc_control(-25 * (-1) ** i, 0, 0, 0))  # movs laterales
        time.sleep(4)

        self.Enjambre.tellos[0].send_rc_control(0, 0, -25, 0)  # Drone der baja
        self.Enjambre.tellos[1].send_rc_control(0, 0, 0, 0)  # Drone izq para
        time.sleep(2)

        self.Enjambre.tellos[1].send_rc_control(0, 0, 25, 0)  # Drone izq sube
        self.Enjambre.tellos[0].send_rc_control(0, 0, 0, 0)  # Drone der para
        time.sleep(2)
        self.Enjambre.tellos[1].send_rc_control(0, 0, 0, 0)

    def Circulo(self):

        self.Enjambre.parallel(lambda i, tello: tello.curve_xyz_speed(100 * ((-1) ** i), -50 * ((-1) ** i), 0, 0, -100 * ((-1) ** i), 0, 25))
        time.sleep(0.5)
        self.Enjambre.parallel(lambda i, tello: tello.curve_xyz_speed(-100 * ((-1) ** i), 50 * ((-1) ** i), 0, 0, 100 * ((-1) ** i), 0, 25))

    def Flips(self):

        self.Enjambre.parallel(lambda i, tello: tello.send_rc_control(0, 25 * ((-1) ** i), 0, 0))
        time.sleep(3)
        self.Enjambre.tellos[0].send_rc_control(0, 0, 0, 0)
        self.Enjambre.tellos[1].send_rc_control(0, 0, 0, 0)
        self.Enjambre.tellos[0].flip_back()
        self.Enjambre.tellos[1].flip_forward()
        time.sleep(1)
        self.Enjambre.parallel(lambda i, tello: tello.send_rc_control(0, -25 * ((-1) ** i), 0, 0))
        time.sleep(3)
        self.Enjambre.tellos[0].send_rc_control(0, 0, 0, 0)
        self.Enjambre.tellos[1].send_rc_control(0, 0, 0, 0)
        self.Enjambre.tellos[0].flip_forward()
        self.Enjambre.tellos[1].flip_back()
        time.sleep(1)

    def BucleRebote(self):

        if self.ids.rebote.state == 'down':
            self.Colision = False
            fSpeed = 117 / 10  # Velocidad lineal real
            interval = 0.25  # Intervalo de tiempo
            self.dInterval = fSpeed * interval
            self.speed = 15
            self.posx, self.posy = 0.5, 0.5
            self.posx2, self.posy2 = 149.5, 0.5
            self.a, self.a2 = 45, 135
            self.lr, self.lr2 = self.speed, -self.speed
            self.fb, self.fb2 = self.speed, self.speed
            self.DistanciaSeguridad = 15
            self.points = [(self.posx, self.posy)]
            self.points2 = [(self.posx2, self.posy2)]
            self.Inicio = True

            #Poner clock
            self.event = Clock.schedule_interval(self.Rebote, interval)
        else:
            self.Enjambre.send_rc_control(0, 0, 0, 0)
            self.event.cancel()

    def Rebote(self, dt):

        vals = cm.Movimiento(self.Colision, self.dInterval, self.speed, self.posx, self.posy, self.a, self.lr, self.fb)
        vals2 = cm.Movimiento2(self.Colision, self.dInterval, self.speed, self.posx2, self.posy2, self.a2, self.lr2, self.fb2)
        #print("VALS ---> " + "lr: " + str(vals[0]) + " fb: " + str(vals[1]) + " x: " + str(vals[2]) + " y: " + str(vals[3]) + " a: " + str(vals[4]))
        #print("VALS2 ---> " + "lr: " + str(vals2[0]) + " fb: " + str(vals2[1]) + " x: " + str(vals2[2]) + " y: " + str(vals2[3]) + " a: " + str(vals2[4]))
        if vals[5] or vals2[5] or self.Colision or self.Inicio:
            self.Enjambre.tellos[0].send_rc_control(vals[0], vals[1], 0, 0)
            self.Enjambre.tellos[1].send_rc_control(vals2[0], vals2[1], 0, 0)
        else:
            pass
        self.Inicio = False
        self.posx, self.posy, self.a, self.lr, self.fb = vals[2], vals[3], vals[4], vals[0], vals[1]
        self.posx2, self.posy2, self.a2, self.lr2, self.fb2 = vals2[2], vals2[3], vals2[4], vals2[0], vals2[1]

        self.points.append((vals[2], vals[3]))
        self.points2.append((vals2[2], vals2[3]))
        Distancia = round(cm.DistanciaDrones(self.points, self.points2), 2)
        #print("Distancia: " + str(Distancia))

        if Distancia <= self.DistanciaSeguridad:
            self.Colision = True
        else:
            self.Colision = False


"Control del Tello EDU Individual"
class ControlWindow(Screen):

    global Listperror
    global ListperrorFB
    Listperror = [0]
    ListperrorFB = [0]

    def clock(self): #Función para actualizar el frame del video
        print("Entro al clock")
        Clock.schedule_interval(self.video, 1/30)

    def video(self, dt):
        """
        #NO FUNCIONA IMAGEN EN ANDROID, DESCOMENTAR SI SE DESEA USAR EN ENTORNO WEB

        img = me.get_frame_read().frame
        #buffer = cv2.flip(img, 0).tobytes()
        #tex = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        #tex.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        "Face Tracking Mode"
        if self.ids.face.state == "down" and self.ids.despegue.state == "down":
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # Detecta objetos y los retorna como una lista de rectángulos.
            myFaceListC = []  # Creación lista de centros de caras
            myFaceListArea = []  # Creación lista de áreas
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rectángulo rojo que marque la cara
                cx = x + w // 2
                cy = y + h // 2
                area = w * h
                myFaceListC.append([cx, cy])
                myFaceListArea.append(area)
            if len(myFaceListArea) != 0:
                i = myFaceListArea.index(max(myFaceListArea))  # Únicamente queremos la cara más cercana
                caracercana = [myFaceListC[i], myFaceListArea[i]]
            else:
                caracercana = [[0, 0], 0]

            area = caracercana[1]
            x, y = caracercana[0]
            w = 800
            fbRange = [20000, 28000]  # Rango de áreas donde el drone no avanzará o retrocederá
            pid = [0.20, 0.20, 0]  # 0.4 P, 0.4 D, 0 I
            pid2 = [0.002, 0.002, 0]  # 0.008 P, 0.008 D, 0 I

            error = x - w//2
            speed = pid[0] * error + pid[1]*(error - Listperror[-1])
            speed = int(np.clip(speed, -50, 50))

            if area < fbRange[0]:
                errorFB = fbRange[0] - area
            elif area > fbRange[1]:
                errorFB = fbRange[1] - area
            else:
                errorFB = 0

            speedFB = pid2[0] * errorFB + pid2[1] * (errorFB - ListperrorFB[-1])
            speedFB = int(np.clip(speedFB, -50, 50))

            if x == 0:
                speed = 0
                error = 0
                errorFB = 0
                speedFB = 0

            me.send_rc_control(0, speedFB, 0, speed)
            Listperror.append(error)
            ListperrorFB.append(errorFB)
            print(x, w, area, Listperror[-1], ListperrorFB[-1])


        "Método archivo jpg"
        cv2.imwrite("imagen.jpg", img)
        self.ids.video.source = "imagen.jpg"
        self.ids.video.reload()
        #self.ids.video.texture = tex
        """

        self.ids.video.source = "ImagenOut.jpg"

    def DespegaAterriza(self):
        if self.ids.despegue.state == "down":
            me.takeoff()
            sleep(2)
        else:
            me.land()
            sleep(2)

    def Desconexion(self):
        me.land()
        me.streamoff()
        sleep(2)
        quit()

    def Movimiento(self):
        lr, fb, ud, yv = 0, 0, 0, 0

        if self.ids.arriba.state == "down":
            ud = speed
        elif self.ids.abajo.state == "down":
            ud = -speed
        if self.ids.yawiz.state == "down":
            yv = -speed
        elif self.ids.yawder.state == "down":
            yv = speed
        if self.ids.delante.state == "down":
            fb = speed
        elif self.ids.atras.state == "down":
            fb = -speed
        if self.ids.izquierda.state == "down":
            lr = -speed
        elif self.ids.derecha.state == "down":
            lr = speed

        me.send_rc_control(lr, fb, ud, yv)

"Archivo de lenguaje Kivy"
kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        self.Title = "Control Básico Tello EDU"
        return kv

if __name__ == '__main__':
    MyApp().run()


