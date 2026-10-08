
import cv2  
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
#Gets the whitest column and row white and print info about it
def highwhite(imagenUmbralizada):
    #rows img
    col_counts = cv2.reduce(imagenUmbralizada, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)


    #finding the whitest row and the rows closest to it by 0.9*maxfil white pixels
    maxfil=0
    arr=col_counts
    for i in range(0,len(arr)):
        if arr[i][0]>=maxfil:
            maxfil=arr[i][0]
    highwhite=[]
    count=0
    for i in range(len(arr)):
        if arr[i][0]>=0.9*maxfil:
            count+=1
            highwhite.append(1)
        else:
            highwhite.append(0)
    maxfil=maxfil/ (255) #max white px in a row
    print("max number of white pixels on row:",maxfil)
    print("rows with very much white(>=0.9*maxfil):",count)

    #cols thing
    col_counts = cv2.reduce(imagenUmbralizada, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)

    #finding the whitest column and the columns closest to it by 0.9*maxfil white pixels

    maxfil=0
    arr=col_counts[0]
    for i in range(0,len(arr)):
        if arr[i]>=maxfil:
            maxfil=arr[i]
    highwhit2=[]
    count=0
    for i in range(len(arr)):
        if arr[i]>=0.9*maxfil:
            count+=1
            highwhit2.append(1)
        else:
            highwhit2.append(0)
    maxfil=maxfil/ (255) #max white px in a row
    print("max number of white pixels on column:",maxfil)
    print("columns with very much white(>=0.9*maxfil):",count)

    imagenUmbralizada = cv2.cvtColor(imagenUmbralizada, cv2.COLOR_GRAY2BGR)

    for i in range(len(highwhit2)):
        if highwhit2[i]:
            #print("cols:",i)
            cv2.line(imagenUmbralizada,(i,0),(i,height),(255,255,0),1)
    for i in range(len(highwhite)):
        if highwhite[i]:
            #print("row:",i)
            cv2.line(imagenUmbralizada,(0,i),(length,i),(255,255,0),1)
    return imagenUmbralizada
img = cv2.imread('mandril.jpg') 
#Conversión de la imagen a niveles de grises de la imagen original en BGR
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gris.shape)
height,length=gris.shape

ggris = cv2.GaussianBlur(gris, (3, 3), 0)

#Calcula en ambas direcciones (horizontal y vertical)
sobelx = cv2.Sobel(ggris, cv2.CV_64F, 1, 0)  # x
sobely = cv2.Sobel(ggris, cv2.CV_64F, 0, 1)  # y
#Combina ambos resultados
sobel = cv2.add(sobelx, sobely)

sobel8 = cv2.convertScaleAbs(sobel)

#Umbralization
valorUmbral = 100 
_, imagenUmbralizada = cv2.threshold(sobel8, valorUmbral, 255, cv2.THRESH_BINARY)
#Lines on lightest rows and columns
imagenUmbralizadaSobel=highwhite(imagenUmbralizada)
imagenUmbralizadaCanny=highwhite(cv2.Canny(gris, 100, 255))

#Shows the modified images in detail
plt.imshow(imagenUmbralizadaSobel, cmap='gray') 
plt.show()
plt.imshow(imagenUmbralizadaCanny, cmap='gray') 
plt.show()

#Show the two images to compare
plt.figure()
plt.subplot(1, 2, 1)
plt.axis("off")
plt.title('Sobel Umbralized image')
plt.imshow(imagenUmbralizadaSobel, cmap='gray') 

plt.subplot(1, 2, 2)
plt.axis("off")
plt.title('Canny Umbralized image')
plt.imshow(imagenUmbralizadaCanny, cmap='gray') 
plt.show()
