import cv2
from glob import glob
from tqdm import tqdm
import numpy as np

# 설정 크기로 변환
def set_size(img, size_h, size_w):
    h,w = img.shape[0:2]
    top,bottom,left,right = 0,0,0,0

    # 가로, 세로 중 가장 긴 변을 찾는다.
    if h<size_h:
        delta_h = size_h - h
        top, bottom = delta_h//2, (delta_h-(delta_h//2)) #0, (delta_h-(delta_h//2))*2
    if w<size_w:
        delta_w = size_w - w
        left, right = delta_w//2, delta_w-(delta_w//2)

    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    return new_img

# 개별 변환
def square(img, black):
    h,w = img.shape[0:2]
    if h > w:
        delta_w = h - w
        
        top, bottom = 0, 0
        left, right = delta_w//2, delta_w-(delta_w//2)
    else:
        delta_h = w - h

        top, bottom = delta_h//2, (delta_h-(delta_h//2))
        left, right = 0,0
    
    if black == True:    
        new_img = cv2.copyMakeBorder(img, top+100, bottom+100, left+100, right+100, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    else:
        new_img = cv2.copyMakeBorder(img, top+100, bottom+100, left+100, right+100, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    return new_img

def set_copysize(img):
    h,w = img.shape[0:2]
    top,bottom,left,right = 0,0,0,0
    size_h = 1500

    # 가로, 세로 중 가장 긴 변을 찾는다.
    if h<size_h:
        delta_h = size_h - h
        top, bottom = 0, delta_h
    
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return new_img

# padding_img = square(h,w)

# padding_img = set_size(h,w,size_h,size_w)

# return padding_img

def pre(path, save_path):
    images = sorted(glob(path+'/*.jpg'))

    h = []
    w = []
    error = []
    for stop, img in enumerate(tqdm(images)):
        # if stop<29:
            # continue
            
        try:
            name = img.split('/')[-1]
            img = cv2.imread(img,0)
            new_img = padding(img)
            # final_color = cv2.cvtColor(new_img,cv2.COLOR_GRAY2RGB)
            cv2.imwrite(save_path+'/'+name,new_img)
        except:
            error.append(name)
            continue    

        # if stop>30:
        #     break


# path = '/storage/kimsj/SNSB/pentagon/score_20220511/preprocessing/img01/score_0'
# save_path = '/storage/kimsj/SNSB/pentagon/score_20220511/preprocessing/resize_img01/score_0'
# pre(path,save_path)