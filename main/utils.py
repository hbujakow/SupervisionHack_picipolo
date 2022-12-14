import pandas as pd
import os, sys
from enum import Enum
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_loader import load_config

config = load_config(str(Path(__file__).resolve().parents[1].joinpath('config.json')))

TEAM_NAME = config['TEAM']['TEAM_NAME']
TEAM_ID = config['TEAM']['TEAM_ID']
NAMES_CSV = ["META", "BAGOFWORDS_S", "BAGOFWORDS_N",
             "WYRAZENIA", "DANE"]
TASK = config['TEAM']["TASK"]
PATH_TO_RESULTS = str(Path(__file__).resolve().parents[1].joinpath(config["RESULTS"]["PATH"]))


class Name(Enum):
    BAGOFWORDS_N = 'BAGOFWORDS_N'
    BAGOFWORDS_S = 'BAGOFWORDS_S'
    DANE = 'DANE'
    META = 'META'
    WYRAZENIA = 'WYRAZENIA'


def export_data(df, name):
    df.to_csv(PATH_TO_RESULTS + '/' + TEAM_NAME + "_" + TASK + "_" + name + '.csv')


def read_data(name):
    try:
        data = pd.read_csv(PATH_TO_RESULTS + '/' + TEAM_NAME + "_" + TASK + "_" + name + '.csv')
        return data
    except FileNotFoundError:
        pass


def create_all_csvs() -> None:
    for file in NAMES_CSV:
        path_to_save = os.path.join(PATH_TO_RESULTS, f"{TEAM_NAME}_{TASK}_{file}.csv")
        match file:
            case "META":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "NAZWA_PLIKU"]).to_csv(path_to_save, index=False)
            case "BAGOFWORDS_S":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save,
                                                                                                    index=False)
            case "BAGOFWORDS_N":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "SLOWO", "LICZBA_WYSTAPIEN"]).to_csv(path_to_save,
                                                                                                    index=False)
            case "WYRAZENIA":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "WYRAZENIE", "FLAGA_WYSTAPIENIA"]).to_csv(path_to_save,
                                                                                                         index=False)
            case "DANE":
                pd.DataFrame(columns=["ID_KIID", "ID_ZESPOLU", "ISIN", "IDENTYFIKATOR_KRAJOWY",
                                      "NUMER_RFI", "DATA_AKTUALIZACJI_KIID", "KATEGORIE_JEDNOSTEK_UCZESTNICTWA",
                                      "CZESTOTLIWOSC_ZBYWANIA_I_ODKUPOWANIA_JEDNOSTEK_UCZESTNICTWA",
                                      "CZY_FUNDUSZ_WYPLACA_DYWIDENDE", "BENCHMARK",
                                      "PROFIL_RYZYKA_I_ZYSKU", "SRRI",
                                      "FUND_TYPE"]).to_csv(path_to_save, index=False)
            case _:
                raise ValueError("Wrong value")


if __name__ == '__main__':
    create_all_csvs()
