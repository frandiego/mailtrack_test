import logging
import os

import pandas as pd


class Controller:
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    @classmethod
    def _read_csv(cls, path: str):
        # read csv safely
        if not os.path.exists(path):
            cls.logger.error(f'Path {path} does not exist')
        return pd.read_csv(path)

    @staticmethod
    def _unroll_time(times: pd.Series, time_format: str) -> pd.Series:
        # from a series or list of strings (time format) or datetime,
        # generates a time-ordered series of unique values according to the given format
        date_times = pd.to_datetime(times)
        date_range = pd.date_range(date_times.min().date(), date_times.max().date())
        return pd.Series(list(set(map(lambda i: format(i, time_format), date_range))))

    @staticmethod
    def _cross_product(dfa: pd.DataFrame, dfb: pd.DataFrame, auxiliar_column: str = '__key') -> pd.DataFrame:
        # cross product in data frame, (some pandas version has not implemented)
        dfa[auxiliar_column] = dfb[auxiliar_column] = 0
        cross_product = dfa.merge(dfb, on=auxiliar_column, how='outer')
        dfa.drop([auxiliar_column], axis=1, inplace=True)
        dfb.drop([auxiliar_column], axis=1, inplace=True)
        return cross_product.drop([auxiliar_column], axis=1)
