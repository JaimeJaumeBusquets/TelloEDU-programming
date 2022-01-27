from djitellopy import tello
from djitellopy import TelloSwarm

me = tello.Tello()
me.connect()
print(me.get_battery())

ssid = "    "
password = "    "

#me.set_wifi_credentials(ssid, password)
me.connect_to_wifi(ssid, password)

