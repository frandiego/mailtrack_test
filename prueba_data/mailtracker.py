import pandas as pd

from .transformer import Transfomer


class MailTrackDataTest(Transfomer):

    def pregunta_1(self) -> pd.DataFrame:
        # active user by month, 0 if no active users, order by yearmonth descending
        df = self.unique_months.merge(self.monthly_active_users, how='left').fillna(0)
        return df.sort_values('yearmonth', ascending=False)

    def pregunta_2(self, month: str = '2021-04') -> pd.DataFrame:
        # number active users per domain in a given month, return only those with max active users
        df = self.monthly_connections.query(f"connections >= {self.min_active_connections} & yearmonth == '{month}'")
        df = df.merge(self.users).groupby(['yearmonth', 'domain'], as_index=False).agg(
            active_users=('user_id', 'nunique'))
        return df[df['active_users'] == max(df['active_users'])]

    def pregunta_3(self) -> pd.DataFrame:
        # countries with no active users per months in a flat column concatenated by comma
        df = self.monthly_active_users_by_country.query('active_users<1')
        df = df.groupby('yearmonth', as_index=False)
        df = df.agg(countries=('country_name', lambda i: ','.join(list(set(i)))))
        df['countries'] = df['countries'].astype(str)
        return df.sort_values('yearmonth', ascending=False)

    def pregunta_4(self) -> pd.DataFrame:
        # growth rate of active users per month and country (all months and countries)
        df = self.monthly_active_users_by_country.sort_values(['country_name', 'yearmonth']).reset_index(drop=True)
        df['pct_change'] = df.groupby(['country_name'])['active_users'].pct_change().round(3) * 100
        return df.sort_values(['country_name', 'yearmonth'], ascending=[True, False])

    def pregunta_5(self, top: int = 10) -> pd.DataFrame:
        # last 10 users connections by country order by country and time
        df = self.connections.merge(self.users)
        df['rank'] = df.groupby(['country_id'])['timestamp'].rank(ascending=False)
        df = df[df['rank'] <= top][['email', 'country_name', 'timestamp']]
        return df.sort_values(['country_name', 'timestamp'], ascending=[True, False])
