import pandas as pd
import os

TEAM_NAME = "Picipolo"
TEAM_ID = "8"
NAMES_CSV = ["META", "BAGOFWORDS_S", "BAGOFWORDS_N",
             "WYRAZENIA", "DANE"]
PATH_TO_RESULTS = "./results"

def create_all_csvs() -> None:
    for file in NAMES_CSV:
        path_to_save = os.path.join(PATH_TO_RESULTS, f"{TEAM_NAME}_{TEAM_ID}_{file}.csv")
        match file:
            case "META":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "NAZWA_PLIKU"]).to_csv(path_to_save)
            case "BAGOFWORDS_S":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save)
            case "BAGOFWORDS_N":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save)
            case "WYRAZENIA":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "WYRAZENIE", "FLAGA_WYSTAPIENIA"]).to_csv(path_to_save)
            case "DANE":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "ISIN", "IDENTYFIKATOR_KRAJOWY",
                                      "NUMER_RFI", "DATA_AKTUALIZACJI_KIID", "KATEGORIE_JEDNOSTEK_UCZESTNICTWA",
                                      "CZESTOTLIWOSC_ZBYWANIA_I_ODKUPOWANIA_JEDNOSTEK_UCZESTNICTWA",
                                      "CZY_FUNDUSZ_WYPLACA_DYWIDENDE", "BENCHMARK",
                                      "ZALECANY_OKRES_INWESTYCJI", "PROFIL_RYZYKA_I_ZYSKU", "SRRI",
                                      "FUND_TYPE"]).to_csv(path_to_save)
            case _:
                raise ValueError

