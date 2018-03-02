import os
import cv2
import json
import numpy as np
import numpy.random as nr

os.chdir('/home/chenran/software/TT100K')

annotation = json.loads(open('data/annotations.json').read())
indexs = open('data/train/ids.txt').readlines()
categorys = ['i5','pl30','pl50','pl60','pl80','pl100', 'pl120']
for imageid in indexs:
    Flag = 0
    imageid = imageid.strip()
    img = annotation['imgs'][imageid]
    img_path = '/home/chenran/software/TT100K/data/'+img['path']
#    image = pl.imread(img_path)
    for id in range(len(img['objects'])):
        category = img['objects'][id]['category']
        if category in categorys:
            image = cv2.imread(img_path)
            Flag = 1
            break
    if Flag == 1:
        indices = np.zeros([7])
        for id in range(len(img['objects'])):
            category = img['objects'][id]['category']
            if category in categorys:
                x1 = int(round(img['objects'][id]['bbox']['xmin'])) - nr.randint(3,6)
                if x1 <= 0:
                    x1 = 0

                y1 = int(round(img['objects'][id]['bbox']['ymin'])) - nr.randint(3,6)
                if y1 <= 0:
                    y1 = 0

                x2 = int(round(img['objects'][id]['bbox']['xmax'])) + nr.randint(3,6)
                if x2 >= image.shape[0]-1:
                    x2 = image.shape[0]-1

                y2 = int(round(img['objects'][id]['bbox']['ymax'])) + nr.randint(3,6)
                if y2 >= image.shape[1]-1:
                    y2 = image.shape[1] -1
                crop_img = image[y1:y2, x1:x2,:]
                for k in range(7):
                    if category == categorys[k]:
                        indices[k] += 1

                cv2.imwrite('data/signs/'+str(category)+'/'+str(imageid)+'_'+str(int(indices[k]))+'.jpg', crop_img)
