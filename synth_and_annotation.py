import random
import os
import numpy as np
import cv2
from glob import glob

synth_annotation = open('/home/chenran/software/TT100K/data/synth_annotation.txt', 'w')
synth_id= open('/home/chenran/software/TT100K/data/synth_id.txt', 'w')


img_names = glob(os.path.join('/home/chenran/Desktop/123/virtual_sign', '*.jpg'))
while img_names != '':
    img_names = glob(os.path.join('/home/chenran/Desktop/123/virtual_sign', '*.jpg'))
    back_imgs = glob(os.path.join('/home/chenran/software/TT100K/data/nosign_1_split', '*.jpg'))
    img_num = np.random.randint(1,6,1)[0]
    img_name = random.sample(img_names, img_num)
    back_img_name = random.sample(back_imgs, 1)[0]
    imgs = []
    max_H = 0
    max_W = 0
    for i in range(img_num):
        img = cv2.imread(img_name[i])
        imgs.append(img)
        max_H = max(max_H, img.shape[0])
        max_W = max(max_W, img.shape[1])
    back_img = cv2.imread(back_img_name)
    start_x = int(np.random.uniform(0, max_W-1, 1))
    start_y = int(np.random.uniform(0, max_H-1, 1))
    H_num = (back_img.shape[0]-start_y)/max_H
    W_num = (back_img.shape[1]-start_x)/max_W
    if H_num * W_num < img_num:
        print 'fail',
    else:
        synth_annotation.write(back_img_name.split('/')[-1].split('.')[0])
        synth_annotation.write(';')
        synth_id.write(back_img_name.split('/')[-1].split('.')[0])
        synth_id.write('\n')
        indices_i_j = random.sample(range(H_num*W_num), img_num)
        for k in range(img_num):
            indice_i_j = indices_i_j[k]
            indice_i = indice_i_j/W_num
            indice_j = indice_i_j - W_num*indice_i
            x_min = int(start_x + indice_j*max_W + np.random.uniform(0, max_W-imgs[k].shape[1], 1)[0])
            y_min = int(start_y + indice_i*max_H + np.random.uniform(0, max_H-imgs[k].shape[0], 1)[0])
            back_img[y_min:y_min+imgs[k].shape[0], x_min:x_min+imgs[k].shape[1],:] = imgs[k]

            synth_annotation.write(str(x_min))
            synth_annotation.write(';')
            synth_annotation.write(str(y_min))
            synth_annotation.write(';')
            synth_annotation.write(str(x_min+imgs[k].shape[1]))
            synth_annotation.write(';')
            synth_annotation.write(str(y_min+imgs[k].shape[0]))
            synth_annotation.write(';')
            sign_label = img_name[k].split('/')[-1].split('.')[0].split('_')[-1]
            synth_annotation.write(sign_label)
            synth_annotation.write(';')
            os.remove(img_name[k])
        synth_annotation.write('\n')
        cv2.imwrite('/home/chenran/software/TT100K/data/synth_imgs/'+back_img_name.split('/')[-1], back_img)
        os.remove(back_img_name)

synth_id.close()
synth_annotation.close()
