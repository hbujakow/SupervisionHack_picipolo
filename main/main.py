from utils import create_all_csvs
from data_extracter.extractor import DataExtractor

import PyPDF2


# Scraper
# Initializing all modules
# Loop iterating all documents
# All modules call -> which results in 5 csv creations
# Finito

def main():
    # print('cokolwiek')
    reader = PyPDF2.PdfFileReader('documents/KIID_AGIO_Dochodowy_PLUS-1.pdf')
    whole_text = [reader.getPage(i).extractText() for i in range(2)]
    tmp = [el.split('\n') for el in whole_text]
    whole_text = tmp[0]
    whole_text.extend(tmp[1])

    dataExtractor = DataExtractor()
    dataExtractor.update_csv_file(whole_text, 1)

if __name__ == '__main__':
    create_all_csvs()
    main()