import cv2

def convert_01(img):
    image = img.copy()
    image[image==255]=1
    image[image==0]=255
    image[image==1]=0

    return image