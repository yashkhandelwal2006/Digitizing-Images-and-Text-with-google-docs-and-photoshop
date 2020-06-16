from PIL import Image,ImageChops,ImageFilter
import numpy as np
import sys
sys.path.insert(1, 'C:/Users/yash/Desktop/conputevision and python/YOLO-1/U-2-Net')
from segmentation import run
from coordinates import get_coordinates
import pyautogui
import time
import cv2 
import matplotlib.pyplot as plt


if __name__=="__main__":
    target_test_coordinates=(1500,1500)
    scanned_image = Image.open("ObjectToBeSegemented/object6.jpg")
    if scanned_image.size[0] > 1024 or scanned_image.size[1] > 1024:
        scanned_image.thumbnail((1024, 1024))
    size=scanned_image.size
    res = run(np.array(scanned_image),size)
    mask = res.convert("L")
    empty = Image.new("RGBA", size, 0)
    scanned_image = Image.composite(scanned_image, empty, mask)
    scanned_image.show()
    print("scanning ends here")
    time.sleep(4)
    img1 = cv2.imread("Screenshots/photo.jpg")
    img2 = pyautogui.screenshot()
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    x,y=get_coordinates(img1,img2,target_test_coordinates)
    print(x,y)
    print("mapping complete")
    cv2.rectangle(img2, (x,y), (x+5,y+5), (0,0,255), 25)
    cv2.rectangle(img1, (target_test_coordinates[0],target_test_coordinates[1]), (target_test_coordinates[0]+5,target_test_coordinates[1]+5), (0,0,255), 25)
    
