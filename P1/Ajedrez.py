
#Basically a chess table is 8x8. 800x800px means squares 100x100 per color. I start with 
#A blank chess table and will paint it black with two nested for cycles
import cv2  
import numpy as np
import matplotlib.pyplot as plt
ancho = 800
alto = 800

gris_img = np.zeros((alto,ancho,1), dtype = np.uint8)
#Starts with a black image
a=True
for i in range(0,800,100):
    for j in range(0,800,100):
        if a:
            gris_img[i:i+100,j:j+100,0] = 255 #Makes a box white every 2
            a=False
        else:
            a=True
    a=a^1
#Shows the image
plt.imshow(gris_img, cmap='gray')
plt.show()
