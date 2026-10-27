
import cv2  
import numpy as np
import matplotlib.pyplot as plt
import csv
import plasticlib
from plasticlib import *


min_area=80
def segment(img,tolerance=11,kernel_size=7): #get the contourns of the elements
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    background = int(np.argmax(hist))
    difference = np.abs(img.astype(np.int16) - background)

    # Pixels sufficiently different from background become white
    mask = (difference > tolerance).astype(np.uint8) * 255
# Kernel used to connect small gaps
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (kernel_size, kernel_size)
    )

    # Fill small gaps and connect nearby regions
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, kernel
    )
    # Remove small isolated noise
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3,3)
    )
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    #remove noise
    contours_filtered = [
    c for c in contours
    if min_area <= cv2.contourArea(c) 
]
    return contours_filtered


#clean the grey pixel around the black elements cause they gets wrongly included
# to do so find the common intensity of the found element and keep only the pixels close like tolerance
def clean_contour(img, contour, tolerance=25, bin_size=15):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create a mask for this contour
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, cv2.FILLED)

    pixels = gray[mask > 0]
    if len(pixels) == 0:
        return np.zeros_like(mask)

    # Group intensities into bins of 5 and find the most common bin
    bins = pixels // bin_size
    dominant_bin = np.bincount(bins, minlength=256 // bin_size).argmax()
    dominant_intensity = dominant_bin * bin_size + bin_size // 2

    # Keep only pixels close to the dominant intensity
    cleaned = np.zeros_like(mask)
    keep = (
        (mask > 0) &
        (np.abs(gray.astype(np.int16) - dominant_intensity) <= tolerance)
    )
    cleaned[keep] = 255

    return cleaned


def Get_datas(imrgb,contour):
    return getMediumColor(imrgb,contour),getMediumBrightness(imrgb,contour),getMediumRough(imrgb,contour)


#Open imgs
imgF = cv2.imread('FRA.png') 
imgP = cv2.imread('PEL.png') 
imgT = cv2.imread('TAR.png') 
imgs=[imgF,imgP,imgT]
#segment
cont1=segment(imgF)
cont2=segment(imgP)
cont3=segment(imgT)
conts=[cont1,cont2,cont3]

#clean segments
for i in range(len(conts)):
    cleaned_contours = []

    for contour in conts[i]:
        cleaned_mask = clean_contour(imgs[i], contour)

        new_contours, _ = cv2.findContours(
            cleaned_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cleaned_contours.extend(
            c for c in new_contours if cv2.contourArea(c) >= 65
        )

    conts[i] = cleaned_contours

a1,b1,c1=Get_datas(imgF,cont1)

a2,b2,c2=Get_datas(imgP,cont2)

a3,b3,c3=Get_datas(imgT,cont3)

medcolor=[a1,a2,a3]
medbrightness=[b1,b2,b3]
medroughness=[c1,c2,c3]
for i in range(3):
    medcolor[i],medbrightness[i],medroughness[i]=Get_datas(imgs[i],conts[i])

print(medcolor)
print(medbrightness)
print(medroughness)

#optional control for segmentation
#for i in range(3):
#    show_segmentation(imgs[i],conts[i])

#only brightness and roundness there are 4 cases: [1,1],[1,0],[0,1],[0,0]

breaker=False
imgcases=[[(0,1)],[(1,1),(1,0)],[(0,0)]]
maxtruth=0
bestrough=0
bestbright=0
cuenta=0
for i in conts:
    for j in i:
        cuenta+=1

print(f"{cuenta} contourns")

blackdif=0.05
#Finding the optimal search values
for roughness in range(600,800,1):
    rough=roughness/1000
    for brightness in range(300,1100):
        brightx=brightness/10
        truth=0
        cases=[]
        for i in range(len(imgs)):
            img=imgs[i]
            case=[0,0,0,0]
            round,notround,rounds=getRoughnessData(f"image{i}",rough,conts[i])
            bright,notbright,brights=getBrightnessData(f"image{i}",brightx,img,conts[i])
            blackround,blacknotround,blackrounds=getRoughnessData(f"image{i}",rough+blackdif,conts[i])
            
            for j in range(len(rounds)):
                if(brights[j]==0):
                    if (rounds[j]!=blackrounds[j]):
                        rounds[j]=blackrounds[j]
                nowcase=(rounds[j],brights[j])
                if nowcase in imgcases[i]:
                    truth+=1
                else:
                    pass
                if(rounds[j]==1 and brights[j]==1):
                    case[0]=1
                if(rounds[j]==1 and brights[j]==0):
                    case[1]=1
                if(rounds[j]==0 and brights[j]==1):
                    case[2]=1
                if(rounds[j]==0 and brights[j]==0):
                    case[3]=1
            cases.append(case)
        nice=True

        for i in range(4):
            same=0
            for case in cases:
                if case[i]==1:
                    if(same):
                        nice=False
                        break
                    same=1
        if (truth>maxtruth):
            maxtruth=truth
            bestrough=rough
            bestbright=brightx
            print(f"truth: {truth}/{cuenta}")
        if nice:
            print(f"good values! Brightness: {brightx} and roughness: {rough}")
            br=brightx
            ro=rough
            breaker=True
            break
    if(breaker):
        break
print(f"bestbright: {bestbright}, bestrough: {bestrough}")
brightx, rough = bestbright, bestrough

#check to see what we got wrong, to optimiz our model next time
for i in range(len(imgs)):
    img = imgs[i]
    wrong_contours = []
    wrong_info = []

    _, _, rounds = getRoughnessData(
        f"image{i}", rough, conts[i]
    )
    _, _, brights = getBrightnessData(
        f"image{i}", brightx, img, conts[i]
    )
    _, _, blackrounds = getRoughnessData(
        f"image{i}", rough + blackdif, conts[i]
    )

    for j in range(len(conts[i])):
        # Match the special rule used in the optimization cycle
        is_round = rounds[j]

        if brights[j] == 0:
            is_round = blackrounds[j]

        nowcase = (is_round, brights[j])

        if nowcase not in imgcases[i]:
            wrong_contours.append(conts[i][j])
            wrong_info.append(
                (
                    j,
                    is_round,
                    brights[j],
                    getRough(conts[i][j]),
                    getBrightness(img, conts[i][j])
                )
            )

    result = img.copy()
    cv2.drawContours(
        result, wrong_contours, -1, (0, 0, 255), 2
    )

    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title(
        f"Image {i} — wrong: {len(wrong_contours)}/{len(conts[i])}"
    )
    plt.axis("off")
    plt.show()

    print(f"\nImage {i}: misclassified contours")
    for idx, is_round, is_bright, circ, bval in wrong_info:
        print(
            f"Contour {idx}: round={is_round}, bright={is_bright}, "
            f"circularity={circ:.3f}, brightness={bval:.1f}"
        )


# Test the model on the real image
imagen = "MPs_test.jpg"
csv_file = "MPs_test_bbs.csv"

img = cv2.imread(imagen)
result = img.copy()

brightx, rough = bestbright, bestrough

y_true = []
y_pred = []
correct = 0
wrong = 0
skipped = 0

with open(csv_file, newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        etiqueta = row["label"]

        x_min, y_min, x_max, y_max = map(
            int, [row["x_min"], row["y_min"],
                  row["x_max"], row["y_max"]]
        )

        # Keep coordinates inside the image
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(img.shape[1], x_max)
        y_max = min(img.shape[0], y_max)

        if x_max <= x_min or y_max <= y_min:
            skipped += 1
            continue

        roi = img[y_min:y_max, x_min:x_max]
        contours = segment(roi)

        if not contours:
            print(f"No contour detected for {etiqueta} at {(x_min, y_min)}")
            skipped += 1
            continue

        # Use the largest detected contour inside the annotated box
        c = max(contours, key=cv2.contourArea)

        brightness = getBrightness(roi, c)
        circularity = getRough(c)

        # Same classification rule as your threshold search
        if brightness <= brightx:
            is_round = circularity > rough + blackdif
        else:
            is_round = circularity > rough

        if is_round:
            prediction = "PEL"
        elif brightness > brightx:
            prediction = "FRA"
        else:
            prediction = "TAR"

        y_true.append(etiqueta)
        y_pred.append(prediction)

        is_correct = prediction == etiqueta
        if is_correct:
            correct += 1
            color = (0, 255, 0)       # Green
        else:
            wrong += 1
            color = (0, 0, 255)       # Red

        cv2.rectangle(
            result, (x_min, y_min), (x_max, y_max), color, 2
        )
        cv2.putText(
            result, f"{prediction} {'OK' if is_correct else 'WRONG'}",
            (x_min, max(20, y_min - 5)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
        )

# Results
print(f"Evaluated: {len(y_true)}")
print(f"Correct: {correct}")
print(f"Wrong: {wrong}")
print(f"Skipped: {skipped}")
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import seaborn as sns


if y_true:
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print(f"Weighted precision: {precision_score(y_true, y_pred, average='weighted', zero_division=0):.3f}")
    print(f"Weighted recall: {recall_score(y_true, y_pred, average='weighted', zero_division=0):.3f}")
    print(f"Weighted F1: {f1_score(y_true, y_pred, average='weighted', zero_division=0):.3f}")

    classes = ["FRA", "PEL", "TAR"]
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    plt.figure(figsize=(8, 7))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=classes, yticklabels=classes
    )
    plt.xlabel("Predicted")
    plt.ylabel("Ground truth / annotated")
    plt.title("Confusion matrix")
    plt.tight_layout()
    plt.show()

plt.figure(figsize=(14, 9))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title("Test predictions: green = correct, red = incorrect")
plt.axis("off")
plt.show()
exit()
            
chiaro0scuro=0.5 #we could binary search too
#optional, presnt previous images and have guess belonging in a for cycle to fine tune automatically the
#right values to search for


#da quello che ho visto: nero spigoloso va in TAR, tondo nero va in PEL, così come tondi in generale
# in FRA vanno chiari spigolosi


#open img and decide the belonging



#confusion matrix

