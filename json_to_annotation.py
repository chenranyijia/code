import os
import cv2
import json
import numpy as np
import numpy.random as nr

os.chdir('/home/chenran/software/TT100K')

annotation = json.loads(open('data/annotations.json').read())
indexs = open('data/train_TT100K/ids.txt').readlines()
categorys = ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27',
             'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5',
             'pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']
annotation_test = open('data/annotation_train.txt', 'w')

if not os.path.exists('data/train_signs'):
    os.mkdir('data/train_signs')

for sign in categorys:
    if not os.path.exists('data/train_signs/'+sign):
        os.mkdir('data/train_signs/'+sign)
indices = dict(zip(categorys, range(len(categorys))))
for imageid in indexs:
    Flag = 0
    imageid = imageid.strip()
    img = annotation['imgs'][imageid]
    img_path = '/home/chenran/software/TT100K/data/train_TT100K/'+img['path'].split('/')[-1]
    if img['path'].split('/')[0] == 'train':
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
        #indices = dict(zip(categorys, range(len(categorys))))
        for id in range(len(img['objects'])):
            category = img['objects'][id]['category']
            if category in categorys:
                indices[category] += 1
                x1 = int(round(img['objects'][id]['bbox']['xmin']))
                if x1 <= 0:
                    x1 = 0
                annotation_test.write(str(x1))
                annotation_test.write(';')

                y1 = int(round(img['objects'][id]['bbox']['ymin']))
                if y1 <= 0:
                    y1 = 0
                annotation_test.write(str(y1))
                annotation_test.write(';')

                x2 = int(round(img['objects'][id]['bbox']['xmax']))
                if x2 >= image.shape[0]-1:
                    x2 = image.shape[0]-1
                annotation_test.write(str(x2))
                annotation_test.write(';')

                y2 = int(round(img['objects'][id]['bbox']['ymax']))
                if y2 >= image.shape[1]-1:
                    y2 = image.shape[1] -1
                annotation_test.write(str(y2))
                annotation_test.write(';')
                annotation_test.write(category)
                annotation_test.write(';')
                new_img = image[y1:y2, x1:x2, :]
                cv2.imwrite('data/train_signs/'+category+'/'+imageid+'_'+category+ '_' +str(indices[category])+'.jpg', new_img)
        annotation_test.write('\n')
print indices
annotation_test.close()
#{'pl120': 231, 'w57': 305, 'io': 586, 'w55': 150, 'pl100': 471, 'ip': 197, 'w59': 165, 'w13': 129, 'pl5': 298, 'pl80': 609, 'p27': 98, 'p26': 528, 'p23': 175, 'ph5': 94, 'ph4': 102, 'pl20': 122, 'il100': 95, 'pl60': 554, 'pl40': 900, 'pg': 122, 'pm20': 139, 'pn': 1921, 'po': 772, 'pr40': 174, 'il80': 202, 'pl30': 398, 'wo': 117, 'i2': 297, 'i5': 1047, 'i4': 477, 'p10': 252, 'p11': 978, 'p12': 116, 'p19': 98, 'pne': 1415, 'ph4.5': 142, 'p3': 126, 'p6': 86, 'p5': 274, 'il60': 342, 'pm55': 132, 'w32': 110, 'pl50': 687, 'pm30': 108, 'pl70': 133}
