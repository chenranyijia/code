import os
os.chdir('/home/chenran/Desktop/123')
import cv2
import numpy as np
import math
import random
from glob import glob
total_sign = 1500





def conversion(img):
    new_img = np.zeros(img.shape)
    alpha = np.random.uniform(-math.pi/8, math.pi/8, 1)
    coeff = np.random.uniform(0.9,1.1,4)
    light = np.random.uniform(0.6, 1.8, 1)
    resize = np.random.uniform(0.7,1.4,1)
    aspect_ratio = np.random.uniform(0.8,1,1)
    new_height = int(img.shape[0]*resize)
    new_width = int(img.shape[1]*resize*aspect_ratio)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_i = int(coeff[0] * np.cos(alpha)*i - coeff[1] * np.sin(alpha)*j)
            new_j = int(coeff[2] * np.sin(alpha)*i + coeff[3] * np.cos(alpha)*j)
            new_i = np.clip(new_i, 0, img.shape[0]-1)
            new_j = np.clip(new_j, 0, img.shape[1]-1)
            for c in range(img.shape[2]):
                new_img[i,j,c] = int(light*img[new_i, new_j, c])
                new_img[i,j,c] = np.clip(new_img[i,j,c], 0, 255)

    new_img = cv2.resize(new_img,(new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return new_img
Threshold_min = 16
Threshold_max = 256
#back_grounds = glob(os.path.join('pic', '*.jpg'))
for sign in ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27', 'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5','pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']:
    k = 0
    sign_names = glob(os.path.join('/home/chenran/software/TT100K/data/train_signs', sign, '*.jpg'))
    #for i in range(total_sign - len(sign_names)):
    while total_sign-len(sign_names)-k >= 0:
        single_sign_name = random.choice(sign_names)
        single_sign = cv2.imread(single_sign_name)
        single_sign = conversion(single_sign)
        if single_sign.shape[0] >= Threshold_min and single_sign.shape[1] >= Threshold_min and single_sign.shape[0] <= Threshold_max and single_sign.shape[1] <= Threshold_max:
            #back_ground = random.choice(back_grounds)
            #back_ground = cv2.imread(back_ground)
            k += 1
            cv2.imwrite('/home/chenran/Desktop/123/virtual_sign/'+str('%04d' %k)+'_'+sign+'.jpg', single_sign)
        else:
            cv2.imwrite('/home/chenran/Desktop/123/wrong_sign/' + str('%04d' % k) + '_' + sign + '.jpg', single_sign)
