import cv2

def remove_background(img, order, name):
    #세로, 가로
    #행, 열
    num = 255

    if order == 'copy':
        if name in ['wknz-025_1.tiff','wknz-146_1.tiff','wknz-038_1.tiff','wknz-063_1.tiff']:
            return img

        # 상하단 제거(snsb, 반응시간)
        img[:310,:] = num
        img[-145:,:] = num
        # 좌우 검은색 영역 제거
        img[:,:55] = num
        img[:,-25:] = num
    elif order == 'immediate':
        if name in ['wknz-012_2.tiff','wknz-021_2.tiff']:
            return img

        # snsb, 반응시간 제거
        img[:310,:]=num
        img[-260:,:]=num
        # 좌우 검은색 영역 제거
        img[:,:55] = num
        img[:,-45:] = num
    elif order == 'delay':
        if name in ['wknz-041_3.tiff','wknz-045_3.tiff','wknz-046_3.tiff']:
            return img

        # snsb, 반응시간 제거
        img[:300,:]=num
        img[-170:,:]=num
        # 좌우 검은색 영역 제거
        img[:,:50] = num
        img[:,-50:] = num

    return img
