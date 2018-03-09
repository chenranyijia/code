import os
import cv2
import json
import numpy as np
import numpy.random as nr

os.chdir('/home/chenran/software/TT100K')

annotation = json.loads(open('data/annotations.json').read())
indexs = open('data/test/ids.txt').readlines()
categorys = ['i5','pl30','pl50','pl60','pl80','pl100', 'pl120']
annotation_test = open('data/annotation_test.txt', 'w')

for imageid in indexs:
    Flag = 0
    imageid = imageid.strip()
    img = annotation['imgs'][imageid]
    img_path = '/home/chenran/software/TT100K/data/'+img['path']
    if img['path'].split('/')[0] == 'test':
#    image = pl.imread(img_path)
      for id in range(len(img['objects'])):
        category = img['objects'][id]['category']
        if category in categorys:
            image = cv2.imread(img_path)
            Flag = 1
            break
      if Flag == 1:
        annotation_test.write(imageid)
        annotation_test.write(';')
        indices = np.zeros([7])
        for id in range(len(img['objects'])):
            category = img['objects'][id]['category']
            if category in categorys:
                x1 = int(round(img['objects'][id]['bbox']['xmin']))
                if x1 <= 0:
                    x1 = 0
                annotation_test.write(str(x1))
                annotation_test.write(';')

                y1 = int(round(img['objects'][id]['bbox']['ymin']))
                if y1 <= 0:
                    y1 = 0
                annotation_test.write(str(x1))
                annotation_test.write(';')

                x2 = int(round(img['objects'][id]['bbox']['xmax']))
                if x2 >= image.shape[0]-1:
                    x2 = image.shape[0]-1
                annotation_test.write(str(x1))
                annotation_test.write(';')

                y2 = int(round(img['objects'][id]['bbox']['ymax']))
                if y2 >= image.shape[1]-1:
                    y2 = image.shape[1] -1
                annotation_test.write(str(x1))
                annotation_test.write(';')
                annotation_test.write(category)
                annotation_test.write(';')
        annotation_test.write('\n')
