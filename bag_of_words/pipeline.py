import fitz
from typing import List
import re
import pandas as pd

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

def preprocessing(text: str) -> str:
    t = text.replace('\n', '')
    result = [word for word in t if word not in get_stopwords('./stopwords.txt')]
    result = re.sub("[^a-zA-Z0-9ąęćśńółźż]", " ", t)
    return result

def create_bag_of_words(text: str, organisation: str) -> pd.DataFrame:
    import collections, itertools
    counter = dict(collections.Counter(itertools.chain.from_iterable(x.split() for x in [text])))
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df = df.rename(columns={'index':'words', 0: 'count'})
    df ['organisation'] = organisation
    return df

if __name__ == "__main__":
    files = ['KIID_BNP_Paribas_GSW_2022-09-21-8.pdf', 'KIID_MIL01_2022-02-21.pdf']
    final_data = pd.DataFrame(columns=["words", "count", "organisation"])
    for f in files:
        data = read_pdf(f)
        data_preprocessed = preprocessing(data)
        df = create_bag_of_words(data_preprocessed, f[:-4])
        final_data = pd.concat([final_data, df])
    print(final_data)