import struct
from ctypes import *
import numpy as np
import cv2
import os
from glob import glob

def writeMnist(data,rows,cols, path_images = "imt_mnist_training_set.data",path_labels="imt_mnist_training_labels.data"):
    _set,_labels = data

    model = 0
    print _set[0].dtype

    if(len(_set[0])>0 and type(_set[0]) == float):
        model = 1
    magic_nums_trainning = 2051
    magic_nums_labels = 2049

    num_training = len(_set)
    header_images = [magic_nums_trainning,num_training,rows,cols*3]
    header_labels = [magic_nums_labels,num_training]
    len_img = rows*cols*3

    header_images_format = '>IIII'
    header_labels_format = '>II'

    len_img_format = '>'+str(len_img)+'B'

    buffer_training_set = create_string_buffer(4*4 + len_img*num_training)
    buffer_training_labels = create_string_buffer(2*4  +  num_training)
    offset = 0

    struct.pack_into(header_images_format,buffer_training_set,offset,*header_images)
    offset += struct.calcsize(header_images_format)
    print(len_img_format)
    for i in range(num_training):
        if(model == 1):
            byte_type = np.array(_set[i])*255
            byte_type = byte_type.astype(np.uint8).ravel()
        else:
            byte_type = _set[i].ravel()
        struct.pack_into(len_img_format,buffer_training_set,offset,*byte_type)
        offset += struct.calcsize(len_img_format)

    file_training_set = open(path_images,'wb')
    file_training_set.write(buffer_training_set)
    offset =  0
    struct.pack_into(header_labels_format,buffer_training_labels,offset,*header_labels)
    offset += struct.calcsize(header_labels_format)
    for i in range(num_training):
        struct.pack_into(">B",buffer_training_labels,offset,_labels[i])
        offset += struct.calcsize(">B")
    file_training_label = open(path_labels,'wb')
    file_training_label.write(buffer_training_labels)

os.chdir('/home/chenran/software/learning_by_association/signs/target')
clses = ['il50', 'il60', 'il70', 'il80', 'il100']
lab_to_num = dict(zip(clses, range(len(clses))))
height = 32
width = 32
data = []
label = []
for cls in clses:
    img_names = glob(os.path.join(cls, '*.jpg'))
    for img_name in img_names:
        img = cv2.imread(img_name)
        n_img = cv2.resize(img,(height,width),interpolation=cv2.INTER_LINEAR)
        n_img = np.reshape(n_img,height*width*3)
        data.append(n_img)
        label.append(lab_to_num[cls])
data = np.array(data)
label = np.array(label)
writeMnist([data, label],32,32, path_images = "t10k-images.idx3-ubyte",path_labels="t10k-label.idx3-ubyte")
