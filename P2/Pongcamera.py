import cv2  
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
vid = cv2.VideoCapture(0)

#Marca de inicio
disponible = 0 
while(True):      
    # fotograma a fotograma
    ret, frame = vid.read()
    print(frame.shape)
    if ret:
        if disponible > 0:
            dif = cv2.absdiff(frame, pframe)     
            # Muestra resultado
            dif = cv2.cvtColor(dif, cv2.COLOR_BGR2GRAY)

            M=cv2.moments(dif)
            if M['m00'] != 0:  # Prevent division by zero if no white pixels are found
                cX = int(M['m10'] / M['m00'])
        
                cv2.imshow('Diferencia', dif)   
        else:
            disponible = 1

        #Copia fotograma actual para la diferencia en el siguiente forograma
        pframe = frame.copy()
    # Detenemos pulsado ESC
    if cv2.waitKey(20) == 27:
        break
  
# Libera el objeto de captura
vid.release()
# Destruye ventanas
cv2.destroyAllWindows()