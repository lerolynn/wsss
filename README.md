# Weakly Supervised Semantic Segmentation

This repository runs the full Weakly Supervised Semantic Segmentaiton pipeline following the method of [IRNet](https://github.com/jiwoon-ahn/irn)

## Installation

This repository is tested on Ubuntu 18.04, using Python 3.7 and Pytorch >= 1.11 Other environment variables are as specified in the `environment.yml` file.

_Note: Pytorch environment should be suitable to your CUDA version. This repository was tested on Pytorch versions 1.11.0 and 1.12.0 for the Nvidia RTX 2080Ti and 3090 GPUs respectively._

---

### Quick Setup

To setup the environment variables and install the required datasets, run `setup.sh` in the root directory of the repository.

```console
.source setup.sh
```

The setup script is configured to set up the Anaconda environment, download the PASCAL VOC2012, the MS COCO2014 datasets and the pretrained segmentation weights and to 

---

#### Setup Steps:

1. Install and setup the Conda environment `wsss`
2. The datasets are downloaded and moved to the folders as specified in the directory hierarchy [here](./data/README.md). (Pseudo masks will be generated by subsequent steps) More information on the datasets is located in the [README](./data/README.md) of the data folder.

   * Pascal VOC2012 is downloaded from the official [Pascal VOC website](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/#devkit)
   * MS COCO dataset is downloaded from the offical [COCO website](https://cocodataset.org/#download)

3. While VOC provides segmentation masks as images, COCO ground truth segmentation masks have to be converted from the annotation files by running:

```
python utils/coco_ann_to_mask.py
```
4. Download weights used for the segmentation model. Weights are pretrained on the ImageNet dataset for fair comparison, and are provided by the authors of [RIB](https://github.com/jbeomlee93/RIB).

---

## Usage

Pseudo ground truth segmentation labels following the [IRN](https://github.com/jiwoon-ahn/irn) method is first generated and copied to the `pseudo_mask` folders of the respective VOC and COCO datasets.

DeepLab-v2 is used to perform Semantic Segmentation, with ground-truth labels used in training replaced by the pseudo-labels generated by IRN.

### IRN



#### VOC2012 dataset

To obtain pseudo-labels for the VOC2012 dataset, in the `pseudo_mask` directory, run:

```python
# Run IRN
python run_sample.py

# Move pseudo-labels to the VOC2012 data directory
mv result/voc12/sem_seg ../data/VOC2012/pseudo_mask
```

#### COCO2014 dataset

To obtain pseudo-labels for the COCO2014 dataset, in the `pseudo_mask` directory, run:

```python
# Run IRN for the COCO datset
python run_sample_coco.py

# Move pseudo-labels to the coco2014 data directory
mv result/coco14/sem_seg ../data/coco2014/pseudo_mask/train2014
```

After pseudo-labels are generated from IRN, 

### Segmentation

Semantic Segmentation is run in the `segmentation` directory. From the root directory:

```console
cd segmentation
```

Train Deeplab v2
```console
python main.py train --config-path configs/voc12.yaml

python main.py train --config-path configs/coco14.yaml
```

Evaluate performance on validation set

```console
python main.py test --config-path configs/voc12.yaml --model-path output/voc12/models/train/checkpoint_final.pth

python main.py test --config-path configs/coco14.yaml --model-path output/coco14/models/train2014/checkpoint_final.pth
```

Evaluate with CRF post-processing
```console
python main.py crf --config-path configs/voc12.yaml

python main.py crf --config-path configs/coco14.yaml
```

## Acknowledgment

Much of this code was borrowed from [IRN](https://github.com/jiwoon-ahn/irn) and [deeplab-pytorch](https://github.com/kazuto1011/deeplab-pytorch)