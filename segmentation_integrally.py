import os
import cv2
import numpy as np

os.chdir('/home/chenran/Desktop/data/data_without_argument/train')
txt_file = open('annotation_train.txt').readlines()
split_txt_file = open('train_split/annotation_train_split.txt', 'w')

split_path = 'train_split/train_split_img'
if not os.path.exists(split_path):
    os.mkdir(split_path)

error_path = 'train_split/error_img'
if not os.path.exists(error_path):
    os.mkdir(error_path)
#split_path_addition = 'train_split_addition/'
#if not os.path.exists(split_path_addition):
#    os.mkdir(split_path_addition)
'''
splits_path = 'trains_split'
if not os.path.exists(splits_path):
    os.mkdir(splits_path)
'''

train_ids = open('train_split/train_ids.txt', 'w')
categorys = ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12', 'p19', 'p23', 'p26', 'p27',
             'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5', 'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl50','pl60', 'pl5',
             'pl70', 'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32', 'w55', 'w57', 'w59', 'wo']


def calculate_overlap(grid, bounding):
    x1 = max(grid[0], bounding[0])
    y1 = max(grid[1], bounding[1])
    x2 = min(grid[2], bounding[2])
    y2 = min(grid[3], bounding[3])
    overlap = max(0, x2-x1)*max(0,y2-y1)
    return overlap

for id in txt_file:
    im_info = id.strip().split(';')
    if not os.path.exists('train_img/'+im_info[0]+'.jpg'):
        print 'not exists', im_info[0]
        continue
  #if im_info[0] not in {'36748', '92338'}:#:== '93072'  # == '18166'
    img = cv2.imread('train_img/'+im_info[0]+'.jpg')
    H = img.shape[0]
    W = img.shape[1]

    #calculate the coordinate of bounding boxes
    _x1 = []
    _y1 = []
    _x2 = []
    _y2 = []
    _category = []
    _ctr_x = []
    _ctr_y = []
    for k in range((len(im_info) - 2) / 5):
        if im_info[k * 5 + 5] in categorys:
            x1 = int(im_info[k * 5 + 1])
            y1 = int(im_info[k * 5 + 2])
            x2 = int(im_info[k * 5 + 3])
            y2 = int(im_info[k * 5 + 4])
            ctr_x = (x2 + x1) / 2
            ctr_y = (y2 + y1) / 2
#            if ctr_y >= i * H / 4 and ctr_x >= j * W / 4 and ctr_y < (i + 1) * H / 4 and ctr_x < (j + 1) * W / 4:
#                Flag = 1
            _x1.append(x1)
            _y1.append(y1)
            _x2.append(x2)
            _y2.append(y2)
            _ctr_x.append(ctr_x)
            _ctr_y.append(ctr_y)
            _category.append(im_info[k * 5 + 5])
    _x1 = np.array(_x1, dtype=np.int32)
    _y1 = np.array(_y1, dtype=np.int32)
    _x2 = np.array(_x2, dtype=np.int32)
    _y2 = np.array(_y2, dtype=np.int32)
    _ctr_x = np.array(_ctr_x, dtype=np.int32)
    _ctr_y = np.array(_ctr_y, dtype=np.int32)

    if len(_x1) > 0:
        for i in range(4):
            for j in range(4):
                #obtain the bounding boxes in the grid
                inside_x1 = []
                inside_y1 = []
                inside_x2 = []
                inside_y2 = []
                inside_category = []
                outside_x1=[]
                outside_y1=[]
                outside_x2=[]
                outside_y2=[]
                for k in range(len(_x1)):
                    if _ctr_y[k] >= i * H / 4 and _ctr_x[k] >= j * W / 4 and _ctr_y[k] < (i + 1) * H / 4 and _ctr_x[k] < (j + 1) * W / 4:
                        inside_x1.append(_x1[k])
                        inside_x2.append(_x2[k])
                        inside_y1.append(_y1[k])
                        inside_y2.append(_y2[k])
                        inside_category.append(_category[k])
                    else:
                        outside_x1.append(_x1[k])
                        outside_x2.append(_x2[k])
                        outside_y1.append(_y1[k])
                        outside_y2.append(_y2[k])
                if len(inside_x1) > 0:
                    inside_x1 = np.array(inside_x1)
                    inside_y1 = np.array(inside_y1)
                    inside_x2 = np.array(inside_x2)
                    inside_y2 = np.array(inside_y2)

                    x1_min = min(inside_x1)#min(min(_x1), j*W/4)
                    y1_min = min(inside_y1)#min(min(_y1), i*H/4)
                    x2_max = max(inside_x2)#max(max(_x2), (j+1)*W/4)
                    y2_max = max(inside_y2)#max(max(_y2), (i+1)*H/4)
                    if x2_max-x1_min <= W/4 and y2_max-y1_min <= H/4:
                        if x1_min >= j*W/4 and y1_min >= i*H/4 and x2_max <= (j+1)*W/4 and y2_max <= (i+1)*H/4:
                            flag = True
                            for m in range(len(outside_x1)):
                                overlap = calculate_overlap([j*W/4,i*H/4,(j+1)*W/4,(i+1)*H/4],[outside_x1[m],outside_y1[m],outside_x2[m],outside_y2[m]])
                                if overlap > 0:
                                    flag = False
                                    break
                            if flag:
                                train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                train_ids.write('\n')
                                new_img = img[i*(H/4):(i+1)*H/4, j*W/4:(j+1)*W/4,:]
                                cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                                split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                split_txt_file.write(';')
                                for m in range(len(inside_x1)):
                                    split_txt_file.write(str(inside_x1[m] - j*W/4))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_y1[m] - i*H/4))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_x2[m] - j*W/4))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_y2[m] - i*H/4))
                                    split_txt_file.write(';')
                                    split_txt_file.write(inside_category[m])
                                    split_txt_file.write(';')
                                split_txt_file.write('\n')
                            else:
                                flag = True
                        # calculate the max grid by regression
                                origin_x1 = 0
                                origin_y1 = 0
                                origin_x2 = W-1
                                origin_y2 = H-1
                                for m in range(len(outside_x1)):
                                    overlap = calculate_overlap([x1_min,y1_min,x2_max,y2_max],[outside_x1[m],outside_y1[m],outside_x2[m],outside_y2[m]])
                                    outside_area = (outside_x2[m] - outside_x1[m]) * (outside_y2[m] - outside_y1[m])
                                    if float(overlap)/float(outside_area) > 0.1:
                                        print 'can not segmentation in (H/4, W/4)', im_info[0] + '_{:02d}_{:02d}'.format(i, j)
                                        error_img = img[origin_y1:origin_y2,origin_x1:origin_x2,:]
                                        cv2.imwrite(error_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), error_img)
                                        flag = False
                                        break
                                    else:
                                        if float(overlap) / float(outside_area) > 0:
                                            if outside_x1[m] < x1_min and x1_min < outside_x2[m] < x2_max:
                                                origin_x1 = x1_min
                                            elif x1_min < outside_x1[m] < x2_max and outside_x2[m] > x2_max:
                                                origin_x2 = x2_max
                                            elif outside_y1[m] < y1_min and y1_min < outside_y2[m] < y2_max:
                                                origin_y1 = y1_min
                                            elif outside_y2[m] > y2_max and y1_min < outside_y1[m] < y2_max:
                                                origin_y2 = y2_max
                                            else:
                                                print 'error', im_info[0]

                                        else:
                                            overlap = calculate_overlap([origin_x1,origin_y1,origin_x2,origin_y2],[outside_x1[m],outside_y1[m],outside_x2[m],outside_y2[m]])
                                            if overlap > 0:
                                                if outside_x2[m] < x1_min:
                                                    origin_x1 = outside_x2[m]
                                                if outside_x1[m] > x2_max:
                                                    origin_x2 = outside_x1[m]
                                                if outside_y2[m] < y1_min:
                                                    origin_y1 = outside_y2[m]
                                                if outside_y1[m] > y2_max:
                                                    origin_y2 = outside_y1[m]
                                if flag:
                                  if origin_x2-origin_x1 >= W/4 and origin_y2-origin_y1 >= H/4:
                                    start_x = np.random.randint(max(origin_x1, max(0,x2_max-W/4)), min(x1_min,max(0,origin_x2-W/4))+1)
                                    start_y = np.random.randint(max(origin_y1, max(0,y2_max-W/4)), min(y1_min,max(0,origin_y2-W/4)+1))
                                    train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                    train_ids.write('\n')
                                    new_img = img[start_y:start_y+H/4, start_x:start_x+W/4,:]
                                    cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                                    split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                    split_txt_file.write(';')
                                    for m in range(len(inside_x1)):
                                        split_txt_file.write(str(inside_x1[m] - start_x))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(inside_y1[m] - start_y))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(inside_x2[m] - start_x))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(inside_y2[m] - start_y))
                                        split_txt_file.write(';')
                                        split_txt_file.write(inside_category[m])
                                        split_txt_file.write(';')
                                    split_txt_file.write('\n')

                                  else:
                                    bounding = min(origin_x2-origin_x1, origin_y2-origin_y1)
                                    if bounding < (x2_max-x1_min) or bounding < (y2_max-y1_min):
                                        print 'can not extract in isometry', im_info[0]
                                        error_img = img[origin_y1:origin_y2, origin_x1:origin_x2, :]
                                        cv2.imwrite(error_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), error_img)
                                    else:
                                        #bounding = min(origin_x2 - origin_x1, origin_y2 - origin_y1)
                                        if origin_x2-origin_x1 < origin_y2-origin_y1:
                                            start_x = origin_x1
                                            start_y = np.random.randint(max(origin_y1, max(0,y2_max - bounding)),min(y1_min, max(0,origin_y2 -bounding ))+ 1)
                                        else:
                                            start_y = origin_y1
                                            start_x = np.random.randint(max(origin_x1, max(0,x2_max - bounding)),min(x1_min, max(0,origin_x2 -bounding ))+ 1)
                                        scale = float(H / 4) / bounding
                                        new_img = img[start_y:start_y + bounding, start_x:start_x + bounding, :]
                                        new_img = cv2.resize(new_img, (W / 4, H / 4), interpolation=cv2.INTER_CUBIC)
                                        cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),new_img)
                                        train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                        train_ids.write('\n')
                                        split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                        split_txt_file.write(';')
                                        for m in range(len(inside_x1)):
                                            split_txt_file.write(str(int(scale*(inside_x1[m] - start_x))))
                                            split_txt_file.write(';')
                                            split_txt_file.write(str(int(scale*(inside_y1[m] - start_y))))
                                            split_txt_file.write(';')
                                            split_txt_file.write(str(int(scale*(inside_x2[m] - start_x))))
                                            split_txt_file.write(';')
                                            split_txt_file.write(str(int(scale*(inside_y2[m] - start_y))))
                                            split_txt_file.write(';')
                                            split_txt_file.write(inside_category[m])
                                            split_txt_file.write(';')
                                        split_txt_file.write('\n')
                                        
                        #some signs outside (i*H/4:(i+1)*H/4, j*W/4:(j+1)*W/4)
                        else:
                            flag = True
                            origin_x1 = 0
                            origin_y1 = 0
                            origin_x2 = W - 1
                            origin_y2 = H - 1
                            for m in range(len(outside_x1)):
                                overlap = calculate_overlap([x1_min, y1_min, x2_max, y2_max],[outside_x1[m], outside_y1[m], outside_x2[m],outside_y2[m]])
                                outside_area = (outside_x2[m] - outside_x1[m]) * (outside_y2[m] - outside_y1[m])
                                if float(overlap)/float(outside_area) > 0.1:
                                    print float(overlap)/float(outside_area)
                                    print 'can not segmentation in biases', im_info[0] + '_{:02d}_{:02d}'.format(i, j)
                                    error_img = img[origin_y1:origin_y2,origin_x1:origin_x2,:]
                                    cv2.imwrite(error_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), error_img)
                                    flag = False
                                    break
                                else:
                                    if float(overlap) / float(outside_area) > 0:
                                        if outside_x1[m] < x1_min and x1_min < outside_x2[m] < x2_max:
                                            origin_x1 = x1_min
                                        elif x1_min < outside_x1[m] < x2_max and outside_x2[m] > x2_max:
                                            origin_x2 = x2_max
                                        elif outside_y1[m] < y1_min and y1_min < outside_y2[m] < y2_max:
                                            origin_y1 = y1_min
                                        elif outside_y2[m] > y2_max and y1_min < outside_y1[m] < y2_max:
                                            origin_y2 = y2_max
                                        else:
                                            print 'error', im_info[0]
                                    else:
                                        overlap = calculate_overlap([origin_x1, origin_y1, origin_x2, origin_y2],[outside_x1[m], outside_y1[m], outside_x2[m], outside_y2[m]])
                                        if overlap > 0:
                                            if outside_x2[m] < x1_min:
                                                origin_x1 = outside_x2[m]
                                            if outside_x1[m] > x2_max:
                                                origin_x2 = outside_x1[m]
                                            if outside_y2[m] < y1_min:
                                                origin_y1 = outside_y2[m]
                                            if outside_y1[m] > y2_max:
                                                origin_y2 = outside_y1[m]
                            if flag:
                              if origin_x2 - origin_x1 >= W / 4 and origin_y2 - origin_y1 >= H / 4:
                                start_x = np.random.randint(max(origin_x1, max(0,x2_max - W / 4)),
                                                                min(x1_min, max(0, origin_x2 - W / 4)) + 1)
                                start_y = np.random.randint(max(origin_y1, max(0,y2_max - W / 4)),
                                                                min(y1_min, max(0,origin_y2 - W / 4)) + 1)
                                train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                train_ids.write('\n')
                                new_img = img[start_y:start_y + H / 4, start_x:start_x + W / 4, :]
                                cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),
                                                new_img)
                                split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                split_txt_file.write(';')
                                for m in range(len(inside_x1)):
                                    split_txt_file.write(str(inside_x1[m] - start_x))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_y1[m] - start_y))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_x2[m] - start_x))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(inside_y2[m] - start_y))
                                    split_txt_file.write(';')
                                    split_txt_file.write(inside_category[m])
                                    split_txt_file.write(';')
                                split_txt_file.write('\n')

                              else:
                                bounding = min(origin_x2-origin_x1, origin_y2-origin_y1)
                                if bounding < (x2_max-x1_min) or bounding < (y2_max-y1_min):
                                    print 'can not extracted in isometry', im_info[0]
                                    error_img = img[origin_y1:origin_y2, origin_x1:origin_x2, :]
                                    cv2.imwrite(error_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),error_img)

                                else:
                                    if origin_x2-origin_x1 < origin_y2-origin_y1:
                                        start_x = origin_x1
                                        start_y = np.random.randint(max(origin_y1, max(0,y2_max - bounding)),min(y1_min, max(0,origin_y2 -bounding ))+ 1)
                                    else:
                                        start_y = origin_y1
                                        start_x = np.random.randint(max(origin_x1, max(0,x2_max - bounding)),min(x1_min, max(0,origin_x2 -bounding ))+ 1)
                                    scale = float(H / 4) / bounding
                                    new_img = img[start_y:start_y + bounding, start_x:start_x + bounding, :]
                                    new_img = cv2.resize(new_img, (W / 4, H / 4), interpolation=cv2.INTER_CUBIC)
                                    cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),new_img)
                                    train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                    train_ids.write('\n')
                                    split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                    split_txt_file.write(';')
                                    for m in range(len(inside_x1)):
                                        split_txt_file.write(str(int(scale*(inside_x1[m] - start_x))))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(int(scale*(inside_y1[m] - start_y))))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(int(scale*(inside_x2[m] - start_x))))
                                        split_txt_file.write(';')
                                        split_txt_file.write(str(int(scale*(inside_y2[m] - start_y))))
                                        split_txt_file.write(';')
                                        split_txt_file.write(inside_category[m])
                                        split_txt_file.write(';')
                                    split_txt_file.write('\n')
                    else:
                        origin_x1 = 0
                        origin_y1 = 0
                        origin_x2 = W - 1
                        origin_y2 = H - 1
                        flag = True
                        for m in range(len(outside_x1)):
                            overlap = calculate_overlap([x1_min, y1_min, x2_max, y2_max],
                                                        [outside_x1[m], outside_y1[m], outside_x2[m],
                                                         outside_y2[m]])
                            outside_area = (outside_x2[m] - outside_x1[m]) * (outside_y2[m] - outside_y1[m])
                            if float(overlap)/float(outside_area) > 0.1:
                                flag = False
                                print 'can not segmentation out', im_info[0] + '_{:02d}_{:02d}'.format(i, j)
                                error_img = img[j*H/4:(j+1)*H/4, i*W/4:(i+1)*W/4, :]
                                cv2.imwrite(error_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j),error_img)
                                break
                            else:
                                if float(overlap) / float(outside_area) > 0:
                                    if outside_x1[m] < x1_min and x1_min < outside_x2[m] < x2_max:
                                        origin_x1 = x1_min
                                    elif x1_min < outside_x1[m] < x2_max and outside_x2[m] > x2_max:
                                        origin_x2 = x2_max
                                    elif outside_y1[m] < y1_min and y1_min < outside_y2[m] < y2_max:
                                        origin_y1 = y1_min
                                    elif outside_y2[m] > y2_max and y1_min < outside_y1[m] < y2_max:
                                        origin_y2 = y2_max
                                    else:
                                        print 'error', im_info[0]
                                else:
                                    overlap = calculate_overlap([origin_x1, origin_y1, origin_x2, origin_y2],
                                                            [outside_x1[m], outside_y1[m], outside_x2[m],
                                                             outside_y2[m]])
                                    if overlap > 0:
                                        if outside_x2[m] < x1_min:
                                            origin_x1 = outside_x2[m]
                                        if outside_x1[m] > x2_max:
                                            origin_x2 = outside_x1[m]
                                        if outside_y2[m] < y1_min:
                                            origin_y1 = outside_y2[m]
                                        if outside_y1[m] > y2_max:
                                            origin_y2 = outside_y1[m]
                        if flag:
                            if min(origin_x2-origin_x1, origin_y2-origin_y1) < max(x2_max-x1_min,y2_max-y1_min):
                                print 'large, can not segmentation in isometry'
                                error_img = img[origin_y1:origin_y2, origin_x1:origin_x2,:]
                                cv2.imwrite(error_path+'/'+im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), error_img)
                            else:
                                bounding = max(x2_max-x1_min,y2_max-y1_min)
                                if x2_max-x1_min > y2_max-y1_min:
                                    start_x = x1_min
                                    start_y = np.random.randint(max(origin_y1, max(0, y2_max-bounding)), min(y1_min, max(0,origin_y2-bounding))+1)
                                else:
                                    start_y = y1_min
                                    start_x = np.random.randint(max(origin_x1, max(0,x2_max-bounding)), min(x1_min, max(0,origin_x2-bounding))+1)
                                scale = float(H/4)/bounding
                                new_img = img[start_y:start_y + bounding, start_x:start_x + bounding, :]
                                new_img = cv2.resize(new_img, (W / 4, H / 4), interpolation=cv2.INTER_CUBIC)
                                cv2.imwrite(split_path + '/' + im_info[0] + '_{:02d}_{:02d}.jpg'.format(i, j), new_img)
                                train_ids.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                train_ids.write('\n')
                                split_txt_file.write(im_info[0] + '_{:02d}_{:02d}'.format(i, j))
                                split_txt_file.write(';')
                                for m in range(len(inside_x1)):
                                    split_txt_file.write(str(int(scale * (inside_x1[m] - start_x))))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(int(scale * (inside_y1[m] - start_y))))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(int(scale * (inside_x2[m] - start_x))))
                                    split_txt_file.write(';')
                                    split_txt_file.write(str(int(scale * (inside_y2[m] - start_y))))
                                    split_txt_file.write(';')
                                    split_txt_file.write(inside_category[m])
                                    split_txt_file.write(';')
                                split_txt_file.write('\n')
