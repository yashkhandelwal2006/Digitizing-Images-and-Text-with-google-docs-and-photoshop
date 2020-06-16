import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt

def ocr():
    img=cv2.imread("scan.png")
    img=cv2.resize(img,None,fx=1.7,fy=1.7,interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel=np.ones((1,1),np.uint8)
    img=cv2.dilate(img,kernel,iterations=1)
    img=cv2.erode(img,kernel,iterations=1)
    custom_config = r'-l eng --psm 1'
    text = pytesseract.image_to_string(img,config=custom_config)
    te=[]
    for i in text.split("\n"):
        if len(i)>3:
            te.append(i)
    return te
#img=cv2.imread("scan1.png")
#text=ocr(img)
#print(text)
#plt.imshow(img)
#plt.show()
