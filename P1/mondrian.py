import cv2  
import numpy as np
import matplotlib.pyplot as plt
ancho = 800
alto = 800

#Crea una imagen con tres planos
color_img = np.zeros((alto,ancho,3), dtype = np.uint8)
color_img[0:800,0:800]=(255,255,255)

#Línea roja vertical de grosor 3
"""What I need to do is lines and filled rectangles, that's it
But to make it actually cool I need to do random rectangles
I start white, put random rectangles... Would need to keep a list of all
the rectangles, the lines ecc, it takes to long
I just have to make one actually, so I can do it manually I guess
"""
#Rectángulo relleno
cv2.rectangle(color_img,(0,0),(100,500),(255,255,0),-1)#yellow
cv2.rectangle(color_img,(300,300),(400,500),(255,0,0),-1)#red
cv2.rectangle(color_img,(500,300),(700,600),(0,255,0),-1)#green
cv2.rectangle(color_img,(200,100),(750,300),(0,0,255),-1)#blue
cv2.line(color_img,(100,300),(ancho,300),(0,0,0),10)
cv2.line(color_img,(300,300),(300,alto),(0,0,0),10)
cv2.line(color_img,(500,300),(500,alto),(0,0,0),10)
cv2.line(color_img,(300,600),(ancho,600),(0,0,0),10)
cv2.line(color_img,(100,0),(100,500),(0,0,0),10)
cv2.line(color_img,(0,500),(500,500),(0,0,0),10)

cv2.line(color_img,(400,300),(400,alto),(0,0,0),10)
cv2.line(color_img,(700,300),(700,alto),(0,0,0),10)
cv2.line(color_img,(750,300),(750,0),(0,0,0),10)
cv2.line(color_img,(100,100),(ancho,100),(0,0,0),10)
cv2.line(color_img,(200,100),(200,500),(0,0,0),10)
cv2.line(color_img,(400,100),(400,300),(0,0,0),10)





#Visualiza sin especificar el mapa de color gris
plt.imshow(color_img) 
plt.show()

#Salva la imagen resultante a disco
#cv2.imwrite('imagen.jpg', color_img)


