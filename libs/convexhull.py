import cv2
from queue import Empty

def convexhull(img):
    image = img.copy()

    img = cv2.medianBlur(img,5)
    # img = cv2.medianBlur(img,19)

    contour, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    x=[]
    y=[]
    h=[]
    w=[]

    for i,cnt in enumerate(contour):
        if cv2.contourArea(cnt)<10:
            continue
        hull = cv2.convexHull(cnt,clockwise=True)
        # cv2.drawContours(img, [hull], 0, (0, 255, 0), 2)
        a,b,c,d = cv2.boundingRect(cnt)
        x.append(a),y.append(b),h.append(b+d),w.append(a+c)

    # x.remove(0)
    # y.remove(0)
    # h.remove(3508)
    # w.remove(2480)

    # print(x)
    # print(y)
    # print(h)
    # print(w)
    # exit()

    if len(x) == 0 & len(y)==0 & len(w)==0 & len(h)==0:
        print('image is none')

        return img 

    image = image[min(y):max(h),min(x):max(w)]
    
    # 전처리가 부족하닥 생각되어 crop하여 삭제된 원본 이미지를 +100만큼 "복구"
    # image = image[min(y)+100:max(h)+100,min(x)+100:max(w)+100]
    
    # 전처리 crop이 완벽하게 됐다고 가정하고 새로운 공백 이미지를 +100만큼 "추가"
    image = cv2.copyMakeBorder(image, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return image
