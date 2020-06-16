
import time
import cv2
import numpy as np
from PIL import Image,ImageChops,ImageFilter
import numpy as np
import sys
sys.path.insert(1, 'C:/Users/yash/Desktop/conputevision and python/YOLO-1/U-2-Net')
from segmentation import run
from filestack import Client
from seleniumScript import main
from ocr import ocr

def getPublicURL():
    client = Client("AYfgWcwErT3KN8oLDeumcz")
    params = {'mimetype': 'image/jpg'}
    new_filelink = client.upload(filepath="scan.png")
    return new_filelink.url

def run1():
    print("scan input image")
    cap = cv2.VideoCapture('http://192.168.43.51:8080/video')
    f=np.zeros((100,100))
    diff=0
    count=0
    found_frame=0
    while(True):
        ret, frame = cap.read()
        frame1=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(frame1, (100,100), interpolation = cv2.INTER_AREA)
        ret,thresh=cv2.threshold(resized,127,255,cv2.THRESH_BINARY)
        thresh=thresh/255
        diff_now=abs(np.sum(np.subtract(thresh,f)))
        if abs(diff_now-diff)<60:
            count+=1
        else:
            count=0
        if count==75:
            found_frame=frame
            break
        diff=diff_now
        f=thresh
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    print("image captured")
    scanned_image=im_pil = Image.fromarray(found_frame)
    if scanned_image.size[0] > 1024 or scanned_image.size[1] > 1024:
        scanned_image.thumbnail((1024, 1024))
    size=scanned_image.size
    res = run(np.array(scanned_image),size)
    mask = res.convert("L")
    empty = Image.new("RGBA", size, 0)
    scanned_image = Image.composite(scanned_image, empty, mask)
    return scanned_image

for i in range(1,3):
    time.sleep(8)
    image=run1()
    img=image.convert("RGBA")
    data = np.array(img) 
    red, green, blue, alpha = data.T 
    data = np.array([blue, green, red, alpha])
    data = data.transpose()
    img = Image.fromarray(data)
    img = img.crop(img.getbbox())
    img.save("scan.png")
    print("image saved")
    
    print("calling ocr")
    text=ocr()
    print("ocr call completed")
    if len(text)>0:
        main(text1=text)
        print("text insertion done")
    else:
        URL=getPublicURL()
        print(URL)
        main(URL)
        print("image insertion done")
    #style=Image.open("tshirt.jpg")
    #print(style.size)
    #img=Image.fromarray(cv2.resize(np.array(img),dsize=None,fx=0.3,fy=0.3,interpolation = cv2.INTER_CUBIC))
    #img=Image.fromarray(cv2.resize(np.array(img),dsize=(112,200),interpolation = cv2.INTER_CUBIC))
    #style.paste(img, (250, 80), img)
    #style.show()
