from typing import List, Tuple

import pandas as pd
import plotly.graph_objects as go
from natsort import natsorted, ns
import streamlit as st


st.title('PvP match history')

@st.cache_data
def load_data() -> Tuple[pd.DataFrame, List[str]]:
    data = pd.read_csv('match_data.csv', sep=';')
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
