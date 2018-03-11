import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os, sys, cv2
import argparse
import os.path as osp
import glob

this_dir = osp.dirname(__file__)
sys.path.insert(0, this_dir+'/..')

from lib.networks.factory import get_network
from lib.fast_rcnn.config import cfg
from lib.fast_rcnn.test import im_detect
from lib.fast_rcnn.nms_wrapper import nms
from lib.utils.timer import Timer

CLASSES = ('__background__', 'i5', 'pl30', 'pl50', 'pl60', 'pl80', 'pl100', 'pl120')


# CLASSES = ('__background__','person','bike','motorbike','car','bus')

def vis_detections(im, class_name, dets, ax, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
        )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                 fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im = cv2.imread(image_name)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')

    CONF_THRESH = 0.2
    NMS_THRESH = 0.2

    cls_name = dict(zip(np.arange(len(CLASSES)),CLASSES))
    cls_matrix = np.arange(len(CLASSES)).reshape([1,-1])+np.zeros([boxes.shape[0],1])
    cls_scores_fg = scores[:, 1:len(CLASSES)]
    cls_boxes_fg = boxes[:, 4:4*(len(CLASSES))]
    cls_matrix_fg = cls_matrix[:, 1:len(CLASSES)]

    cls_scores_fg = cls_scores_fg.reshape([-1,1])
    cls_boxes_fg = cls_boxes_fg.reshape([-1,4])
    cls_matrix_fg = cls_matrix_fg .reshape([-1,1])

    keeps = np.where(cls_scores_fg>=CONF_THRESH)[0]

    cls_scores_fg = cls_scores_fg[keeps]
    cls_boxes_fg = cls_boxes_fg[keeps]
    cls_matrix_fg = cls_matrix_fg[keeps]


    dets = np.hstack((cls_boxes_fg, cls_scores_fg)).astype(np.float32)
    keep = nms(dets, NMS_THRESH)
    print len(keep)
    dets = dets[keep, :]
    cls_matrix_fg = cls_matrix_fg[keep,:]
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1
        cls_fg_ind = np.where(cls_matrix_fg==cls_ind)[0]
        detses = dets[cls_fg_ind, :]
        vis_detections(im, cls, detses, ax, thresh=CONF_THRESH)

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        default='VGGnet_test')
    parser.add_argument('--model', dest='model', help='Model path',
                        default='/home/chenran/Desktop/master/DETRCNN/output_180k/exp_dir/voc_2007_trainval/VGGnet_fast_rcnn_iter_160000.ckpt')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    '''
    if args.model == ' ' or not os.path.exists(args.model):
        print ('current path is ' + os.path.abspath(__file__))
        raise IOError(('Error: Model not found.\n'))
    '''
    # init session
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = get_network(args.demo_net)
    # load model
    print ('Loading network {:s}... '.format(args.demo_net)),
    saver = tf.train.Saver()
    saver.restore(sess, args.model)
    print (' done.')

    # Warmup on a dummy image
    '''
    im = 128 * np.ones((300, 300, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _ = im_detect(sess, net, im)
    '''
    im_names = glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.png')) + \
               glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.jpg'))

    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Demo for {:s}'.format(im_name)
        demo(sess, net, im_name)

plt.show()
