
from __future__ import absolute_import, print_function

import os.path as osp
from glob import glob

import cv2
import numpy as np
import scipy.io as sio
import torch
from PIL import Image
from torch.utils import data

from .base import _BaseDataset

class COCO(_BaseDataset):
    """COCO ground truth dataset"""

    def __init__(self, year=2014, **kwargs):
        self.year = year
        super(COCO, self).__init__(**kwargs)

    def _set_files(self):
        self.root = osp.join(self.root, "coco{}".format(self.year))
        # Create data list by parsing the "images" folder
        if self.split in ["train2014", "val2014"]:
            file_list = osp.join(self.root, "ImageSets", self.split + ".txt")
            file_list = tuple(open(file_list, "r"))
            file_list = [id_.strip() for id_ in file_list]
            self.files = file_list
        else:
            raise ValueError("Invalid split name: {}".format(self.split))

    def _load_data(self, index):
        # Set paths
        image_id = self.files[index]
        image_path = osp.join(self.root, "JPEGImages", self.split, "COCO_{}_".format(self.split) + image_id + ".jpg")
        label_path = osp.join(self.root, "gt_mask", self.split, image_id + ".png")

        # Load an image and label
        image = cv2.imread(image_path, cv2.IMREAD_COLOR).astype(np.float32)
        label = np.asarray(Image.open(label_path), dtype=np.int32)
        return image_id, image, label

class pseudoCOCO(_BaseDataset):
    """COCO pseudo ground truth dataset"""

    def __init__(self, year=2014, **kwargs):
        self.year = year
        super(pseudoCOCO, self).__init__(**kwargs)

    def _set_files(self):
        self.root = osp.join(self.root, "coco{}".format(self.year))
        # Create data list by parsing the "images" folder
        if self.split in ["train2014", "val2014"]:
            file_list = osp.join(self.root, "ImageSets", self.split + ".txt")
            file_list = tuple(open(file_list, "r"))
            file_list = [id_.strip() for id_ in file_list]
            self.files = file_list
        else:
            raise ValueError("Invalid split name: {}".format(self.split))

    def _load_data(self, index):
        # Set paths
        image_id = self.files[index]
        image_path = osp.join(self.root, "JPEGImages", self.split, "COCO_{}_".format(self.split) + image_id + ".jpg")
        label_path = osp.join(self.root, "pseudo_mask", self.split, image_id + ".png")

        # Load an image and label
        image = cv2.imread(image_path, cv2.IMREAD_COLOR).astype(np.float32)
        label = np.asarray(Image.open(label_path), dtype=np.int32)
        return image_id, image, label