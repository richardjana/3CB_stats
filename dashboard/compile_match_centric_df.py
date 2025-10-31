from glob import glob

from natsort import natsorted
import pandas as pd

def get_transform_round_df(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file, sep=';')

    round = df['round'].iloc[0]
    df = df.drop('round', axis=1)
    df = df.drop([col for col in df.columns if col.startswith('card_')], axis=1)

    player_dict = dict(zip([col for col in df.columns if col.startswith('result_')], df['player'].tolist()))
    df = df.rename(columns=player_dict)

    df_long = df.melt(id_vars='player', var_name='opponent', value_name='points_player')
    df_long = df_long[df_long['player'] != df_long['opponent']]

    df_matches = df_long.merge(df_long, left_on=['player', 'opponent'], right_on=['opponent', 'player'], suffixes=('_1', '_2'))
    df_matches = df_matches.drop(['opponent_1', 'opponent_2'], axis=1)
    df_matches['round'] = round

    return df_matches

round_dfs = []
for csv in natsorted(glob('../API/data/raw/round_*.csv')):
    round_dfs.append(get_transform_round_df(csv))

match_data = pd.concat(round_dfs)
match_data.to_csv('match_data.csv', sep=';', index=False)
