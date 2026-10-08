
import cv2  
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

img = cv2.imread('mandril.jpg') 
#Conversión de la imagen a niveles de grises de la imagen original en BGR
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height,length=gris.shape
plt.figure()
#Eliminamos etiquetas de los ejes
plt.axis("off")
canny = cv2.Canny(gris, 100, 200)
col_counts = cv2.reduce(canny, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)

plt.axis("off")
plt.title("Canny with whites density")


maxfil=0
arr=col_counts
#Gets the most white row
for i in range(0,len(arr)):
    if arr[i][0]>=maxfil:
        maxfil=arr[i][0]
highwhite=[]
count=0
#get the rows that are at least 0.9*the most white
for i in range(len(arr)):
    if arr[i][0]>=0.9*maxfil:
        count+=1
        highwhite.append(1)
    else:
        highwhite.append(0)
maxfil=maxfil/ (255) #max white px in a row
print("max number of white pixels on row:",maxfil)
print("rows with very much white(>0.9*maxfil):",count)
canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
for i in range(len(highwhite)):
    if highwhite[i]:
        
        #print("row:",i)
        cv2.line(canny,(0,i),(length,i),(255,255,0),1)



plt.imshow(canny, cmap='gray') 
plt.show()

