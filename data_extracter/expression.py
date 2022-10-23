from enum import Enum


class Rule(Enum):
    # (matching sentence - different cases)
    NEAR_NEIGHBOURHOOD = 5,
    STRICTER_NEAR_NEIGHBOURHOOD = 3,
    WHOLE_STRING = 100
    SENTENCE_AFTER = -1


class ExpressionsToFind(Enum):
    ISIN = ('ISIN', "(\s|^)([\dA-Z]{12})(\s|\.)", Rule.NEAR_NEIGHBOURHOOD),
    RFI = ('RFI', "(\s|^)([\dA-Z]{11})(\s|\.)", Rule.WHOLE_STRING),
    COUNTRY_IDENTIFIER = ('identyfikator krajowy', "\s([0-9]{3,4})(\s|\.)", Rule.NEAR_NEIGHBOURHOOD),
    ACTUALIZATION_DATE = ('data aktualizacji', "((\d{2}-\d{2}-\d{4}) | \d{2}\.\d{2}\.\d{4})", Rule.NEAR_NEIGHBOURHOOD),
    CATEGORY = ("kategoria", "(\s|^)((ABCD){1})(\s|\.)", Rule.STRICTER_NEAR_NEIGHBOURHOOD),
    FREQUENCY = ("czestotliwosc zbywania i odkupowania", "((\b(miesieczny|M)\b)|(\b(dzienny|D)\b)|\b((kwartal|Q))\b|\b(tygodniowy|W)\b)", Rule.NEAR_NEIGHBOURHOOD),
    DIVIDEND = ("czy wypłaca diwidende", None, True),
    BENCHMARK = ("benchmark", "benchmark(.*?)\.", Rule.SENTENCE_AFTER),
    ADVISED_PERIOD_INVESTMENT = ("zalecany okres inwestycji", None, Rule.NEAR_NEIGHBOURHOOD),  # need to implement custom logic
    RISK_PROFIT_PROFILE = ("profil ryzyka i zysku", "Profil ryzyka i zysku(.*)(.*?)", Rule.WHOLE_STRING),
    SRRI = ("SRRI", None, Rule.WHOLE_STRING),
    FUND_TYPE = ("typ funduszu", "(\s|^)(SFIO)\s", Rule.WHOLE_STRING)
