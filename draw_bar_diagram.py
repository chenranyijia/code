import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(1)
ax1 = plt.subplot(111)

data = np.array([1887,1379,1045,969,874,735,660,580,579,526,515,476,449,374,338,297,269,263,258,244,208,197,190,163,136,122,122,111,109,107,106,104,103,98,98,92,90,87,84,83,75,73,73,70,69,59,44,42,41,40,37,36,35,31,31,29,28,28,26,26,21,19,19,18,17,16,15,15,14,13,13,12,12,11,11,11,11,11,10,10,9,9,9,9,8,7,7,6,6,6,6,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
width = 0.5
data = data[:40]
x_bar = np.arange(len(data))

rect = ax1.bar(left=x_bar, height=data, width=width, color='lightblue')
for rec in rect:
    x = rec.get_x()
    height = rec.get_height()
    ax1.text(x+0.1, 1.02*height, str(height))

labels = ['pn','pne','i5','p11','pl40','po','pl50','io','pl80','pl60','p26','i4','pl100','pl30','il60','i2','pl5','w57','p5','p10','pl120','il80','ip','p23','pr40','ph4.5','w59','p3','w55','pm20','p12','pg','pl70','pm55','pl20','il100','w13','p19','p27','ph4','pm30','wo','ph5','w32','p6','il90','pa14','pl90','pb','p9','w30','p25','w58','w63','pl15','p1','il50','p18','pl110','p22','i10','p17','il110','p14','w22','ps','ph4.2']
labels = labels[:40]
ax1.set_xticks(x_bar)
ax1.set_xticklabels(labels)
plt.show()





'''
# engines = ['-Deconv', 'Our Proposal']
plt.style.use('ggplot')
logistic_regression = [
    [1, 4, 10, 19, 10, 10, 31, 9, 22, 1, 7, 4, 6, 4, 0, 1, 1, 23, 29, 0, 1, 8, 2, 5, 8, 8, 29, 17, 2, 0, 27, 5, 0, 1, 1,
     0, 1, 0, 8, 1, 6, 13, 0],
    [1, 2, 8, 15, 9, 8, 27, 8, 16, 1, 7, 4, 6, 4, 0, 1, 0, 19, 24, 0, 1, 5, 2, 5, 6, 5, 22, 16, 2, 0, 23, 4, 0, 1, 0, 0,
     1, 0, 7, 1, 5, 11, 0]]

engines = ['-Deconv', 'Our Proposal']
colors = 'gb'

fig, ax1 = plt.subplots(ncols=1)
idx = np.arange(len(logistic_regression[0]))
n = len(logistic_regression)
width = 1.0 / (n + 1)
for i in range(n):
    ax1.bar(idx + i * width, logistic_regression[i], width, color=colors[i], alpha=0.8)
    xpos = idx + (i + 0.5) * width
    ypos = logistic_regression[i]
ax1.legend(engines)
ax1.set_xlabel('classes')
ax1.set_ylabel('Number')
ax1.set_title('The distribution of false classified samples')
plt.show()
'''

