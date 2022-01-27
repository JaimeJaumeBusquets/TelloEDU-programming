from djitellopy import TelloSwarm
import time

"Indicar IPS"
swarm = TelloSwarm.fromIps([
    "192.168.1.139",
    "192.168.1.138",
])
swarm.connect()

for tello in swarm:
    print(tello.get_battery())

swarm.takeoff()
swarm.parallel(lambda i, tello: tello.move_up(30))


swarm.parallel(lambda i, tello:
               tello.curve_xyz_speed(100*((-1)**i), -50*((-1)**i), 0, 0, -100*((-1)**i), 0, 25))
time.sleep(0.2)
swarm.parallel(lambda i, tello:
               tello.curve_xyz_speed(-100 * ((-1) ** i), 50 * ((-1) ** i), 0, 0, 100 * ((-1) ** i), 0, 25))