import spacy
from traitlets import Bool, default
import fitz
from typing import List
import re
import pandas as pd
import collections, itertools
import sys, os
from main.utils import TEAM_NAME, TEAM_ID, read_data, export_data, Name

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BagOfWordsCreator:
    def __init__(self, model=spacy.load("pl_core_news_sm")):
        self.model = model

    def create_csv(self, text: str, main_key: int) -> None:
        data_raw = read_data(Name.BAGOFWORDS_S.value)
        data_normalised = read_data(Name.BAGOFWORDS_N.value)
        df_raw = self.create_bag_of_words(text, main_key)
        df_normalised = self.create_bag_of_words(text, main_key, True)
        data_raw = pd.concat([data_raw, df_raw])
        export_data(data_raw, Name.BAGOFWORDS_S.value)
        data_normalised = pd.concat([data_normalised, df_normalised])
        export_data(data_normalised, Name.BAGOFWORDS_N.value)

    def get_stopwords(self, filepath: str) -> List[str]:
        with open(filepath, 'r') as f:
            stopwords = [line[:-1] for line in f.readlines()]
        return stopwords

    def preprocessing(self, text: str, lemmatized: bool) -> str:
        t = text.replace('\n', ' ')
        wihtout_stopwords = " ".join([word for word in t.split() if word not in self.get_stopwords('./stopwords.txt')])
        result = re.sub("[^a-zA-Z0-9ąęćśńółźż]", " ", wihtout_stopwords)
        if lemmatized:
            result = re.sub("[^a-zA-Ząęćśńółźż]", " ", wihtout_stopwords)
            doc = self.model(result)
            result = " ".join([token.lemma_ for token in doc])
        return result

    def create_bag_of_words(self, data: str, main_key: int, lemmatized=False) -> pd.DataFrame:
        data_preprocessed = self.preprocessing(data, lemmatized)
        counter = dict(collections.Counter(itertools.chain.from_iterable(x.split() for x in [data_preprocessed])))
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df = df.rename(columns={'index': 'SLOWA', 0: 'LICZBA'})
        df['ID_KIID'] = main_key
        df['ID_ZESPOLU'] = TEAM_ID
        return df
