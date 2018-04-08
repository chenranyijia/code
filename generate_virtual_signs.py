import os
os.chdir('/home/chenran/Desktop/data/data_without_argument/train/synth')
import cv2
import numpy as np
import math
import random
from glob import glob

total_sign = 300
if not os.path.exists('vir_signs/'):
    os.mkdir('vir_signs')

def conversion(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #generate light transformer random number
    inte = np.random.randint(0,2,1)
    if inte == 0:
        factor = np.random.uniform(0.6,0.9,1)
    else:
        factor = np.random.uniform(1.2, 1.7, 1)
        if inte != 1:
            print 'error'

    for m in np.arange(img.shape[0]):
        for n in np.arange(img.shape[1]):
            pixel = factor*hsv[m,n,2]
            pixel = min(max(10,pixel), 255)
            hsv[m,n,2] = pixel
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    new_img = np.zeros(img.shape)

    alpha1 = np.random.uniform(-math.pi/32, math.pi/32, 1)
    alpha2 = np.random.uniform(-math.pi/8, math.pi/8, 1)
    coeff = np.random.uniform(0.9,1.1,4)
    #light = np.random.uniform(0.6, 1.8, 1)
    resize = np.random.uniform(0.7,1.4,1)
    aspect_ratio = np.random.uniform(0.7,1,1)
    new_height = int(max(img.shape[0], img.shape[1])*resize)
    new_width = int(new_height*aspect_ratio)
    #new_img = np.zeros((new_height, new_width, 3))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_i = int(coeff[0] * np.cos(alpha2)*i - coeff[1] * np.sin(alpha1)*j)
            new_j = int(coeff[2] * np.sin(alpha1)*i + coeff[3] * np.cos(alpha2)*j)
            new_i = np.clip(new_i, 0, img.shape[0]-1)
            new_j = np.clip(new_j, 0, img.shape[1]-1)
            new_img[i,j,:] = img[new_i, new_j, :]
            #for c in range(img.shape[2]):
            #    new_img[i,j,c] = int(light*img[new_i, new_j, c])
            #    new_img[i,j,c] = np.clip(new_img[i,j,c], 0, 255)
    if min(new_width, new_height) < 16:
        new_width = 16
        new_height = int(float(new_width)/aspect_ratio)
    new_img = cv2.resize(new_img,(new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return new_img

T_min = 16
T_max = 256
#back_grounds = glob(os.path.join('pic', '*.jpg'))
for sign in ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27', 'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5','pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']:
    sign_names = glob(os.path.join('signs', sign, '*.jpg'))
    if not os.path.exists('vir_signs/'+sign):
        os.mkdir('vir_signs/'+sign)
    #for i in range(total_sign - len(sign_names)):
    replic_N = total_sign/len(sign_names)
    print replic_N
    for i in range(replic_N):
        for im_name in sign_names:
            img1 = cv2.imread(im_name)
            img = conversion(img1)
            if img.shape[0] >= T_min and img.shape[1] >= T_min and img.shape[0] <= T_max and img.shape[1] <= T_max:
                cv2.imwrite('vir_signs/'+sign+'/'+'vir_'+str(i)+im_name.split('/')[-1], img)
            else:
                cv2.imwrite('wrong/' + im_name.split('/')[-1], img)
