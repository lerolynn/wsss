
import numpy as np
import os
from chainercv.datasets import VOCSemanticSegmentationDataset
from chainercv.evaluations import calc_semantic_segmentation_confusion
import imageio
from PIL import Image

def run(args):
    preds = []
    if args.voc:
        dataset = VOCSemanticSegmentationDataset(split=args.chainer_eval_set, data_dir=args.voc12_root)
        labels = [dataset.get_example_by_keys(i, (1,))[0] for i in range(len(dataset))]
        for id in dataset.ids:
            cls_labels = imageio.imread(os.path.join(args.sem_seg_out_dir, id + '.png')).astype(np.uint8)
            cls_labels[cls_labels == 255] = 0
            preds.append(cls_labels.copy())

    else:
        ids = open('coco14/train2014_semseg.txt').readlines()
        ids = [i.split('\n')[0] for i in ids]
        labels = []
        n_img = 0

        for i, id in enumerate(ids):
            label = np.array(Image.open('../data/coco2014/mask/train2014/%s.png' % id))
            cls_labels = imageio.imread(os.path.join(args.sem_seg_out_dir, id + '.png')).astype(np.uint8)
            cls_labels[cls_labels == 255] = 0
            preds.append(cls_labels.copy())
            labels.append(label)
            n_img += 1   

    confusion = calc_semantic_segmentation_confusion(preds, labels)[:21, :21]

    gtj = confusion.sum(axis=1)
    resj = confusion.sum(axis=0)
    gtjresj = np.diag(confusion)
    denominator = gtj + resj - gtjresj
    fp = 1. - gtj / denominator
    fn = 1. - resj / denominator
    iou = gtjresj / denominator
    
    print("total images", n_img)
    print(fp[0], fn[0])
    print(np.mean(fp[1:]), np.mean(fn[1:]))

    print({'iou': iou, 'miou': np.nanmean(iou)})
    print()
