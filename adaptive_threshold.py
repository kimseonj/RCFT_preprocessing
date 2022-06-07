import cv2

def adaptive_threshold(img):
    # median filter // Remove noise
    img = cv2.medianBlur(img,3)

    # adaptive Threshold // graysclae
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,17,5)
    
    return img