import os
import cv2
import numpy as np

os.chdir('/home/chenran/Desktop/data-1024')
txt_file = open('train.txt').readlines()
split_txt_file = open('train_split.txt', 'w')

origin_img_path = 'train/'

split_path = 'train_split/'
if not os.path.exists(split_path):
    os.mkdir(split_path)

split_path_addition = 'train_split_addition/'
if not os.path.exists(split_path_addition):
    os.mkdir(split_path_addition)
'''
splits_path = 'trains_split'
if not os.path.exists(splits_path):
    os.mkdir(splits_path)
'''

#train_ids = open('train_ids.txt', 'w')
categorys = ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27',
             'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5',
             'pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']


for id in txt_file:
    im_info = id.strip().split(';')
    if not os.path.exists(origin_img_path+im_info[0]+'.jpg'):
        print 'not exists', im_info[0]
        continue
  #if im_info[0] not in {'36748', '92338'}:#:== '93072'  # == '18166'
    img = cv2.imread(origin_img_path+im_info[0]+'.jpg')
    H = img.shape[0]
    W = img.shape[1]
    for i in range(2):
        for j in range(2):
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
                    if ctr_y >= i * H / 2 and ctr_x >= j * W / 2 and ctr_y < (i + 1) * H / 2 and ctr_x < (j + 1) * W / 2:
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
                if x2_max-x1_min <= W/2 and y2_max-y1_min <= H/2:
                  if x1_min >= j*W/2 and y1_min >= i*H/2 and x2_max <= (j+1)*W/2 and y2_max <= (i+1)*H/2:
                    #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    #train_ids.write('\n')
                    new_img = img[i*(H/2):(i+1)*H/2, j*W/2:(j+1)*W/2,:]
                    cv2.imwrite(split_path + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                    split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    split_txt_file.write(';')
                    for m in range(len(_x1)):
                        split_txt_file.write(str(_x1[m] - j*W/2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y1[m] - i*H/2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_x2[m] - j*W/2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y2[m] - i*H/2))
                        split_txt_file.write(';')
                        split_txt_file.write(_category[m])
                        split_txt_file.write(';')
                    split_txt_file.write('\n')

                  elif x1_min < j*W/2 or y1_min < i*H/2:
                    coord_x = min(x1_min, j*W/2)
                    coord_y = min(y1_min, i*H/2)



                    if x2_max <= (j+1)*W/2 and y2_max <= (i+1)*H/2:

                      f=0
                      for g in range((len(im_info) - 2) / 5):
                          if im_info[g * 5 + 5] in categorys:
                              xg1 = int(im_info[g * 5 + 1])
                              yg1 = int(im_info[g * 5 + 2])
                              xg2 = int(im_info[g * 5 + 3])
                              yg2 = int(im_info[g * 5 + 4])
                              ctrg_x = (xg2 + xg1) / 2
                              ctrg_y = (yg2 + yg1) / 2
                              if ctrg_y >= coord_y and ctrg_x >= coord_x and ctrg_y < coord_y + H / 2 and coord_x + W / 2:
                                  f += 1
                      d = 0
                      for e in range(len(_x1)):
                          if _x1[e] >= coord_x and _x2[e] <= coord_x+W/2 and _y1[e] >= coord_y and _y2[e] <= coord_y+H/2:
                              d += 1

                      if f == d and f == len(_x1):
                        #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                        #train_ids.write('\n')
                        new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                        cv2.imwrite(split_path + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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
                          #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                          #train_ids.write('\n')
                          coord_y = i*H/2
                          coord_x = j*W/2
                          new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                          cv2.imwrite(split_path_addition + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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



                    elif x2_max > (j+1)*W/2:
                      coord_x = x2_max-W/2
                      coord_y = coord_y

                      f=0
                      for g in range((len(im_info) - 2) / 5):
                          if im_info[g * 5 + 5] in categorys:
                              xg1 = int(im_info[g * 5 + 1])
                              yg1 = int(im_info[g * 5 + 2])
                              xg2 = int(im_info[g * 5 + 3])
                              yg2 = int(im_info[g * 5 + 4])
                              ctrg_x = (xg2 + xg1) / 2
                              ctrg_y = (yg2 + yg1) / 2
                              if ctrg_y >= coord_y and ctrg_x >= coord_x and ctrg_y < coord_y + H / 2 and coord_x + W / 2:
                                  f += 1
                      d = 0
                      for e in range(len(_x1)):
                          if _x1[e] >= coord_x and _x2[e] <= coord_x+W/2 and _y1[e] >= coord_y and _y2[e] <= coord_y+H/2:
                              d += 1

                      if f==d and f == len(_x1):
                        #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                        #train_ids.write('\n')
                        new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                        cv2.imwrite(split_path + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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
                          #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                          #train_ids.write('\n')
                          coord_y = i*H/2
                          coord_x = j*W/2
                          new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                          cv2.imwrite(split_path_addition + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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


                    elif y2_max > (i+1)*H/2:
                      coord_x = coord_x
                      coord_y = y2_max - H/2

                      f=0
                      for g in range((len(im_info) - 2) / 5):
                          if im_info[g * 5 + 5] in categorys:
                              xg1 = int(im_info[g * 5 + 1])
                              yg1 = int(im_info[g * 5 + 2])
                              xg2 = int(im_info[g * 5 + 3])
                              yg2 = int(im_info[g * 5 + 4])
                              ctrg_x = (xg2 + xg1) / 2
                              ctrg_y = (yg2 + yg1) / 2
                              if ctrg_y >= coord_y and ctrg_x >= coord_x and ctrg_y < coord_y + H / 2 and coord_x + W / 2:
                                  f += 1
                      d = 0
                      for e in range(len(_x1)):
                          if _x1[e] >= coord_x and _x2[e] <= coord_x+W/2 and _y1[e] >= coord_y and _y2[e] <= coord_y+H/2:
                              d += 1

                      if f==d and f==len(_x1):
                        #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                        #train_ids.write('\n')
                        new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                        cv2.imwrite(split_path + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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
                          #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                          #train_ids.write('\n')
                          coord_y = i*H/2
                          coord_x = j*W/2
                          new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                          cv2.imwrite(split_path_addition + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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

                  elif x2_max > (j+1) * W / 2 or y2_max > (i+1) * H / 2:
                      coord_x = max(x2_max, (j+1) * W / 2)
                      coord_x -= W/2
                      coord_y = max(y2_max, (i+1) * H / 2)
                      coord_y -= H/2

                      if x1_min >= j * W / 2 and y1_min >= i * H / 2:

                          f = 0
                          for g in range((len(im_info) - 2) / 5):
                              if im_info[g * 5 + 5] in categorys:
                                  xg1 = int(im_info[g * 5 + 1])
                                  yg1 = int(im_info[g * 5 + 2])
                                  xg2 = int(im_info[g * 5 + 3])
                                  yg2 = int(im_info[g * 5 + 4])
                                  ctrg_x = (xg2 + xg1) / 2
                                  ctrg_y = (yg2 + yg1) / 2
                                  if ctrg_y >= coord_y and ctrg_x >= coord_x and ctrg_y < coord_y + H / 2 and coord_x + W / 2:
                                      f += 1
                          d = 0
                          for e in range(len(_x1)):
                              if _x1[e] >= coord_x and _x2[e] <= coord_x + W / 2 and _y1[e] >= coord_y and _y2[e] <= coord_y + H / 2:
                                  d += 1
                          if d==f and d == len(_x1):
                            #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                            #train_ids.write('\n')
                            new_img = img[coord_y:coord_y+H/2, coord_x:coord_x+W/2, :]
                            cv2.imwrite(split_path + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
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
                              #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                              #train_ids.write('\n')
                              coord_y = i * H / 2
                              coord_x = j * W / 2
                              new_img = img[coord_y:coord_y + H / 2, coord_x:coord_x + W / 2, :]
                              cv2.imwrite(split_path_addition + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),
                                          new_img)
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
                  else:
                      print 'error', im_info[0]
                else:
                    print 'afetrnoon', im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j)
                    #train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    #train_ids.write('\n')
                    new_img = img[i * (H / 2):(i + 1) * H / 2, j * W / 2:(j + 1) * W / 2, :]
                    cv2.imwrite(split_path_addition + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                    split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                    split_txt_file.write(';')
                    for m in range(len(_x1)):
                        split_txt_file.write(str(_x1[m] - j * W / 2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y1[m] - i * H / 2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_x2[m] - j * W / 2))
                        split_txt_file.write(';')
                        split_txt_file.write(str(_y2[m] - i * H / 2))
                        split_txt_file.write(';')
                        split_txt_file.write(_category[m])
                        split_txt_file.write(';')
                    split_txt_file.write('\n')


split_txt_file.close()
#train_ids.close()
