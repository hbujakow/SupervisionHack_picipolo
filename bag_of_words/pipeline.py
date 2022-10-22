from xmlrpc.client import boolean

from traitlets import Bool, default
import fitz
from typing import List
import re
import pandas as pd
import collections, itertools
import spacy
# from spacy.lang.pl.examples import sentences 

model = spacy.load('pl_core_news_sm')

def read_pdf(file: str) -> str:
    text=[]
    with fitz.open(file) as doc:
        for page in doc:
            text.append(page.get_text())
    return ' '.join(text)

def get_stopwords(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        stopwords = [line[:-1] for line in f.readlines()]
    return stopwords

def preprocessing(text: str, lemmatized: bool) -> str:
    t = text.replace('\n', ' ')
    wihtout_stopwords = " ".join([word for word in t.split() if word not in get_stopwords('./stopwords.txt')])
    result = re.sub("[^a-zA-Z0-9ąęćśńółźż]", " ", wihtout_stopwords)
    if lemmatized:
        result = re.sub("[^a-zA-Ząęćśńółźż]", " ", wihtout_stopwords)
        doc = model(result)
        result = " ".join([token.lemma_ for token in doc])
    return result

def create_bag_of_words(file: str, organisation: str, lemmatized = False) -> pd.DataFrame:
    data = read_pdf(f)
    data_preprocessed = preprocessing(data, lemmatized)
    counter = dict(collections.Counter(itertools.chain.from_iterable(x.split() for x in [data_preprocessed])))
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df = df.rename(columns={'index':'words', 0: 'count'})
    df ['organisation'] = organisation
    return df

if __name__ == "__main__":
    files = ['KIID_BNP_Paribas_GSW_2022-09-21-11.pdf', 'KIID_MIL01_2022-02-21.pdf'] ## example
    data_raw = pd.DataFrame(columns=["words", "count", "organisation"])
    data_normalised = pd.DataFrame(columns=["words", "count", "organisation"])
    for f in files:
        df_raw = create_bag_of_words(f, f[:-4])
        df_normalised = create_bag_of_words(f, f[:-4], True)
        data_raw = pd.concat([data_raw, df_raw])
        data_normalised = pd.concat([data_normalised, df_normalised])
    # print(data_normalised)