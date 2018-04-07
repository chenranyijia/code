import sys
import os
import codecs
import cv2
import shutil

os.chdir('/home/chenran/software/TT100K/data')
catg = {}
catg1 = {}
im_info = open('annotation_train.txt').readlines()

new_annotation = open('/home/chenran/Desktop/data/data_without_argument/train/train_annotation.txt','w')
new_train_ids = open('/home/chenran/Desktop/data/data_without_argument/train/train_ids.txt','w')
valid_new_annotation = open('/home/chenran/Desktop/data/data_without_argument/valid/valid_annotation.txt','w')
valid_new_train_ids = open('/home/chenran/Desktop/data/data_without_argument/valid/valid_ids.txt','w')

min_num = 40
min_num1 = 20

train_img_path = '/home/chenran/Desktop/data/data_without_argument/train/train_img'
if not os.path.exists(train_img_path):
    os.mkdir(train_img_path)

valid_img_path = '/home/chenran/Desktop/data/data_without_argument/valid/valid_img'
if not os.path.exists(valid_img_path):
    os.mkdir(valid_img_path)

for img_infom in im_info:
    img_infom = img_infom.strip().split(';')
    img_name = 'train/'+img_infom[0]+'.jpg'
    if not os.path.exists(img_name):
        print 'not found img'
        continue
    L = (len(img_infom)-2)/5
    flag = False
    for i in range(L):
        cat = img_infom[5*i+5]
        if cat not in catg:
            flag = True
            break
        elif catg[cat] < min_num:
            flag = True
            break
    if flag:
        for i in range(L):
            cat = img_infom[5*i+5]
            if cat not in catg:
                catg[cat] = 1
            else:
                catg[cat] += 1
        shutil.copy(img_name, train_img_path)
        for k in range(len(img_infom)):
            new_annotation.write(img_infom[k])
            new_annotation.write(';')
        new_annotation.write('\n')
        new_train_ids.write(img_infom[0])
        new_train_ids.write('\n')
    else:
        flag1 = False
        for i in range(L):
            cat1 = img_infom[5 * i + 5]
            if cat1 not in catg1:
                flag1 = True
                break
            elif catg1[cat1] < min_num1:
                flag1 = True
                break
        if flag1:
            for i in range(L):
                cat1 = img_infom[5 * i + 5]
                if cat1 not in catg1:
                    catg1[cat1] = 1
                else:
                    catg1[cat1] += 1
            shutil.copy(img_name, valid_img_path)
            for k in range(len(img_infom)):
                valid_new_annotation.write(img_infom[k])
                valid_new_annotation.write(';')
            valid_new_annotation.write('\n')
            valid_new_train_ids.write(img_infom[0])
            valid_new_train_ids.write('\n')

new_annotation.close()
new_train_ids.close()
valid_new_annotation.close()
valid_new_train_ids.close()

print 'catg', catg
mins = 10
for key in catg.keys():
    if catg[key] > mins:
        mins = catg[key]
print 'mins', mins

print 'catg1', catg1
mins1 = 10
for key in catg1.keys():
    if catg1[key] > mins1:
        mins1 = catg1[key]
print 'mins1', mins1
