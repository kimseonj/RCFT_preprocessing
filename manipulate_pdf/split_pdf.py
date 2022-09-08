# pdf2tiff
# ! pip install PyPDF2

# pdf split
from PyPDF2 import PdfFileWriter, PdfFileReader

import os
from glob import glob
from tqdm import tqdm

def split_pdf(pdf_path, save_path):
    file_name = pdf_path.split('/')[-1]
    inputpdf = PdfFileReader(open(pdf, "rb"))

#     for i in range(inputpdf.numPages):
#         output = PdfFileWriter()
#         output.addPage(inputpdf.getPage(i))
#         with open(os.path.join(save_path, file_name), "wb") as outputStream:
#             output.write(outputStream)
            
    # 원광대학교
    os.makedirs(os.path.join(save_path,'info'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'copy'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'immediate'), exist_ok=True)
    os.makedirs(os.path.join(save_path,'delay'), exist_ok=True)  

    rcfts = ['info', 'copy', 'immediate', 'delay']
    
    for i, rcft in zip(range(inputpdf.numPages), rcfts):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(os.path.join(save_path, rcft, file_name), "wb") as outputStream:
            output.write(outputStream)
    
# run
pdfs = sorted(glob('/data/wknz_original/all/*.pdf'))
save_path = '/data/kimsj/split_pdf'

for pdf in tqdm(pdfs):
    split_pdf(pdf, save_path)