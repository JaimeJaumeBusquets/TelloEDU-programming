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
swarm.move_up(30)


swarm.parallel(lambda i, tello: tello.send_rc_control(0, 25*((-1)**i), 0, 0))
time.sleep(3)
swarm.tellos[0].send_rc_control(0, 0, 0, 0)
swarm.tellos[1].send_rc_control(0, 0, 0, 0)
swarm.tellos[0].flip_back()
swarm.tellos[1].flip_forward()
time.sleep(1)
swarm.parallel(lambda i, tello: tello.send_rc_control(0, -25*((-1)**i), 0, 0))
time.sleep(3)
swarm.tellos[0].send_rc_control(0, 0, 0, 0)
swarm.tellos[1].send_rc_control(0, 0, 0, 0)
swarm.tellos[0].flip_forward()
swarm.tellos[1].flip_back()
time.sleep(1)
swarm.land()