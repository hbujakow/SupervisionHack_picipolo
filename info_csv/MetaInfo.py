import pandas as pd
import os, sys

from main import TEAM_NAME, Name, export_data, read_data

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MetaInfo:
    def __init__(self):
        pass

    def update_csv_file(filename: str, primary_key: int) -> None:
        original = read_data(Name.META.value)
        df = pd.DataFrame([[TEAM_NAME, primary_key, filename]], columns=original.columns)
        original = pd.concat([original, df])
        export_data(original, Name.META.value)
