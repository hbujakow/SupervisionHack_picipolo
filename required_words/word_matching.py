import os
import pandas as pd
from PyPDF2 import PdfReader
from fuzzywuzzy import fuzz
import fitz
import re

alphabets = "([A-Za-z])"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def pdfToString(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def newPdfToString(file):
    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text()

    return text


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def word_matching(folder, out="./required.csv"):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    required = ["kluczowe informacje dla inwestorów",
                "niniejszy dokument zawiera kluczowe informacje dla inwestorów dotyczące tego funduszu. "
                "nie są to materiały marketingowe. dostarczenie tych informacji jest wymogiem prawnym mającym na "
                "celu ułatwienie zrozumienia charakteru i ryzyka związanego z inwestowaniem w ten fundusz. "
                "przeczytanie niniejszego dokumentu jest zalecane inwestorowi, "
                "aby mógł on podjąć świadomą decyzję inwestycyjną.",
                "niniejsze kluczowe informacje dla inwestorów są aktualne na dzień",
                "fundusz otrzymał zezwolenie na prowadzenie działalności w",
                "zalecenie: niniejszy fundusz może nie być odpowiedni dla inwestorów, "
                "którzy planują wycofać swoje środki w ciągu",
                "może zostać pociągnięta do odpowiedzialności za każde oświadczenie zawarte w niniejszym dokumencie, "
                "które wprowadza w błąd, jest niezgodne ze stanem faktycznym lub niespójne "
                "z odpowiednimi częściami prospektu emisyjnego UCITS.",
                "opłaty jednorazowe pobierane przed lub po dokonaniu inwestycji",
                "opłata za subskrypcję",
                "opłata za umorzenie",
                "opłaty pobierane z funduszu w ciągu roku",
                "opłaty bieżące",
                "opłaty pobierane z funduszu w określonych warunkach szczególnych",
                "opłata za wyniki",
                "cele i polityka inwestycyjna",
                "profil ryzyka i zysku",
                "opłaty",
                "wyniki osiągnięte w przeszłości",
                "informacje praktyczne"]

    df = pd.DataFrame(
        columns=["file", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                 "18"])

    for file in files:
        list = [0] * 19
        list[0] = file
        text = str.lower(newPdfToString(file))
        text = re.sub('\s{2,}', ' ', text)
        sentences = split_into_sentences(text)

        for j in range(len(required)):
            if j == 1:
                if fuzz.partial_ratio(required[j], text) >= 95:
                    list[j + 1] = 1

            else:
                for sentence in sentences:
                    if fuzz.partial_ratio(required[j], sentence) >= 95:
                        list[j + 1] = 1
                        break

        df = df.append(pd.DataFrame([list],
                                    columns=["file", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                                             "13",
                                             "14", "15", "16", "17", "18"]),
                       ignore_index=True)

        df.to_csv(out)