# Convert annotation information to xml files, written in python.

#encoding=utf-8

import sys
import os
import codecs
import cv2

#########设置路径#########
os.chdir('/home/chenran/software/TT100K/data')
path_img = 'train'
path_xml = 'train_xml'

########打开并读取文件########
fp = open('annotation_train.txt')
fp2 = open('train_sequence.txt', 'w')
uavinfo = fp.readlines()

########利用for循环读取文件内容并写入xml文件########
for i in range(len(uavinfo)):
    line = uavinfo[i]
    line = line.strip().split(';')
    if line[0] != '':
        img = cv2.imread(path_img + '/' + line[0] + '.jpg')
        sp = img.shape
        height = sp[0]
        width = sp[1]
        depth = sp[2]
        name_plus_suffix = line[0]
        name = name_plus_suffix.split('.')[0]
#        remainder = len(line) % 6
#        if remainder == 0:
#            fp2.writelines(name+'\n')
        if name:
            with codecs.open(path_xml + '/' + name + '.xml', 'w', 'utf-8') as xml:
                xml.write('<annotation>\n')
                xml.write('\t<folder>' + 'xml' + '</folder>\n')
                xml.write('\t<filename>' + name_plus_suffix+'.jpg' + '</filename>\n')
                xml.write('\t<source>\n')
                xml.write('\t\t<database>The traffic_sign Database</database>\n')
                xml.write('\t\t<annotation>TT100K</annotation>\n')
                xml.write('\t\t<image>chenran</image>\n')
                xml.write('\t\t<flickrid>NULL</flickrid>\n')
                xml.write('\t</source>\n')
                xml.write('\t<owner>\n')
                xml.write('\t\t<flickrid>NULL</flickrid>\n')
                xml.write('\t\t<name>chenran</name>\n')
                xml.write('\t</owner>\n')
                xml.write('\t<size>\n')
                xml.write('\t\t<width>' + str(width) + '</width>\n')
                xml.write('\t\t<height>' + str(height) + '</height>\n')
                xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
                xml.write('\t</size>\n')
                xml.write('\t\t<segmented>0</segmented>\n')
                for j in range((len(line)-2)/5):
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>'  + str(line[5*j+5]) +'</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>0</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(line[5*j+1]) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(line[5*j+2]) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(line[5*j+3]) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(line[5*j+4]) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
                xml.write('</annotation>') 
fp2.close()
fp.close()
