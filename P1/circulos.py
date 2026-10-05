import cv2  
import numpy as np
import matplotlib.pyplot as plt
vid = cv2.VideoCapture(0)
  
while(True):
    # fotograma a fotograma
    ret, frame = vid.read()
    

    
    if ret:  
        # Muestra fotograma
        cv2.imshow('Vid', frame)
    
    # Detenemos pulsado ESC
    if cv2.waitKey(20) == 27:
        break
  
# Libera el objeto de captura
vid.release()
# Destruye ventanas
cv2.destroyAllWindows()
