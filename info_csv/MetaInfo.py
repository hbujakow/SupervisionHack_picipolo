import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import TEAM_NAME, TEAM_ID, TASK

class MetaInfo:
    def __init__(self):
        pass

    def update_csv_file(filename: str, primary_key: int) -> None:
        original = pd.read_csv(f'../results/{TEAM_NAME}_{TASK}_META.csv')
        df = pd.DataFrame([[TEAM_NAME, primary_key, filename]], columns=original.columns)
        original = pd.concat([original, df])
        original.to_csv(f'../results/{TEAM_NAME}_{TASK}_META.csv', index=False)