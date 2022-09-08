# pdf2imgae
from pdf2image import convert_from_path

import os
from tqdm import tqdm
from glob import glob

def enu(pdf_path, save_path):
    file_name = pdf_path.split('/')[-1].split('.')[0]
    
    pages = convert_from_path(pdf_path)
    
#     for page, i in enumerate(pages, start=1):
#         page.save(os.path.join(save_path,(file_name + '_{}'.format(i) + '.jpg')), 'JPEG')

    # 원광대학교  
    os.makedirs(os.path.join(save_path,'info'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'copy'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'immediate'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'delay'), exist_ok=True)    
        
    rcfts = ['info', 'copy', 'immediate', 'delay']
    for page, rcft in zip(pages, rcfts):
        page.save(os.path.join(save_path,rcft,(file_name + '.jpg')), 'JPEG')


# run
files_path = sorted(glob('/data/wknz_original/all/*.pdf'))
save_path = '/data/kimsj/test1/'

for file in tqdm(files_path):
    enu(file, save_path)