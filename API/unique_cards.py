import glob
import json
import re
from typing import cast, Dict, List, TypedDict, Union

import numpy as np
from numpy.typing import NDArray
import pandas as pd

def add_derivates_to_round(df: pd.DataFrame) -> None:
    """ Add derivative columns to history DataFrame.
    Args:
        df (pandas DataFrame): Full round history.
    """
    # to apply this to the whole of all data, use groupby 'round'?
    df['sum'] = df.loc[:, df.columns.str.startswith('result_')].sum(axis=1)

    df['%'] = df['sum'] / (len(df)-1) / 6 * 100

    # has to be done after computing '%'
    if 'bonus' in df.columns:  # e.g. round 65
        df['sum'] = df['sum'] + df['bonus']

    if df.at[0, 'round'] in [75, 79]:  # least points win
        ascending = True
    else:
        ascending = False

    df['place'] = df['sum'].rank(method='min', ascending=ascending).astype(int)
    if df.at[0, 'round'] >= 30:  # introduction of tiebreaker rule in round 30
        for pl in df['place'].unique():
            indices = df.index[df['place'] == pl]
            row_sums = df.loc[indices, [f"result_{idx}" for idx in indices]].sum(axis=1)
            ranks = row_sums.rank(method='min', ascending=ascending).astype(int)
            df.loc[indices, 'place'] = ranks + pl - 1


def validate_results(df: pd.DataFrame) -> bool:
    """Validate the results columns in a Dataframe containing one or multiple rounds.
    Args:
        df (pd.DataFrame): _description_
    Returns:
        bool: Is / are the results table(s) consistent?
    """
    # possible results: 6-0, 4-1, 3-3, ...
    valid_results = {(0, 6), (6, 0),
                     (1, 4), (4, 1),
                     (2, 2), (3, 3)}

    is_valid = True
    for round_number, round_data in df.groupby('round'):
        res_table = round_data.loc[:, round_data.columns.str.startswith(
            'result_')].to_numpy()

        if res_table.shape[0] != res_table.shape[1]:  # should be square
            print(f"Error in results ({round_number}): not square.")
            return False

        for i in range(res_table.shape[0]):
            for j in range(i+1, res_table.shape[1]):
                if (res_table[i, j], res_table[j, i]) not in valid_results:
                    print(
                        f"Error in results ({round_number}): "
                        f"{i + 1} {j + 1}: {res_table[i, j]}-{res_table[j, i]}"
                    )
                    is_valid = False

    return is_valid


def load_data() -> pd.DataFrame:
    """ Load full raw dataset from the individual csv files to a single pandas
        DataFrame.
    """
    data_cumu = pd.DataFrame()
    for file in glob.glob('data/raw/round_*.csv'):
        data = pd.read_csv(file, sep=';')
        if validate_results(data):
            add_derivates_to_round(data)
            data_cumu = pd.concat([data_cumu, data])

    return data_cumu


def unique_across_columns(group):
    # Flatten the values from all target columns and take unique ones
    card_columns = [col for col in group.columns if col.startswith('card_')]
    return pd.unique(group[card_columns].values.ravel())

if __name__ == '__main__':
    data = load_data()

    res = data.groupby('player').apply(unique_across_columns).reset_index(name='unique_cards')
    res['num_unique_cards'] = res['unique_cards'].apply(len)
    print(res)
