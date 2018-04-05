
# -*- coding: utf-8 -*-
import os
os.chdir('C:\Users\chenran\Desktop')
import cv2
import numpy as np
img = cv2.imread('92338.jpg')

'''
for i in range(2):
    for j in range(1,4):
        new_img = img[512*i:512*(i+1),512*j:512*(j+1),:]
        cv2.imwrite('{}_{}.jpg'.format(i,j), new_img)
'''
#img = cv2.resize(img,(1024,1024))


#img1 = img
for i in range(4):
    for j in range(4):
        cv2.rectangle(img,(512*i,512*j),(512*(i+1),512*(j+1)),(0,255,0),2)

        
cv2.rectangle(img,(506,0),(1055,549),(0,0,255),3)
#img_1 = img1[0:549,506:1055,:]
#cv2.imwrite('img_1.jpg',img_1)

cv2.rectangle(img,(1055,70),(1502,517),(0,0,255),3)
#img_2 = img1[70:517,1055:1502,:]
#cv2.imwrite('img_2.jpg',img_2)

cv2.rectangle(img,(1502,42),(2014,554),(0,0,255),3)
#img_3 = img1[42:553,1502:2014,:]
#cv2.imwrite('img_3.jpg',img_3)
#cv2.rectangle(img,(512*i,512*j),(512*(i+1),512*(j+1)),(0,255,0),1)
#img = img[412:1124,412:1838,:]
#cv2.imshow('',img)
img = img[:1054,412:,:]
cv2.imwrite('segmentation.jpg',img)
