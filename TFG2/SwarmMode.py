from djitellopy import tello
from djitellopy import TelloSwarm

me = tello.Tello()
me.connect()
print(me.get_battery())

ssid = "MIWIFI_dd6r"
password = "RJEY6pCJ"

#me.set_wifi_credentials(ssid, password)
me.connect_to_wifi(ssid, password)

