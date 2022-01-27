from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()
""" Go forward/backward"""
me.send_rc_control(0, 50, 0, 0)
sleep(2)
" Go right/left"
me.send_rc_control(30, 0, 0, 0)
sleep(2)
" Rotate clockwise/anticlockwise (yaw)"
me.send_rc_control(0, 0, 0, 30)
sleep(2)
" Go up/down"
me.send_rc_control(0, 0, 30, 0)
sleep(2)

me.send_rc_control(0, 0, 0, 0) #stop

me.land()

