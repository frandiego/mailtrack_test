import pandas as pd

from .controller import Controller


class Transfomer(Controller):
    min_active_connections = 2

    def __init__(self, connections_path: str, users_path: str, countries_paths: str):
        self.connections = self._read_connections(connections_path)
        self.countries = self._read_countries(countries_paths)
        self.users = self._read_users(users_path)
        self.unique_months = self._unique_months()
        self.monthly_connections = self._monthly_connections()
        self.monthly_active_users_by_country = self._monthly_active_users_by_country()
        self.monthly_active_users = self._monthly_active_users()

    def _read_connections(self, path: str) -> pd.DataFrame:
        # read and clean user_connections.csv
        df = self._read_csv(path)
        df['yearmonth'] = df['timestamp'].map(lambda i: i[:7]).astype(str)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df[['timestamp', 'yearmonth', 'user_id']].sort_values('timestamp')

    def _read_countries(self, path: str) -> pd.DataFrame:
        # read and clean countries.csv
        return self._read_csv(path).rename(columns={'id': 'country_id', 'name': 'country_name'})

    def _read_users(self, path: str) -> pd.DataFrame:
        # read and clean users.csv
        df = self._read_csv(path)
        df['domain'] = df['email'].map(lambda i: i.split('@')[1].strip())
        df = df.merge(self.countries, how='left')
        df.rename(columns={'id': 'user_id'}, inplace=True)
        return df[['user_id', 'country_id', 'email', 'domain', 'country_name']]

    def _unique_months(self, column_name: str = 'yearmonth') -> pd.DataFrame:
        # unroll time of column names and create a dataframe with unique months and yearmonth
        return pd.DataFrame(self._unroll_time(self.connections['timestamp'], '%Y-%m'), columns=[column_name])

    def _monthly_connections(self) -> pd.DataFrame:
        # number of connections by yearmonth, and user_id
        df = self.connections.groupby(['yearmonth', 'user_id'], as_index=False).size()
        return df.rename(columns={'size': 'connections'}).sort_values(['yearmonth', 'user_id'])

    def _monthly_active_users_by_country(self) -> pd.DataFrame:
        # add all country and months and compute unique users (active users)
        df = self.monthly_connections.query(f'connections>={self.min_active_connections}')
        df = df.merge(self.users).groupby(['yearmonth', 'country_name'], as_index=False)
        df = df.agg(active_users=('user_id', 'nunique'))
        df_countries = self._cross_product(self.unique_months, self.countries[['country_name']])
        df = df_countries.merge(df, how='left').fillna(0)
        df['active_users'] = df['active_users'].astype(int)
        return df

    def _monthly_active_users(self) -> pd.DataFrame:
        # active users by month and country and group by month
        df = self.monthly_active_users_by_country.copy()
        return df.groupby(['yearmonth'], as_index=False).agg(active_users=('active_users', 'sum'))
