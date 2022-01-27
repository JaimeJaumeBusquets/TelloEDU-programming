from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())

"Cámara frontal (0) o inferior (1)"
me.set_video_direction(0)
me.streamon()

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (320, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
