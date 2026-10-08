import cv2  
import numpy as np
import matplotlib.pyplot as plt
vid = cv2.VideoCapture(0)
  
while(True):
    # fotograma a fotograma
    ret, frame = vid.read()
    height,wide,rgb=frame.shape
    darkest=frame.max()
    clearest=frame.min()
    xd,yd=0,0
    xc,yc=0,0
    #lowest mean and highest mean rgb shuld be the darkest and clearest
    #I loop through every pixel of the matrix to find it
    for i in range(480):
        for j in range(640):
            mean=(frame[i,j,0]+frame[i,j,2]+frame[i,j,1])/3
            if(mean>clearest):
                clearest=mean
                xc=i
                yc=j
            if(mean<darkest):
                darkest=mean
                xd=i
                xd=j
    cv2.circle(frame,(xc,yc), 15, (0,0,0), -1)
    cv2.circle(frame,(xd,yd), 15, (255,255,255), -1)

    
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
