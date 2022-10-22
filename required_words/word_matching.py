import utils.word_validator as word_validator


def word_matching(data, pdf_name, threshhold=95):
    data = data.lower()
    text = str.lower(word_validator.pdfToString(pdf_name))
    text = word_validator.re.sub('\s{2,}', ' ', text)
    sentences = word_validator.split_into_sentences(text)
    print(text)
    if word_validator.fuzz.partial_ratio(data, text) >= threshhold:
        return True
    else:
        for sentence in sentences:
            if word_validator.fuzz.partial_ratio(data, sentence) >= threshhold:
                return True
    return False


if __name__ == '__main__':
    print(word_matching('pekao konserwatywny plus', 'ex'))
