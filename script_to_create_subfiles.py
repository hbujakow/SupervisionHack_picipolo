import os
from PyPDF2 import PdfFileWriter, PdfFileReader

root = './dokumenty-labelowanie/'

for folder in os.listdir(root):
    for file in os.listdir(os.path.join(root, folder)):
        inputpdf = PdfFileReader(open(os.path.join(root, folder + '/', file), "rb"))
        file_folder_name = file.replace('.pdf', '')
        files_path = os.path.join(root, folder, file_folder_name)
        isExist = os.path.exists(files_path)
        if not isExist:
            os.makedirs(files_path)
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open(os.path.join(files_path, file.replace('.pdf', f'_{i}.pdf')), "wb") as outputStream:
                output.write(outputStream)