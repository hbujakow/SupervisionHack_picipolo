from main.utils import create_all_csvs
from data_extracter.extractor import DataExtractor
from bag_of_words.bag_of_words_creator import BagOfWordsCreator
from expression_checker.expression_checker import ExpressionClass
from info_csv import MetaInfo

import os
import PyPDF2


def main():
    primary_key = 1

    for file in os.list('./documents'):
        reader = PyPDF2.PdfFileReader(f'.documents/{file}')
        whole_text = [reader.getPage(i).extractText() for i in range(2)]
        tmp = [el.split('\n') for el in whole_text]
        whole_text = tmp[0]
        whole_text.extend(tmp[1])

        info_csv = MetaInfo()
        dataExtractor = DataExtractor()
        bagOfWords = BagOfWordsCreator()
        expressionChecker = ExpressionClass()

        info_csv.update_csv_file(file, primary_key)
        dataExtractor.update_csv_file(whole_text, primary_key)
        bagOfWords.update_csv_file(whole_text, primary_key)
        expressionChecker.update_csv_file(whole_text, primary_key)

        primary_key += 1


if __name__ == '__main__':
    create_all_csvs()
    # main()