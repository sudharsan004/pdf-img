# from pdf_processor.settings import BASE_DIR
from io import BytesIO
import os, fitz , datetime
# # Python3 program to convert image to pfd
# using img2pdf library
# importing necessary libraries
import img2pdf
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import os
# Create your views here.

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

BASE_DIR = os.getcwd()
dir = os.path.join(BASE_DIR,'path')
input_dir= os.path.join(BASE_DIR,'input')
output_dir= os.path.join(BASE_DIR,'output')

def clean_dir():
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def pdfToImg(pdfPath, imagePath,page_no):    
    # print("imagePath="+imagePath)
    # print(pdfPath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
                 # The scaling factor for each size is 1.3, which will generate an image with a resolution increase of 2.6 for us.
                 # If there is no setting here, the default picture size is: 792X612, dpi=96
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#Determine whether the folder where the image is stored exists
            os.makedirs(imagePath) # If the image folder does not exist, create it

        pix.writePNG(imagePath+'/'+f'{page_no}.png')#Write the picture into the specified folder
        
        
 



def home(filename):
    clean_dir()
    # if request.method == "POST" and request.FILES['myfile']:
    # print(request.POST)
    # myfile = open('input.pdf')
    # print(myfile)
    inputpdf = PdfFileReader(os.path.join(input_dir,filename),strict=False)
    # inputpdf = PdfFileReader(myfile)
    # print(inputpdf.getNumPages())
    # for i in range(myfile.numPages):
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        if(i<10):
            file_path= os.path.join(dir,f'0{i}.pdf')
        else:
            file_path= os.path.join(dir,f'{i}.pdf')

        with open(file_path, "wb") as outputStream:
            output.write(outputStream)

    # page_no = input("Enter Page numbers: ")
    # print(page_no.split(','))
    input_array=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for f in os.listdir(dir):
        for page in input_array:
            if page-1<10:
                if f'0{page-1}.pdf' in f:
                    # print(f)
                    pdfToImg(os.path.join(dir,f),dir,page)
                    image = Image.open(os.path.join(dir,f'{page}.png'))
                    # converting into chunks using img2pdf
                    pdf_bytes = img2pdf.convert(image.filename)

                    # opening or creating pdf file
                    file = open(os.path.join(dir,f), "wb")

                    # writing pdf files with chunks
                    file.write(pdf_bytes)
                    image.close()
                    file.close()
            else:
                if f'{page-1}.pdf' in f:
                    # print(f)
                    pdfToImg(os.path.join(dir,f),dir,page)
                    image = Image.open(os.path.join(dir,f'{page}.png'))
                    # converting into chunks using img2pdf
                    pdf_bytes = img2pdf.convert(image.filename)

                    # opening or creating pdf file
                    file = open(os.path.join(dir,f), "wb")

                    # writing pdf files with chunks
                    file.write(pdf_bytes)
                    image.close()
                    file.close()

    output = PdfFileMerger()
    for f in os.listdir(dir):
        if '.pdf' in f:
            pdf = PdfFileReader(os.path.join(dir,f))
            output.append(pdf)
    # outputStream = BytesIO()
    # output.write(outputStream)
    # response.write(outputStream.getvalue())
    with open(os.path.join(output_dir,filename), "wb") as outputStream:
        output.write(outputStream)
    clean_dir()
count=1
for file in os.listdir(input_dir):
    startTime_pdf2img = datetime.datetime.now()#Start time
    print(f'Processing file {file} ...')
    home(file)
    endTime_pdf2img = datetime.datetime.now()#end time
    print(f'time taken : {(endTime_pdf2img-startTime_pdf2img).seconds} seconds')
