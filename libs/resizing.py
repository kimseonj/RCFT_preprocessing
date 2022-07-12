import cv2
from glob import glob
from tqdm import tqdm

def resizing(img):
    src = img
    dst = cv2.resize(src, dsize=(2500, 2500), interpolation=cv2.INTER_LANCZOS4)

    return dst