import cv2  
import numpy as np
import matplotlib.pyplot as plt
import csv
#need to add camera support and that's it, I'm done

img = cv2.imread('Monedas.jpg') 
print(img.shape)
#Recordar que OpenCV lee las imágenes en BGR, por lo que convertimos para visualizr a RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
umbral = 200 # Prueba varios comenzando en 130
# Umbralizado binario invertido, dado que por defecto se asume objetos en blanco

img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

th1,img_th1 = cv2.threshold(img_gris,umbral,255,cv2.THRESH_BINARY_INV)
coin=(0,0)

contornos2, hierarchy2 = cv2.findContours(img_th1, 
    cv2.RETR_EXTERNAL , 
    cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_rgb, contornos2, -1, (0,255,0), 3)
plt.subplot(132)
plt.axis("off")
plt.imshow(img_rgb) 
plt.show()



#setting values to start, so it works with different light types

def getPoint(action, x, y, flags, *userdata):
  # Referencing global variables
    global coin
  # Mark the top left corner when left mouse button is pressed
    # When left mouse button is released, mark bottom right corner
    if action == cv2.EVENT_LBUTTONUP:
        coin = (x,y)   

temp = img.copy()


    #Área mínima (útil filtrar en ocasiones)
    
    #Perímetro del contorno
cv2.namedWindow("Window")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", getPoint)
k=0
# Close the window when key q is pressed
while k!=113:
  # Display the image
  cv2.imshow("Window", img)
  k = cv2.waitKey(0)
  # If c is pressed, clear the window, using the dummy image
  if (k == 99):
    img= temp.copy()
    cv2.imshow("Window", img)
OneEuro=coin
k=0
while k!=113:
  # Display the image
  cv2.imshow("Window", img)
  k = cv2.waitKey(0)
  # If c is pressed, clear the window, using the dummy image
  if (k == 99):
    img= temp.copy()
    cv2.imshow("Window", img)
Cent=coin
both=0
valuescentrel=[1,(276/207),354/207,306/207,388/207,461/207,424/207,520/207]
valueeurorel=[207/424,(276/424),354/424,306/424,388/424,461/424,1,520/424]

def region_rgb(img,contour, r_min, r_max): #thx chatgpt
    """Median RGB color of the ring between r_min*R and r_max*R (R = coin radius)."""
    (cx, cy), r = cv2.minEnclosingCircle(contour)
    h, w = img.shape[:2]
    yy, xx = np.ogrid[:h, :w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    mask = (dist >= r_min * r) & (dist <= r_max * r)
    bgr = np.median(img[mask], axis=0).astype(float)
    return bgr
def euro_colors(img, euro_contour):
    center = region_rgb(img, euro_contour, 0.0, 0.5)
    ring   = region_rgb(img, euro_contour, 0.80, 0.93)
    return center, ring
def cent_colors(img,contour):
    return  region_rgb(img, contour, 0.0, 0.95)

for c in contornos2:
    area=cv2.contourArea(c)
    #Área del contorno
    if(area>20):
        if cv2.pointPolygonTest(c, OneEuro, False) >= 0:
            areamax = area
            grey,gold=euro_colors(img_rgb,c)
            both+=1
        if cv2.pointPolygonTest(c, Cent, False) >= 0:
            areamin = area
            bronze=cent_colors(img_rgb,c)
            both+=1
        if(both==2):
            break
for i in range(len(valuescentrel)):
    valuescentrel[i]=valuescentrel[i]*areamin
    valueeurorel[i]=valueeurorel[i]*areamax
moneyvalue=0
moneychart=[0.01,0.02,0.05,0.1,0.2,0.5,1,2]



bronzens=[0,1,2]
goldens=[3,4,5]
eurons=[6,7]
cointype=[eurons,goldens,bronzens]
print(gold,bronze,          abs(bronze[0]-gold[0])+abs(bronze[1]-gold[1])+abs(bronze[2]-gold[2])
)
for c in contornos2:

    area = cv2.contourArea(c)




    if(area>20):

        inside,outside=euro_colors(img_rgb,c)
        nocircle=abs(inside[0]-outside[0])+abs(inside[1]-outside[1])+abs(inside[2]-outside[2])
        type=0
        if(nocircle<50):
            difbronze=abs(inside[0]-bronze[0])+abs(inside[1]-bronze[1])+abs(inside[2]-bronze[2])

            difgold=abs(inside[0]-gold[0])+abs(inside[1]-gold[1])+abs(inside[2]-gold[2])

            if(difbronze>50 ):
                type=1 #golden
            else:
                type=2 #bronze
            

    #here we checked for size, I think we should use just size after colour check
        minsum=area*2
        index=-1
        for i in cointype[type]:
            area1val=area-valuescentrel[i]
            area2val=area-valuescentrel[i]
            sum=abs(area1val)+abs(area2val)
            if(sum<minsum):
                minsum=sum
                index=i
        print(area,moneychart[index],inside)
        moneyvalue+=moneychart[index]
print(moneyvalue,areamin,areamax)
    






