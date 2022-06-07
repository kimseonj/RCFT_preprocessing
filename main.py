import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter
from PIL import Image as im
from glob import glob
from tqdm import tqdm
from queue import Empty
from tqdm import tqdm

import adaptive_threshold
import remove_background
import convexhull
import convert_01
import padding
import resizing
# import findContuours

def preprocessing(img, rcft, name):
    img = cv2.imread(img,0)

    img = adaptive_threshold.adaptive_threshold(img)
    result = remove_background.remove_background(img, rcft, name)
    
    img = convert_01.convert_01(result)
    img = convexhull.convexhull(img)
    if rcft == 'copy':
        img = padding.set_copysize(img)
    crop_img = convert_01.convert_01(img)
    
    resizing_img = resizing.resizing(crop_img)
    
    img = padding.square(crop_img)
    padding_img = resizing.resizing(img)
    
    result_img = cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
    crop_img = cv2.cvtColor(crop_img,cv2.COLOR_GRAY2RGB)
    resizing_img = cv2.cvtColor(resizing_img,cv2.COLOR_GRAY2RGB)
    padding_img = cv2.cvtColor(padding_img,cv2.COLOR_GRAY2RGB)

    return result_img, crop_img, resizing_img, padding_img

def save_img(rcft):
    images = sorted(glob(img_path+rcft+'/*.tiff'))
    
    for img in tqdm(images):
        name = img.split('/')[-1]

        result_img, crop_img, resizing_img, padding_img = preprocessing(img, rcft, name)
        
        cv2.imwrite('/storage/kimsj/SNSB/wku_RCFT/tiff_result/result/'+rcft+'/'+name,result_img)
        cv2.imwrite('/storage/kimsj/SNSB/wku_RCFT/tiff_result/crop/'+rcft+'/'+name,crop_img)
        cv2.imwrite('/storage/kimsj/SNSB/wku_RCFT/tiff_result/resizing/'+rcft+'/'+name,resizing_img)
        cv2.imwrite('/storage/kimsj/SNSB/wku_RCFT/tiff_result/padding/'+rcft+'/'+name,padding_img)
        

img_path = '/storage/kimsj/SNSB/wku_RCFT/img/tiff_img/modify_img/'
out_path = '/storage/kimsj/SNSB/wku_RCFT/img/tiff_img/'
rcft = 'delay'
    
save_img(rcft)

'''
흑백반전 이미지 일때 사용.
padding.square 의 0 255는 바꿔줘야한다.

img = adaptive_threshold.adaptive_threshold(img)
result = remove_background.remove_background(img, rcft, name)
result = convert_01.convert_01(result)

# img = convert_01.convert_01(result)
img = convexhull.convexhull(result)
if rcft == 'copy':
    img = padding.set_copysize(img)
# crop_img = convert_01.convert_01(img)
crop_img = img

resizing_img = resizing.resizing(crop_img)

img = padding.square(crop_img)
padding_img = resizing.resizing(img)

result_img = cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
crop_img = cv2.cvtColor(crop_img,cv2.COLOR_GRAY2RGB)
resizing_img = cv2.cvtColor(resizing_img,cv2.COLOR_GRAY2RGB)
padding_img = cv2.cvtColor(padding_img,cv2.COLOR_GRAY2RGB)
'''