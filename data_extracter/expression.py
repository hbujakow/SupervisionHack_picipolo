from enum import Enum


class Rule(Enum):
    # (matching sentence - different cases)
    NEAR_NEIGHBOURHOOD = 5
    STRICTER_NEAR_NEIGHBOURHOOD = 3
    WHOLE_STRING = 100


class ExpressionsToFind(Enum):
    ISIN = ('ISIN', r"(\s|^)([\dA-Z]{12})(\s|\.)", Rule.NEAR_NEIGHBOURHOOD)
    RFI = ('RFI', r"(\s|^)([\dA-Z]{11})(\s|\.)", Rule.WHOLE_STRING)
    COUNTRY_IDENTIFIER = ('identyfikator krajowy', r"\s([0-9]{3,4})(\s|\.)", Rule.NEAR_NEIGHBOURHOOD)
    ACTUALIZATION_DATE = ('data aktualizacji', r"((\d{2}-\d{2}-\d{4}) | \d{2}\.\d{2}\.\d{4})", Rule.NEAR_NEIGHBOURHOOD)
    CATEGORY = ("kategoria", r"(\s|^)((ABCD){1})(\s|\.)", Rule.STRICTER_NEAR_NEIGHBOURHOOD)
    FREQUENCY = ("czestotliwosc zbywania i odkupowania", r"((\b(miesieczny|M)\b)|(\b(dzienny|D)\b)|\b((kwartal|Q))\b|\b(tygodniowy|W)\b)", Rule.NEAR_NEIGHBOURHOOD)
    DIVIDEND = ("czy wypłaca diwidende", None, Rule.NEAR_NEIGHBOURHOOD)
    BENCHMARK = ("benchmark", r"benchmark(.*?)\.", Rule.WHOLE_STRING)
    # # ADVISED_PERIOD_INVESTMENT = ("zalecany okres inwestycji", None, Rule.NEAR_NEIGHBOURHOOD),  # need to implement custom logic
    RISK_PROFIT_PROFILE = ("profil ryzyka i zysku", r"Profil ryzyka i zysku(.*)(.*?)", Rule.WHOLE_STRING)
    SRRI = ("SRRI", r"\b[1-7]\b", Rule.NEAR_NEIGHBOURHOOD)
    FUND_TYPE = ("typ funduszu", r"(\b|^)(SFIO)\b", Rule.WHOLE_STRING)
