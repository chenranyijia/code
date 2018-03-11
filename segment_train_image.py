import os
import cv2
import numpy as np

os.chdir('/home/chenran/software/TT100K/data')
txt_file = open('annotation_train.txt').readlines()
split_txt_file = open('new_annotation_train.txt', 'w')

split_path = 'train_split'
if not os.path.exists(split_path):
    os.mkdir(split_path)
'''
splits_path = 'trains_split'
if not os.path.exists(splits_path):
    os.mkdir(splits_path)
'''

train_ids = open('train_ids.txt', 'w')
categorys = ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27',
             'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5',
             'pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']


for id in txt_file:
  im_info = id.strip().split(';')
  if not os.path.exists('train_TT100K/'+im_info[0]+'.jpg'):
      print 'not exists', im_info[0]
      continue
  if im_info[0] not in {'36748', '92338'}:#:== '93072'  # == '18166'
    img = cv2.imread('train_TT100K/'+im_info[0]+'.jpg')
    H = img.shape[0]
    W = img.shape[1]
    for i in range(4):
        for j in range(4):
            _x1 = []
            _y1 = []
            _x2 = []
            _y2 = []
            _category = []
            for k in range((len(im_info) - 2) / 5):
                if im_info[k * 5 + 5] in categorys:
                    x1 = int(im_info[k * 5 + 1])
                    y1 = int(im_info[k * 5 + 2])
                    x2 = int(im_info[k * 5 + 3])
                    y2 = int(im_info[k * 5 + 4])
                    ctr_x = (x2 + x1) / 2
                    ctr_y = (y2 + y1) / 2
                    if ctr_y >= i * H / 4 and ctr_x >= j * W / 4 and ctr_y < (i + 1) * H / 4 and ctr_x < (j + 1) * W / 4:
                        Flag = 1
                        _x1.append(x1)
                        _y1.append(y1)
                        _x2.append(x2)
                        _y2.append(y2)
                        _category.append(im_info[k*5+5])
            _x1 = np.array(_x1, dtype=np.int32)
            _y1 = np.array(_y1, dtype=np.int32)
            _x2 = np.array(_x2, dtype=np.int32)
            _y2 = np.array(_y2, dtype=np.int32)
            if len(_x1) > 0:
                x1_min = min(_x1)#min(min(_x1), j*W/4)
                y1_min = min(_y1)#min(min(_y1), i*H/4)
                x2_max = max(_x2)#max(max(_x2), (j+1)*W/4)
                y2_max = max(_y2)#max(max(_y2), (i+1)*H/4)
                if x2_max-x1_min <= W/4 and y2_max-y1_min <= H/4:
                  if x1_min >= j*W/4 and y1_min >= i*H/4 and x2_max <= (j+1)*W/4 and y2_max <= (i+1)*H/4:
                    train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    train_ids.write('\n')
                    new_img = img[i*(H/4):(i+1)*H/4, j*W/4:(j+1)*W/4,:]
                    cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                    split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    split_txt_file.write(';')
                    for m in range(len(_x1)):
                        split_txt_file.write(str(_x1[m] - j*W/4))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y1[m] - i*H/4))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_x2[m] - j*W/4))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y2[m] - i*H/4))
                        split_txt_file.write(';')
                        split_txt_file.write(_category[m])
                        split_txt_file.write(';')
                    split_txt_file.write('\n')

                  elif x1_min < j*W/4 or y1_min < i*H/4:
                    coord_x = min(x1_min, j*W/4)
                    coord_y = min(y1_min, i*H/4)
                    if x2_max <= (j+1)*W/4 and y2_max <= (i+1)*H/4:
                      train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      train_ids.write('\n')
                      new_img = img[coord_y:coord_y + H / 4, coord_x:coord_x + W / 4, :]
                      cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                      split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      split_txt_file.write(';')
                      for m in range(len(_x1)):
                        split_txt_file.write(str(_x1[m] - coord_x))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y1[m] - coord_y))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_x2[m] - coord_x))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y2[m] - coord_y))
                        split_txt_file.write(';')
                        split_txt_file.write(_category[m])
                        split_txt_file.write(';')
                      split_txt_file.write('\n')
                    elif x2_max > (j+1)*W/4:
                      coord_x = x2_max-W/4
                      coord_y = coord_y
                      train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      train_ids.write('\n')
                      new_img = img[coord_y:coord_y + H / 4, coord_x:coord_x + W / 4, :]
                      cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                      split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      split_txt_file.write(';')
                      for m in range(len(_x1)):
                        split_txt_file.write(str(_x1[m] - coord_x))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y1[m] - coord_y))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_x2[m] - coord_x))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y2[m] - coord_y))
                        split_txt_file.write(';')
                        split_txt_file.write(_category[m])
                        split_txt_file.write(';')
                      split_txt_file.write('\n')
                    elif y2_max > (i+1)*H/4:
                      coord_x = coord_x
                      coord_y = y2_max - H/4
                      train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      train_ids.write('\n')
                      new_img = img[coord_y:coord_y + H / 4, coord_x:coord_x + W / 4, :]
                      cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                      split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                      split_txt_file.write(';')
                      for m in range(len(_x1)):
                          split_txt_file.write(str(_x1[m] - coord_x))
                          split_txt_file.write(';')
                          split_txt_file.write(str(_y1[m] - coord_y))
                          split_txt_file.write(';')
                          split_txt_file.write(str(_x2[m] - coord_x))
                          split_txt_file.write(';')
                          split_txt_file.write(str(_y2[m] - coord_y))
                          split_txt_file.write(';')
                          split_txt_file.write(_category[m])
                          split_txt_file.write(';')
                      split_txt_file.write('\n')
                    else:
                      print 'error', im_info[0]

                  elif x2_max > (j+1) * W / 4 or y2_max > (i+1) * H / 4:
                      coord_x = max(x2_max, (j+1) * W / 4)
                      coord_y = max(y2_max, (i+1) * H / 4)
                      if x1_min >= j * W / 4 and y1_min >= i * H / 4:
                          train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                          train_ids.write('\n')
                          new_img = img[coord_y-H/4:coord_y, coord_x-W/4:coord_x, :]
                          cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                          split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                          split_txt_file.write(';')
                          for m in range(len(_x1)):
                              split_txt_file.write(str(_x1[m] - coord_x + W/4))
                              split_txt_file.write(';')
                              split_txt_file.write(str(_y1[m] - coord_y + H/4))
                              split_txt_file.write(';')
                              split_txt_file.write(str(_x2[m] - coord_x + W/4))
                              split_txt_file.write(';')
                              split_txt_file.write(str(_y2[m] - coord_y + H/4))
                              split_txt_file.write(';')
                              split_txt_file.write(_category[m])
                              split_txt_file.write(';')
                          split_txt_file.write('\n')
                      else:
                          print 'error', im_info[0]
                  else:
                      print 'error', im_info[0]
                else:
                  print 'afetrnoon', im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j)

  else:
      if im_info[0] == '36748':
          img = cv2.imread('train_TT100K/' + im_info[0] + '.jpg')
          H = img.shape[0]
          W = img.shape[1]
          _x1 = np.array([522, 750, 981, 1226])
          _y1 = np.array([658, 639, 626, 628])
          _x2 = np.array([589, 823, 1060, 1300])
          _y2 = np.array([725, 709, 697, 700])

          axis_x1 = np.array([450, 450, 900, 900])
          axis_y1 = np.array([500, 500, 400, 400])
          axis_x2 = np.array([962, 962, 1412, 1412])
          axis_y2 = np.array([1012, 1012, 912, 912])
          _category = ['pl120','pl100', 'pl100', 'pl80']
          i = 1
          num = np.array([1,1,2,2])
          for m in range(len(_x1)):
              if m % 2 == 0:
                  train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, num[m]))
                  train_ids.write('\n')
                  split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, num[m]))
                  split_txt_file.write(';')
                  new_img = img[axis_y1[m]:axis_y2[m], axis_x1[m]:axis_x2[m], :]
                  cv2.imwrite('train_split/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, num[m]), new_img)
              split_txt_file.write(str(_x1[m]-axis_x1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(_y1[m]-axis_y1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(_x2[m]-axis_x1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(_y2[m]-axis_y1[m]))
              split_txt_file.write(';')
              split_txt_file.write(_category[m])
              split_txt_file.write(';')
              if m % 2 == 1:
                  split_txt_file.write('\n')



      elif im_info[0] == '92338':
          img = cv2.imread('train_TT100K/' + im_info[0] + '.jpg')
          H = img.shape[0]
          W = img.shape[1]
          _x1 = np.array([308,788,1310])
          _y1 = np.array([300,300,300])
          _x2 = np.array([820,1300,1822])
          _y2 = np.array([812,812,812])

          axis_x1 = np.array([511, 918, 1356])
          axis_y1 = np.array([415, 376, 394])
          axis_x2 = np.array([631, 1055, 1481])
          axis_y2 = np.array([524, 492, 503])
          _category = ['pl120','pl100','pl80']
          i = 1
          num = np.array([1,2,3])
          for m in range(len(_x1)):
              train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, num[m]))
              train_ids.write('\n')
              split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, num[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(axis_x1[m] - _x1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(axis_y1[m] - _y1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(axis_x2[m] - _x1[m]))
              split_txt_file.write(';')
              split_txt_file.write(str(axis_y2[m] - _y1[m]))
              split_txt_file.write(';')
              split_txt_file.write(_category[m])
              split_txt_file.write(';')
              new_img = img[_y1[m]:_y2[m], _x1[m]:_x2[m],:]
              cv2.imwrite('train_split/'+im_info[0]+'_{:02d}_{:02d}.jpg'.format(i,num[m]), new_img)
      else:
          print 'error1', im_info[0]

split_txt_file.close()
train_ids.close()
