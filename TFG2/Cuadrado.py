from djitellopy import TelloSwarm
import time

"Indicar IPS"
swarm = TelloSwarm.fromIps([
    "XXX.XXX.X.XXX",
    "XXX.XXX.X.XXX",
])
swarm.connect()

for tello in swarm:
    print(tello.get_battery())

swarm.takeoff()
swarm.move_up(30)

"Primer drone de la lista de Ips colocado a la derecha"
swarm.tellos[0].send_rc_control(0, 0, -25, 0) #Drone der baja
time.sleep(2)
swarm.tellos[1].send_rc_control(0, 0, 25, 0) #Drone izq sube
time.sleep(2)

swarm.parallel(lambda i, tello: tello.send_rc_control(25*(-1)**i, 0, 0, 0)) #movs laterales
time.sleep(4)

swarm.tellos[0].send_rc_control(0, 0, 25, 0) #Drone der sube
swarm.tellos[1].send_rc_control(0, 0, 0, 0) #Drone izq para
time.sleep(4)

swarm.tellos[0].send_rc_control(0, 0, 0, 0) #Drone der para
swarm.tellos[1].send_rc_control(0, 0, -25, 0) #Drone izq baja
time.sleep(4)

swarm.parallel(lambda i, tello: tello.send_rc_control(-25*(-1)**i, 0, 0, 0)) #movs laterales
time.sleep(4)

swarm.tellos[0].send_rc_control(0, 0, -25, 0) #Drone der baja
swarm.tellos[1].send_rc_control(0, 0, 0, 0) #Drone izq para
time.sleep(2)

swarm.tellos[1].send_rc_control(0, 0, 25, 0) #Drone izq sube
swarm.tellos[0].send_rc_control(0, 0, 0, 0) #Drone der para
time.sleep(2)

swarm.land()




