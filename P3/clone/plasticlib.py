
import cv2  
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
def getMediumColor(imgrgb,contourns):
    mean_color=0
    count=0
    for c in contourns:
        area=cv2.contourArea(c)
        if(area>10):
            mask = np.zeros(imgrgb.shape[:2], dtype=np.uint8)

        # Fill the particle's contour in white
            cv2.drawContours(mask, [c], -1, 255, thickness=cv2.FILLED)

            # Calculate mean color using only pixels inside the mask
            mean_color+= np.array(cv2.mean(imgrgb, mask=mask)[:3])
            """plt.figure(figsize=(10, 4))
            
            plt.subplot(1, 2, 1)
            plt.imshow(imgrgb)
            plt.title(f"Contour x on original image")
            plt.axis("off")

            plt.subplot(1, 2, 2)
            plt.imshow(mask, cmap="gray")
            plt.title(f"Filled contour qx")
            plt.axis("off")

            plt.show()"""
            print(mean_color)
            count+=1
    return mean_color/count
def getMediumRough(imgth,contourns):
    mean=0
    count=0
    result = imgth.copy()

    for c in contourns:
        area=cv2.contourArea(c)
        perimeter=cv2.arcLength(c, True)
        if(area>65):
            circularity=(4*math.pi*area)/(perimeter*perimeter)
            mean+=circularity
            count+=1

            # Draw the rectangle
    mean=mean/count
    return mean
def getRough(c):
    area=cv2.contourArea(c)
    perimeter=cv2.arcLength(c, True)
    circularity=(4*math.pi*area)/(perimeter*perimeter)
    return circularity

def getMediumBrightness(image, contours):
    # Create a mask for the particle
    mean=0
    count=0
    for c in contours:
        area=cv2.contourArea(c)
        if(area>10):
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

            cv2.drawContours(
                mask, [c], -1, 255, thickness=cv2.FILLED
            )

            # Convert BGR image to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Extract the brightness (Value) channel
            value = hsv[:, :, 2]

            # Average brightness inside the particle
            mean += cv2.mean(value, mask=mask)[0]
            count+=1


    return mean/count

def getBrightness(image, c):
    # Create a mask for the particle
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(
        mask, [c], -1, 255, thickness=cv2.FILLED
    )

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract the brightness (Value) channel
    value = hsv[:, :, 2]

    # Average brightness inside the particle
    return cv2.mean(value, mask=mask)[0]


def IsRound(roughness,contours):
    round=0
    notRound=0
    rounds=[]
    for c in contours:
        if (getRough(c)>roughness):
            rounds.append(1)
            round+=1
        else:
            rounds.append(0)
            notRound+=1
    return round,notRound,rounds
def IsBright(brightness,image,contours):
    bright=0
    notbright=0
    brights=[]
    for c in contours:
        if (getBrightness(image,c)>brightness):
            bright+=1
            brights.append(1)
        else:
            notbright+=1
            brights.append(0)
    return bright,notbright,brights
cache = {}

def getRoughnessData(image_id, roughness,contourns):
    if image_id not in cache:
        cache[image_id] = {}

    if "rough" not in cache[image_id]:
        arr=[]
        for c in contourns:
            arr.append(getRough(c))
        
        cache[image_id]["rough"] = arr
    round=0
    notRound=0
    rounds=[]
    for c in cache[image_id]["rough"]:
        if (c>roughness):
            rounds.append(1)
            round+=1
        else:
            rounds.append(0)
            notRound+=1
    return round,notRound,rounds


def getBrightnessData(image_id,brightness, img,contourns):
    if image_id not in cache:
        cache[image_id] = {}

    if "bright" not in cache[image_id]:
        arr=[]
        for c in contourns:
            arr.append(getBrightness(img,c))

        cache[image_id]["bright"] = arr
    bright=0
    notbright=0
    brights=[]
    for c in cache[image_id]["bright"]:
        if (c>brightness):
            bright+=1
            brights.append(1)
        else:
            notbright+=1
            brights.append(0)
    return bright,notbright,brights        


def show_segmentation(img, contours):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    background = int(np.argmax(hist))

    difference = np.abs(gray.astype(np.int16) - background)
    mask = (difference > 11).astype(np.uint8) * 255

    overlay = img.copy()
    cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[1].imshow(mask, cmap="gray")
    axes[1].set_title("Before morphology")
    axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Detected contours")

    for ax in axes:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


def compare_masks(img, tolerance=11):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    background = int(np.argmax(hist))

    difference = np.abs(gray.astype(np.int16) - background)
    raw_mask = (difference > tolerance).astype(np.uint8) * 255

    kernel3 = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)
    )
    kernel7 = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (7, 7)
    )

    mask3 = cv2.morphologyEx(
        raw_mask, cv2.MORPH_CLOSE, kernel3
    )
    mask7 = cv2.morphologyEx(
        raw_mask, cv2.MORPH_CLOSE, kernel7
    )

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(raw_mask, cmap="gray")
    axes[0].set_title("Raw threshold")

    axes[1].imshow(mask3, cmap="gray")
    axes[1].set_title("Closing 3x3")

    axes[2].imshow(mask7, cmap="gray")
    axes[2].set_title("Closing 7x7")

    for ax in axes:
        ax.axis("off")

    plt.tight_layout()
    plt.show()
