# -*- coding: utf-8 -*-
"""Assignment_Yolact++.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fvq5-In6Ihv8hMwQ3N7M6rDonwXvQPyz

***Research Areas in Computer Vision :: Evaluating the Yolact++ Architecture***
"""

from google.colab import drive                        # Mounting Google Drive that contains image folders and annotations
drive.mount('/content/drive')

import json, os                                       # Importing necessary python libraries
import glob, shutil, random
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

!pip install cython                                   # Installing necessary libraries
!pip install opencv-python pillow pycocotools matplotlib

!pip install torchvision==0.5.                         # Downgrade torch to accommodate DCNv2
!pip install torch==1.4.0

!mkdir inference_images                               # Creating necessary folders
!mkdir output_images

!git clone https://github.com/dbolya/yolact.git       # Cloning repository

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolact/external/DCNv2

!python setup.py build develop                        # Build DCNv2

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolact/
!mkdir weights

def get_path(path):                                  # Getting all image paths of a given dataset from annotations
    json_file = os.path.join(path)

    with open(json_file) as f:
        imgs_anns = json.load(f)

    images = imgs_anns["images"]
    image_paths = []
    for x in images:
        image_paths.append(x["file_name"])

    return image_paths


def move_images(src_file, dst_file, paths):         # Method to move image from one folder to another
    for path in paths:
        shutil.copy(os.path.join(src_file, path), dst_file)

"""***Getting three random images from the MsCoco Val 2017 for testing***"""

json_path = "/content/drive/MyDrive/instances_val2017.json"

images = get_path(json_path)
test_images = []
for x in range(3):                                  
    img = random.choice(images)
    test_images.append(img)                         

move_images('/content/drive/MyDrive/val2017', '/content/inference_images', test_images)

"""***Getting three random images from the Tiny Voc Dataset for testing***"""

json_path = "/content/drive/MyDrive/tiny_voc_coco_train.json"

images = get_path(json_path)
test_images = []
for x in range(3):                                
    img = random.choice(images)
    test_images.append(img)                        

move_images('/content/drive/MyDrive/voc_train_images', '/content/inference_images', test_images)

"""***Run Evaluation for samples***"""

!python eval.py --trained_model=weights/yolact_plus_base_54_800000.pth --score_threshold=0.5 --top_k=15 --images=/content/inference_images:/content/output_images

output_images = Path('/content/output_images')

def show_images(img_path):
    img = cv2.imread(img_path)
    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(16,16))
    plt.imshow(img_cvt)
    plt.show()

for img_path in output_images.iterdir():
    print(img_path)
    show_images(str(img_path))

"""***Running evaluation on the entire dataset***

If running script, please change the path to the images folder and annotation folder from the config file (yolact/data/config).
"""

!python eval.py --trained_model=weights/yolact_plus_base_54_800000.pth --score_threshold=0.5 --top_k=15

!python eval.py --trained_model=weights/yolact_plus_base_54_800000.pth --score_threshold=0.5 --top_k=15 --output_coco_json

!nvidia-smi