import pandas as pd
from main import utils
import expression_utils
import word_matching

class ExpressionClass():
    def __init__(self):
        self.required = expression_utils.required

    def update_csv(self, primary_key, pdf_name):
        data = utils.read_data('WYRAZENIA')
        for sentence in self.required:
            record = pd.DataFrame([[primary_key, utils.TEAM_ID, sentence, word_matching.word_matching(sentence, pdf_name)]],
                                  columns=data.columns)
            data = pd.concat([data, record])
        utils.export(data, 'WYRAZENIA')

