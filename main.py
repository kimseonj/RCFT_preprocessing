import os
import cv2
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from scipy.ndimage import interpolation as inter
from PIL import Image as im
from glob import glob
from tqdm import tqdm
from queue import Empty
from tqdm import tqdm

from libs.adaptive_threshold import adaptive_threshold
from libs.convexhull import convexhull
from libs.convert_01 import convert_01
from libs.resizing import resizing
import libs.remove_background
import libs.padding
import libs.autopadding
# import findContuours

with open('./config/wknz_rcft.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
block_size = config['adaptive_threshold']['block_size']
c = config['adaptive_threshold']['c']
black = config['black_preprocessing']

def preprocessing(img, rcft, name, black):
    img = cv2.imread(img,0)

    img = adaptive_threshold(img, block_size, c)
    result = libs.remove_background.remove_background(img, rcft, name, config)
    
    img = convert_01(result)
    img = convexhull(img)
    if (rcft == 'copy')|(rcft == 'cropped_copy') :
        img = libs.padding.set_copysize(img)
    crop_img = convert_01(img)
    # crop_img = img

    resizing_img = resizing(crop_img)
    
    img = libs.padding.square(crop_img, black)
    padding_img = resizing(img)

    autopadding_img = libs.autopadding.autopadding(crop_img, black)

    # crop_img = crop_img[753:,]
    # crop_img = convexhull(crop_img)
    # crop_img = convert_01(crop_img)

    result_img = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_GRAY2RGB)
    resizing_img = cv2.cvtColor(resizing_img, cv2.COLOR_GRAY2RGB)
    padding_img = cv2.cvtColor(padding_img, cv2.COLOR_GRAY2RGB)
    autopadding_img = cv2.cvtColor(autopadding_img, cv2.COLOR_GRAY2RGB)

    if black == False:
        return result_img, crop_img, resizing_img, padding_img, autopadding_img
    elif black == True:
        return convert_01(result_img), convert_01(crop_img),\
               convert_01(resizing_img), convert_01(padding_img), convert_01(autopadding_img)


def save_img(img_path, out_path, rcft):
    
    images = sorted(glob(os.path.join(img_path,rcft,'*.tiff')))
    
    os.makedirs(os.path.join(out_path,'result',rcft), exist_ok=True)
    os.makedirs(os.path.join(out_path,'crop',rcft), exist_ok=True)
    # os.makedirs(os.path.join(out_path,'padding',rcft), exist_ok=True)
    os.makedirs(os.path.join(out_path,'autopadding',rcft), exist_ok=True)

    # try:
    for img in tqdm(images):
        # jpg / tiff 둘다 사용하기 위해 확장자 나눠 줌
        name_extention = img.split('/')[-1]

        name = name_extention.split('.')[0]
        extention = name_extention.split('.')[1]
        
        result_img, crop_img, resizing_img, padding_img, autopadding_img = preprocessing(img, rcft, name, black)

        cv2.imwrite(os.path.join(out_path,'result',rcft,name+'.'+extention), result_img)
        cv2.imwrite(os.path.join(out_path,'crop',rcft,name+'.'+extention), crop_img)
        # cv2.imwrite(os.path.join(out_path,'padding',rcft,name+'.'+extention), padding_img)
        cv2.imwrite(os.path.join(out_path,'autopadding',rcft,name+'.'+extention), autopadding_img)

    # except:
    #     error.append(name)    

img_path = config['img_path']
out_path = config['out_path']

for rcft in config['rcft']:
    print(rcft)
    error = []
    # print(img_path)
    save_img(img_path, out_path, rcft)
    error_df = pd.DataFrame({'a':error})
    error_df.to_csv(rcft+'_error.csv', index=False)   