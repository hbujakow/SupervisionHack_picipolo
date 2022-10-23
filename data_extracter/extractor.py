from data_extracter.expression import ExpressionsToFind
from typing import List
import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.utils import TEAM_NAME, TASK, TEAM_ID,  read_data, export_data, Name

class DataExtractor:
    def __init__(self):
        pass

    def update_csv_file(self, textFile: str, primary_key: int) -> None:
        # original = pd.read_csv(f'./results/{TEAM_NAME}_{TASK}_DANE.csv')
        original = read_data(Name.DANE.value)
        df = self.__extractExpressions(textFile, original.columns, primary_key)
        original = pd.concat([original, df])
        export_data(original, Name.DANE.value)
        # original.to_csv(f'../results/{TEAM_NAME}_{TASK}_DANE.csv', index=False)

    def __extractExpressions(self, textFile: str, columns: List[str], primary_key: int) -> pd.DataFrame:
        results = [primary_key, TEAM_ID]
        for expression in ExpressionsToFind:
            for tag, way_to_handle, rule in expression.value:
                match way_to_handle:
                    case isinstance(str):
                        if tag in text:
                            words = text.split(' ')
                            idx_of_tag = words.index(tag)

                            match rule:
                                case Rule.WHOLE_STRING:
                                    if tag in ['RFI', 'profil_ryzyka i zysku', "benchmark"]:
                                        found = re.search(way_to_handle, text)
                                        if found:
                                            results.append(text[found.start():found.end()])
                                        else:
                                            results.append(None)
                                    elif tag == 'profil ryzyka i funduszu':
                                        found_SFIO = re.search(way_to_handle, text)
                                        if found_SFIO:
                                            results.append(text[found_SFIO.start():found.end()])
                                        elif re.search( r"(\b|^)(FIO)\b"):
                                            results.append(text[re.search( r"(\b|^)(FIO)\b").start():re.search( r"(\b|^)(FIO)\b").end()])                           
                                        else:
                                            results.append(None)
                                case Rule.NEAR_NEIGHBOURHOOD:
                                    start_idx = idx_of_tag - Rule.NEAR_NEIGHBOURHOOD.value if (idx_of_tag - Rule.NEAR_NEIGHBOURHOOD.value) > 0 else 0
                                    end_idx = idx_of_tag + Rule.NEAR_NEIGHBOURHOOD if (idx_of_tag + Rule.NEAR_NEIGHBOURHOOD) <= len(words) - 1 else len(words) - 1
                                    subtext = ' '.join(words[start_idx:end_idx])
                                    found = re.search(way_to_handle, subtext)
                                    if found:
                                        results.append(subtext[found.start():found.end()])
                                    else:
                                        results.append(None)
                                case Rule.STRICTER_NEAR_NEIGHBOURHOOD:
                                    start_idx = idx_of_tag - Rule.STRICTER_NEAR_NEIGHBOURHOOD.value if (idx_of_tag - Rule.STRICTER_NEAR_NEIGHBOURHOOD.value) > 0 else 0
                                    end_idx = idx_of_tag + Rule.STRICTER_NEAR_NEIGHBOURHOOD if (idx_of_tag + Rule.STRICTER_NEAR_NEIGHBOURHOOD) <= (len(words) - 1) else (len(words) - 1)
                                    subtext = ' '.join(words[start_idx:end_idx])
                                    found = re.search(way_to_handle, subtext)
                                    if found:
                                        results.append(subtext[found.start():found.end()])
                                    else:
                                        results.append(None)
                    case None:
                        if tag == 'czy wypłaca diwidende':
                            found = re.search(r'\b(dywidend)(\b|\.)')
                            if found:
                                start_idx = idx_of_tag - Rule.NEAR_NEIGHBOURHOOD.value if (idx_of_tag - Rule.NEAR_NEIGHBOURHOOD.value) > 0 else 0
                                end_idx = idx_of_tag + Rule.STRICTER_NEAR_NEIGHBOURHOOD if (idx_of_tag + Rule.STRICTER_NEAR_NEIGHBOURHOOD) <= (len(words) - 1) else (len(words) - 1)
                                subtext = ' '.join(words[start_idx:end_idx])
                                if re.rearch(r'\b(nie)\b'):
                                    results.append(False)
                                else:
                                    results.append(True)
                    case _:
                        raise Error("Invalid way to handle expressions")
        return pd.DataFrame([result], columns=columns)



