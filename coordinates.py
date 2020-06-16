import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import pyautogui
import time
from yolo import yolo_pred_image
from copy import deepcopy

def sift_coordinates(img1,img2):
    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(des1,des2,k=2)
    matchesMask = [[0,0] for i in range(len(matches))]
    all_mapped=[]
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
            pt1 = kp1[m.queryIdx].pt
            pt2 = kp2[m.trainIdx].pt
            all_mapped.append((pt1,pt2))
    return all_mapped,kp1,kp2,matches,matchesMask

def get_coordinates(img1,img2,Y):
    coordnates=yolo_pred_image(img1)
    if coordnates!=0: 
        start_point,end_point=coordnates
        img1=img1[start_point[1]:end_point[1],start_point[0]:end_point[0]]

        all_mapped,kp1,kp2,matches,matchesMask=sift_coordinates(img1,img2)

        towards_right=9999
        towards_left=9999
        towards_up=9999
        towards_down=9999
        right_point=-1
        left_point=-1
        up_point=-1
        down_point=-1
        right_point_o=-1
        left_point_o=-1
        up_point_o=-1
        down_point_o=-1

        for data in all_mapped:
            X=data[0]
            if X[0]!=Y[0] and X[1]!=Y[1]:  
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(X, Y)]))
                if X[0]>Y[0] and towards_right>distance:
                    towards_right=distance
                    right_point=data[1][0]
                    right_point_o=X[0]
                if X[0]<Y[0] and towards_left>distance:
                    towards_left=distance
                    left_point=data[1][0]
                    left_point_o=X[0]
                if X[1]>Y[1] and towards_down>distance:
                    towards_down=distance
                    down_point=data[1][1]
                    down_point_o=X[1]
                if X[1]<Y[1] and towards_up>distance:
                    towards_up=distance
                    up_point=data[1][1]
                    up_point_o=X[1]

        if right_point<=left_point:
            towards_right=9999
            for data in all_mapped:
                X=data[0]
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(X, Y)]))
                if distance<towards_right and X[0]>Y[0] and data[1][0]>left_point:
                    towards_right=distance
                    right_point=data[1][0]
        if down_point<=up_point:
            towards_down=9999
            for data in all_mapped:
                X=data[0]
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(X, Y)]))
                if distance<towards_down and X[1]>Y[1] and data[1][1]>up_point:
                    towards_down=distance
                    down_point=data[1][1]
        if right_point<left_point or right_point==-1:
            right_point=img2.shape[1]
        if down_point<up_point or down_point==-1:
            down_point=img2.shape[0]
        if left_point==-1:
            left_point=0
        if up_point ==-1:
            up_point=0
        if right_point_o==-1:
            right_point_o=img1.shape[1]
        if down_point_o==-1:
            down_point_o=img1.shape[0]
        if left_point_o==-1:
            left_point_o=0
        if up_point_o ==-1:
            up_point_o=0
        #print(right_point_o,left_point_o,down_point_o,up_point_o)        
        #cv2.rectangle(img1, Y, (Y[0]+5,Y[1]+5), (0,0,255), 25)
        img3=img1[int(up_point_o):int(down_point_o),int(left_point_o):int(right_point_o)]
        #cv2.rectangle(img1, (int(left_point_o),int(up_point_o)),(int(right_point_o),int(down_point_o)), (0,255,0), 10)
        #cv2.rectangle(img2, (int(left_point),int(up_point)),(int(right_point),int(down_point)), (0,255,0), 10)
        img4=img2[int(up_point):int(down_point),int(left_point):int(right_point)]
        new_Y=[int(Y[0]-left_point_o),int(Y[1]-up_point_o)]
        #print(img3.shape)
        #print(img4.shape)
        #cv2.rectangle(img3, (new_Y[0],new_Y[1]), (new_Y[0]+5,new_Y[1]+5), (0,0,255), 25)
        y_ratio=img3.shape[0]/img4.shape[0]
        x_ratio=img3.shape[1]/img4.shape[1]
        Y_out=[0]*2
        Y_out[0]=int(new_Y[0]/x_ratio+left_point)
        Y_out[1]=int(new_Y[1]/y_ratio+up_point)
        #cv2.rectangle(img2, (Y_out[0],Y_out[1]), (Y_out[0]+5,Y_out[1]+5), (0,0,255), 25)
        #plt.imshow(img1,cmap="gray")
        #plt.show()
        #plt.imshow(img2,cmap="gray")
        #plt.show()
        return Y_out



'''
    for j in range(int(left_point),int(right_point),25): 
        for i in range(int(down_point),int(up_point),25):
            cv2.rectangle(img2, (j,i), (j+5,i+5), (0,0,255), 10)

    all_mapped,kp1,kp2,matches,matchesMask=sift_coordinates(img1[int(up_point_o):int(down_point_o),int(left_point_o):int(right_point_o)],img2[int(up_point):int(down_point),int(left_point):int(right_point)])
    min_dist=9999
    final_coor=()
    for data in all_mapped:
        X=data[0]
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(X, Y)]))
        if distance<min_dist:
            min_dist=distance
            final_coor=data[1]

    #cv2.rectangle(img4, (int(final_coor[0]),int(final_coor[1])), (int(final_coor[0])+5,int(final_coor[1])+5), (255,0,0), 10)
    print(final_coor)        

    draw_params = dict(matchColor = (0,255,0),singlePointColor = (255,0,0),matchesMask = matchesMask,flags = 0)
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

    plt.imshow(img3,cmap="gray")
    plt.show()

'''
