import pandas as pd
import os
from config_loader import load_config

config = load_config()

TEAM_NAME = config['TEAM']['TEAM_NAME']
TEAM_ID = config['TEAM']['TEAM_ID']
NAMES_CSV = ["META", "BAGOFWORDS_S", "BAGOFWORDS_N",
             "WYRAZENIA", "DANE"]
PATH_TO_RESULTS = config["RESULTS"]["PATH"]

def create_all_csvs() -> None:
    for file in NAMES_CSV:
        path_to_save = os.path.join(PATH_TO_RESULTS, f"{TEAM_NAME}_{TEAM_ID}_{file}.csv")
        match file:
            case "META":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "NAZWA_PLIKU"]).to_csv(path_to_save, index=False)
            case "BAGOFWORDS_S":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save, index=False)
            case "BAGOFWORDS_N":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save, index=False)
            case "WYRAZENIA":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "WYRAZENIE", "FLAGA_WYSTAPIENIA"]).to_csv(path_to_save, index=False)
            case "DANE":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "ISIN", "IDENTYFIKATOR_KRAJOWY",
                                      "NUMER_RFI", "DATA_AKTUALIZACJI_KIID", "KATEGORIE_JEDNOSTEK_UCZESTNICTWA",
                                      "CZESTOTLIWOSC_ZBYWANIA_I_ODKUPOWANIA_JEDNOSTEK_UCZESTNICTWA",
                                      "CZY_FUNDUSZ_WYPLACA_DYWIDENDE", "BENCHMARK",
                                      "ZALECANY_OKRES_INWESTYCJI", "PROFIL_RYZYKA_I_ZYSKU", "SRRI",
                                      "FUND_TYPE"]).to_csv(path_to_save, index=False)
            case _:
                raise ValueError

