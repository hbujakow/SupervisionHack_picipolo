import spacy
from traitlets import Bool, default
import fitz
from typing import List
import re
import pandas as pd
import collections, itertools
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import TEAM_NAME, TASK

data_raw = pd.DataFrame(columns=["words", "count", "organisation", "team_id"])
data_normalised = pd.DataFrame(columns=["words", "count", "organisation", "team_id"])

class BagOfWordsCreator:
    def __init__(self, model=spacy.load("pl_core_news_sm")):
        self.model = model

    def create_csv(self, text: str, main_key: int) -> None:
        data_raw = f"../results/{TEAM_NAME}_{KIID}_BAGOFWORDS_R.csv"
        data_normalised = f"../results/{TEAM_NAME}_{KIID}_BAGOFWORDS_N.csv"
        df_raw = create_bag_of_words(text, main_key)
        df_normalised = create_bag_of_words(f, main_key, True)
        data_raw = pd.concat([data_raw, df_raw])
        data_raw.to_csv(f'../results/{TEAM_NAME}_{KIID}_BAGOFWORDS_R.csv')
        data_normalised = pd.concat([data_normalised, df_normalised])
        data_normalised.to_csv(f"../results/{TEAM_NAME}_{KIID}_BAGOFWORDS_N.csv")

    def get_stopwords(self, filepath: str) -> List[str]:
        with open(filepath, 'r') as f:
            stopwords = [line[:-1] for line in f.readlines()]
        return stopwords

    def preprocessing(self, text: str, lemmatized: bool) -> str:
        t = text.replace('\n', ' ')
        wihtout_stopwords = " ".join([word for word in t.split() if word not in get_stopwords('./stopwords.txt')])
        result = re.sub("[^a-zA-Z0-9ąęćśńółźż]", " ", wihtout_stopwords)
        if lemmatized:
            result = re.sub("[^a-zA-Ząęćśńółźż]", " ", wihtout_stopwords)
            doc = model(result)
            result = " ".join([token.lemma_ for token in doc])
        return result

    def create_bag_of_words(self, data: str, main_key: int, lemmatized = False) -> pd.DataFrame:
        data_preprocessed = self.preprocessing(data, lemmatized)
        counter = dict(collections.Counter(itertools.chain.from_iterable(x.split() for x in [data_preprocessed])))
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df = df.rename(columns={'index':'SLOWA', 0: 'LICZBA'})
        df['ID_KIID'] = main_key
        df['ID_ZESPOLU'] = 8
        return df
