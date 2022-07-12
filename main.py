import os
import cv2
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter
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
# import findContuours

with open('./config/snsb_rcft.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
block_size = config['adaptive_threshold']['block_size']
c = config['adaptive_threshold']['c']
black = config['black_preprocessing']

def white_preprocessing(img, rcft, name):
    img = cv2.imread(img,0)

    img = adaptive_threshold(img, block_size, c)
    result = libs.remove_background.remove_background(img, rcft, name, config)
    
    img = convert_01(result)
    img = convexhull(img)
    if rcft == 'copy':
        img = libs.padding.set_copysize(img)
    crop_img = convert_01(img)
    
    resizing_img = resizing(crop_img)
    
    img = libs.padding.square(crop_img, black)
    padding_img = resizing(img)
    
    result_img = cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
    crop_img = cv2.cvtColor(crop_img,cv2.COLOR_GRAY2RGB)
    resizing_img = cv2.cvtColor(resizing_img,cv2.COLOR_GRAY2RGB)
    padding_img = cv2.cvtColor(padding_img,cv2.COLOR_GRAY2RGB)

    return result_img, crop_img, resizing_img, padding_img

def black_preprocessing(img, rcft, name):
    img = cv2.imread(img,0)
    
    img = adaptive_threshold(img, block_size, c)
    result = libs.remove_background.remove_background(img, rcft, name, config)
    result = convert_01(result)

    # img = convert_01.convert_01(result)
    img = convexhull(result)
    if rcft == 'copy':
        img = libs.padding.set_copysize(img)
    # crop_img = convert_01.convert_01(img)
    crop_img = img

    resizing_img = resizing(crop_img)

    img = libs.padding.square(crop_img, black)
    padding_img = resizing(img)

    result_img = cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
    crop_img = cv2.cvtColor(crop_img,cv2.COLOR_GRAY2RGB)
    resizing_img = cv2.cvtColor(resizing_img,cv2.COLOR_GRAY2RGB)
    padding_img = cv2.cvtColor(padding_img,cv2.COLOR_GRAY2RGB)

    return result_img, crop_img, resizing_img, padding_img

def save_img(img_path, out_path, rcft):
    
    # 2022.06.28 잠시 추가
    # images = sorted(glob(img_path+rcft+'_data/'+rcft+'/*.jpg'))
    score_0 = pd.read_csv('/home/kimsj/project/wku_rcft/rcft/score_0_dx.csv')
    rcft_score_0 = score_0[score_0['rcft'] == rcft]
    images = 'rcft/' + rcft_score_0['img'] + '.jpg'
    
    # '/storage/kimsj/SNSB/wku_project/snsb_rcft/divided_OID_Unum/copy_data/copy/2579_3260.jpg'
    
    os.makedirs(out_path+'/result/'+rcft, exist_ok=True)
    os.makedirs(out_path+'/crop/'+rcft, exist_ok=True)
    os.makedirs(out_path+'/resizing/'+rcft, exist_ok=True)
    os.makedirs(out_path+'/padding/'+rcft, exist_ok=True)
            
    try:
        for img in tqdm(images):
            name_extention = img.split('/')[-1]
            
            name = name_extention.split('.')[0]
            extention = name_extention.split('.')[1]
            
            # 2022.06.28 잠시 추가
            img = '/storage/kimsj/SNSB/wku_project/snsb_rcft/divided_OID_Unum/delay_data/delay/9575_85239.jpg'
            
            if black == True:
                result_img, crop_img, resizing_img, padding_img = black_preprocessing(img, rcft, name)
            else:
                result_img, crop_img, resizing_img, padding_img = white_preprocessing(img, rcft, name)
                
            cv2.imwrite(out_path+'/result/'+rcft+'/'+name+'.jpg',result_img)
            cv2.imwrite(out_path+'/crop/'+rcft+'/'+name+'.jpg',crop_img)
            cv2.imwrite(out_path+'/resizing/'+rcft+'/'+name+'.jpg',resizing_img)
            cv2.imwrite(out_path+'/padding/'+rcft+'/'+name+'.jpg',padding_img)
    except:
        error.append(name)    

img_path = config['img_path']
out_path = config['out_path']
# rcft = config['rcft'][0]
 
config['rcft'] = ['immediate', 'delay']
for rcft in config['rcft']:
    print(rcft)
    error = []
    save_img(img_path, out_path, rcft)
    error_df = pd.DataFrame({'a':error})
    error_df.to_csv(rcft+'_error.csv', index=False)   