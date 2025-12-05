from glob import glob
import json

import pandas as pd
import plotly.graph_objects as go
from natsort import natsorted, ns
import streamlit as st


@st.cache_data
def load_match_data() -> tuple[pd.DataFrame, list[str]]:
    """ Load the full match history from raw round data.
    Returns:
        tuple[pd.DataFrame, list[str]]: Match-centric DataFrame and list of all players.
    """
    def get_transform_round_df(csv_file: str) -> pd.DataFrame:
        """ Get df for a single ronud and transform to match-centric format. """
        df = pd.read_csv(csv_file, sep=';')

        round_number = df['round'].iloc[0]
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
        df_matches['round'] = round_number

        return df_matches

    round_dfs = []
    for csv in natsorted(glob('data/raw/round_*.csv')):
        round_dfs.append(get_transform_round_df(csv))

    data = pd.concat(round_dfs)
    all_players = natsorted(data['player_1'].unique(), alg=ns.IGNORECASE)

    return data, all_players

def convert_to_ohlc_series(df: pd.DataFrame) -> pd.DataFrame:
    """ Convert the match history into OHLC (open, high, low, close) format for plotting.
    Args:
        df (pd.DataFrame): Full match data.
    Returns:
        pd.DataFrame: OHLC DataFrame, ready for plotting.
    """
    cumsum = df[['points_player_1', 'points_player_2']].cumsum()
    df['cumulative_score'] = cumsum['points_player_1'] - cumsum['points_player_2']

    df['open'] = df['cumulative_score'].shift(1)
    df['close'] = df['cumulative_score']
    df['high'] = df[['open', 'close']].max(axis=1)
    df['low'] = df[['open', 'close']].min(axis=1)

    df = df.fillna(0)  # start at 0

    return df

@st.cache_data
def load_elo_data() -> pd.DataFrame:
    """ Load ELO ratings for all players.
    Returns:
        pd.DataFrame: Ready for plotting.
    """
    def read_player_json(f_name) -> list[float]:
        """ Extract the raw data from player json files. """
        with open(f_name, 'r', encoding='utf-8') as file:
            json_dict = json.load(file)
        return json_dict['elo_list']

    elo_data = {}
    for json_file in glob('data/players/*.json'):
        player_name = json_file.split('/')[-1][:-5]
        elo_data[player_name] = read_player_json(json_file)

    elo_data['round'] = list(range(1, len(elo_data[player_name])+1))

    return pd.DataFrame(elo_data)

def make_versus_plot(df: pd.DataFrame, p1: str, p2: str) -> go.Figure:
    """ Prepare the PvP plot, showing the match history between two players.
    Args:
        df (pd.DataFrame): Full data of all matches.
        p1 (str): Name of player 1.
        p2 (str): Name of the opponent.
    Returns:
        go.Figure: Figure to show.
    """
    p1_p2_df = df[(df['player_1'] == p1) & (df['player_2'] == p2)]
    ohlc = convert_to_ohlc_series(p1_p2_df)

    fig = go.Figure(data=[go.Candlestick(x=ohlc['round'],
                    open=ohlc['open'],
                    high=ohlc['high'],
                    low=ohlc['low'],
                    close=ohlc['close'])])

    return fig

def make_elo_plot(df: pd.DataFrame, p1: str, p2: str) -> go.Figure:
    """ Prepare the ELO plot, comparing the history of 2 players.
    Args:
        df (pd.DataFrame): Full data for all players.
        p1 (str): Name of player 1.
        p2 (str): Name of player 2.
    Returns:
        go.Figure: Figure to show.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['round'],
                             y=df[p1],
                             mode='lines',
                             name=p1,
                             line={'color': 'green'}))

    fig.add_trace(go.Scatter(x=df['round'],
                             y=df[p2],
                             mode='lines',
                             name=p2,
                             line={'color': 'red'}))

    fig.update_layout(xaxis_title='Round',
                      yaxis_title='ELO rating',
                      legend={'yanchor': 'top', 'y': 0.99, 'xanchor': 'left', 'x': 0.01})

    return fig


pvp_data, all_players = load_match_data()
elo_data = load_elo_data()

st.title('3-card-blind statistics')
p1 = st.selectbox('player', all_players)
p2 = st.selectbox('opponent', all_players)

st.header('PvP match history')
st.plotly_chart(make_versus_plot(pvp_data, p1, p2), use_container_width=True)

st.header('ELO rating')
st.plotly_chart(make_elo_plot(elo_data, p1, p2), use_container_width=True)
