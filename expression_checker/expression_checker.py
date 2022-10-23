import pandas as pd
from main.utils import read_data, TEAM_ID, export_data, Name
import expression_utils
from expression_checker.word_validator import word_matching


class ExpressionClass():
    def __init__(self):
        self.required = expression_utils.required

    def update_csv_file(self, primary_key, pdf_name):
        data = read_data(Name.WYRAZENIA.value)
        for sentence in self.required:
            record = pd.DataFrame(
                [[primary_key, TEAM_ID, sentence, word_matching.word_matching(sentence, pdf_name)]],
                columns=data.columns)
            data = pd.concat([data, record])
        export_data(data, Name.WYRAZENIA.value)
