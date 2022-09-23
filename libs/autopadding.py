import os
import cv2
import numpy as np
from tqdm import tqdm
from glob import glob
from PIL import Image

import albumentations as A
from albumentations import Compose



def strong_aug(p=1, value=[255,255,255]):
    return Compose(
        [
            A.PadIfNeeded(min_height=1650, min_width=1800, border_mode=cv2.BORDER_CONSTANT, value=value)#, p=1)
        ],
        p=p,
        additional_targets={
            'image_1':'image',
            'image_2':'image',
        }
    )

def autopadding(image, black):
    if black == True:
        black = [255,255,255]
    else :
        black = [0,0,0]
    augmentation = strong_aug(p=1, value=black)
    
    data = {'image':image, 'image_1':image}
    augmented = augmentation(**data)
    aug_img, aug_img1 = augmented['image'], augmented['image_1']

    return aug_img1

if __name__ == '__main__':
    images = sorted(glob('/data/wknz_rcft_tiff/black_background/crop_1/immediate/*.tiff'))
    save_path = '/data/wknz_rcft_tiff/black_background/autopadding/immediate'

    os.makedirs(save_path, exist_ok=True)

    for path in tqdm(images):
        name = path.split('/')[-1]

        image = Image.open(path)
        image = np.array(image)
        autopadding_img = autopadding(image)

        cv2.imwrite(os.path.join(save_path,name), autopadding_img)

