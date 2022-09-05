import os
import cv2
import numpy as np
from tqdm import tqdm
import glob
import albumentations as A
from albumentations import Compose

def strong_aug(p=1):
    return Compose(
        [
            A.PadIfNeeded(min_height=2500, min_width=2500, border_mode=cv2.BORDER_CONSTANT)#, value=[255,0,255], p=1)
        ],
        p=p,
        additional_targets={
            'image_1':'image',
            'image_2':'image',
        }
    )

def autopadding(image):
    augmentation = strong_aug(p=1)
    
    data = {'image':image, 'image_1':image}
    augmented = augmentation(**data)
    aug_img, aug_img1 = augmented['image'], augmented['image_1']

    return aug_img1

if __name__ == '__main__':
    images = sorted(glob('/data/kimsj/project/wku_rcft/image/wknz_copy_cropresult/*.jpg'))
    
    for path in tqdm(images):
        name = path.split('/')[-1]

        image = Image.open(path)
        image = np.array(image)
        autopadding_img = autopadding(image)

        cv2.imwrite('/data/kimsj/project/wku_rcft/image/padding_copy/{}'.format(name), autopadding_img)

