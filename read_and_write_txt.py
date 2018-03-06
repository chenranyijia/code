import os
import cv2

os.chdir('/home/chenran/software/TT100K/data')
annoc = open('train_annotation.txt').readlines()
text = open('re_annotation.txt', 'w')

for line in annoc:
    im_info = line.strip().split(';')
    text.write(im_info[0])
    text.write(';')
    #img = cv2.imread('train/'+str(im_info[0])+'.jpg')
    for i in range((len(im_info)-2)/5):
        x1 = int(im_info[5*i+1])
        if x1 <= 0:
            x1=1
        x2 = int(im_info[5*i+2])
        if x2 <= 0:
            x2=1
        x3 = int(im_info[5*i+3])
        if x3 >= 2047:
            x3 = 2046
        x4 = int(im_info[5*i+4])
        if x4 >= 2047:
            x4 = 2046
        text.write(str(x1))
        text.write(';')
        text.write(str(x2))
        text.write(';')
        text.write(str(x3))
        text.write(';')
        text.write(str(x4))
        text.write(';')
        text.write(im_info[5*i+5])
        text.write(';')
    text.write('\n')

