import cv2
import yaml

def remove_background(img, order, name, config):

    copy_up = config['remove_background']['copy']['up']
    copy_down = config['remove_background']['copy']['down']
    copy_left = config['remove_background']['copy']['left']
    copy_right = config['remove_background']['copy']['right']

    immediate_up = config['remove_background']['immediate']['up']
    immediate_down = config['remove_background']['immediate']['down']
    immediate_left = config['remove_background']['immediate']['left']
    immediate_right = config['remove_background']['immediate']['right']

    delay_up = config['remove_background']['delay']['up']
    delay_down = config['remove_background']['delay']['down']
    delay_left = config['remove_background']['delay']['left']
    delay_right = config['remove_background']['delay']['right']

    #세로, 가로
    #행, 열
    num = 255
    if order == 'copy':
        if name in ['wknz-025_1.tiff','wknz-146_1.tiff','wknz-038_1.tiff','wknz-063_1.tiff']:
            return img

        # 상하단 제거(snsb, 반응시간)
        img[:copy_up,:] = num
        img[copy_down:,:] = num
        # 좌우 검은색 영역 제거
        img[:,:copy_left] = num
        img[:,copy_right:] = num
    elif order == 'immediate':
        if name in ['wknz-012_2.tiff','wknz-021_2.tiff']:
            return img

        # snsb, 반응시간 제거
        img[:immediate_up,:]=num
        img[immediate_down:,:]=num
        # 좌우 검은색 영역 제거
        img[:,:immediate_left] = num
        img[:,immediate_right:] = num
    elif order == 'delay':
        if name in ['wknz-041_3.tiff','wknz-045_3.tiff','wknz-046_3.tiff']:
            return img

        # snsb, 반응시간 제거
        img[:delay_up,:]=num
        img[delay_down:,:]=num
        # 좌우 검은색 영역 제거
        img[:,:delay_left] = num
        img[:,delay_right:] = num

    return img

'''
wku_rcft

copy
310
-145
55
-25

immediate
310
-260
55
-45

delay
300
-170
50
-50
'''