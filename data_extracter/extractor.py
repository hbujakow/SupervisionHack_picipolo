from expression import ExpressionsToFind
from typing import List
import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import TEAM_NAME, TASK

class DataExtractor:
    def __init__(self):
        pass

    def update_csv_file(self, textFile: str, ) -> None:
        original = pd.read_csv(f'../results/{TEAM_NAME}_{TASK}_DANE.csv')
        df = self.__extractExpressions(textFile, original.columns)
        original = pd.concat([original, df])
        original.to_csv(f'../results/{TEAM_NAME}_{TASK}_DANE.csv', index=False)

    def __extractExpressions(self, textFile: str, columns: List[str]) -> pd.DataFrame:
        results = []
        for expression in ExpressionsToFind:
            for tag, way_to_handle, rule in expression.value[0]:
                match way_to_handle:
                    case !None:
                        if tag in text:
                            words = text.split(' ')
                            idx_of_tag = words.index(tag)
                            match rule:
                                case Rule.WHOLE_STRING:
                                    
                                
                    case None:
                        
                    case _:
                        raise Error("Invalid way to handle expressions")
                    
                    
                    
        return pd.DataFrame([result], columns=columns)
                    # case "ISIN":
                    #     pass
                    # case "RFI":
                    #     pass
                    # case "identyfikator krajowy":
                    #     pass
                    # case "data aktualizacji":
                    #     pass
                    # case "kategoria":
                    #     pass
                    # case "czestotliwosc zbywania i odkupowania":
                    #     pass
                    # case "czy wypłaca diwidende":
                    #     pass
                    # case "benchmark":
                    #     pass
                    # case "zalecany okres inwestycji":
                    #     pass
                    # case "profil ryzyka i zysku":
                    #     pass

    def cokolwiek(self):
        for e in WHAT_TO_FIND:
            print(e.value[0])
            print()

DataExtractor().cokolwiek()

