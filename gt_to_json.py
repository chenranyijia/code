import os
import json
os.chdir('/home/chenran/Desktop/data/test')
gt = open('new_annotation_test.txt').readlines()
data = {}
for line in gt:
    im_info = line.strip().split(';')
    data[im_info[0]] = {}
    for i in range((len(im_info)-2)/5):
        data[im_info[0]][str(i)]={}
        data[im_info[0]][str(i)]['xmin']=im_info[5*i+1]
        data[im_info[0]][str(i)]['ymin'] = im_info[5 * i + 2]
        data[im_info[0]][str(i)]['xmax'] = im_info[5 * i + 3]
        data[im_info[0]][str(i)]['ymax'] = im_info[5 * i + 4]
        data[im_info[0]][str(i)]['category'] = im_info[5 * i + 5]
with open('groundtruth.json', 'w') as f:
    json.dump(data, f)
