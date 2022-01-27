# TelloEDU-programming

Este repositorio contiene el código desarrollado durante mi Trabajo de Final de Grado. La memoria de dicho proyecto está disponible en el repositorio como MemoriaTFGJaimeJaumeBusquets y allí se explican detalladamente los pasos seguidos en torno a cada código, instrucciones para instalar el entorno, librerías y versiones necesarias, consejos aportados a raíz de la experiencia obtenida y mis propias conclusiones finales.

Como se puede observar, también se encuentran 3 carpetas disponibles que hacen referencia a cada uno de los capítulos trabajados durante el proyecto:

# TFG
En TFG se encuentran todos los código y archivos referentes al entorno web. Movimientos básicos, transmisión de video, control desde teclado y toma de imágenes, mapeo del movimiento, reconocimiento facial y seguimiento, y por último, control del drone mediante las manos.
# TFG2
En TFG2 todo lo relacionado con el modo Swarm. Como ejecutar el cambio a modo swarm, control del swarm desde teclado y desarrollo de diferentes interacciones entre dos drones (cuadrado, circulo, flips y modo rebote, el cual no funciona correctamente debido a la poca precisión en los movimientos del Tello EDU)
# TFG3
Para terminar, en TFG3 se encuentran los archivos necesarios para generar la aplicación móvil, así como el archivo .apk para poder instalarla directamente. Cabe destacar que la aplicación móvil ha sido generada mediante Kivy y Buildozer, es decir, es una aplicación multiplataforma y en un PC también puede ser usada.

A causa de la incompatibilidad entre OpenCv y Android, las imágenes retransmitidas por el Tello EDU no están disponibles en la versión final de la app. Aún así, el código necesario para implementar dichas imágenes junto con la opción de aplicar el seguimiento facial, están disponibles en el código (comentadas) por si se desea trabajar en PC, donde si funciona correctamente. 

Para cualquier duda, consulte la memoria donde está todo documentado.
