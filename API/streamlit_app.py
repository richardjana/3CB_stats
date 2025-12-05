from glob import glob

import pandas as pd
import plotly.graph_objects as go
from natsort import natsorted, ns
import streamlit as st


st.title('PvP match history')

@st.cache_data
def load_data() -> tuple[pd.DataFrame, list[str]]:
    def get_transform_round_df(csv_file: str) -> pd.DataFrame:
        """ Get df for a single ronud and transform to match-centric format. """
        df = pd.read_csv(csv_file, sep=';')

        round = df['round'].iloc[0]
        df = df.drop('round', axis=1)
        df = df.drop([col for col in df.columns if col.startswith('card_')], axis=1)

        player_dict = dict(zip([col for col in df.columns if col.startswith('result_')],
                               df['player'].tolist()))
        df = df.rename(columns=player_dict)

        df_long = df.melt(id_vars='player', var_name='opponent', value_name='points_player')
        df_long = df_long[df_long['player'] != df_long['opponent']]

        df_matches = df_long.merge(df_long,
                                   left_on=['player', 'opponent'],
                                   right_on=['opponent', 'player'],
                                   suffixes=('_1', '_2'))
        df_matches = df_matches.drop(['opponent_1', 'opponent_2'], axis=1)
        df_matches['round'] = round

        return df_matches

    round_dfs = []
    for csv in natsorted(glob('../API/data/raw/round_*.csv')):
        round_dfs.append(get_transform_round_df(csv))

    data = pd.concat(round_dfs)
    all_players = natsorted(data['player_1'].unique(), alg=ns.IGNORECASE)

    return data, all_players

data, all_players = load_data()


p1 = st.selectbox('player 1', all_players)
p2 = st.selectbox('player 2', all_players)

def filter_data(df: pd.DataFrame, player: str, opponent: str) -> pd.DataFrame:
    filtered_df = df[(df['player_1'] == player) & (df['player_2'] == opponent)]

    return filtered_df

def convert_to_ohlc_series(df: pd.DataFrame) -> pd.DataFrame:
    cumsum = df[['points_player_1', 'points_player_2']].cumsum()
    df['cumulative_score'] = cumsum['points_player_1'] - cumsum['points_player_2']

    df['open'] = df['cumulative_score'].shift(1)
    df['close'] = df['cumulative_score']
    df['high'] = df[['open', 'close']].max(axis=1)
    df['low'] = df[['open', 'close']].min(axis=1)

    df = df.fillna(0)  # start at 0

    return df

p1_p2_df = filter_data(data, p1, p2)
ohlc = convert_to_ohlc_series(p1_p2_df)

fig = go.Figure(data=[go.Candlestick(x=ohlc['round'],
                open=ohlc['open'],
                high=ohlc['high'],
                low=ohlc['low'],
                close=ohlc['close'])])

st.plotly_chart(fig, use_container_width=True)
