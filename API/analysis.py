import glob
import json
import numpy as np
from numpy.typing import NDArray
import pandas as pd
import re
from typing import Dict, List, Tuple, Union

# consume all the raw data and prepare info ready to serve for the API
    # hall of fame
    # players
    # rounds

# plotting ideas:
    # popularity of certain cards over time? (fixed / user inputs cards)

#Pro runde:
#Regeln?, decks, Ergebnisse, Link zum thread

# calculate derivatives per round (sum of points, % of max points, place)
def add_derivates_to_round(df: pd.DataFrame) -> None:
    """ Add derivative columns to history DataFrame.
    Args:
        df (pandas DataFrame): Full round history.
    """
    # to apply this to the whole of all data, use groupby 'round'?
    df['sum'] = df.loc[:,df.columns.str.startswith('result_')].sum(axis=1)
    if 'bonus' in df.columns: # e.g. round 65
        df['sum'] = df['sum'] + df['bonus']

    df['%'] = df['sum'] / (sum(df.columns.str.startswith('result_'))-1) / 6 * 100

    df['place'] = df['sum'].map(lambda s: sum(df['sum']>s)+1)
    # not accounting for the tie breaker. rule since when? round 30?

# calculate global derivates (most played card per player)
def most_played_cards(df: pd.DataFrame) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    """ Find the most-played cards for all players and overall from a pandas
        DataFrame.
    Args:
        df (pandas DataFrame): History of rounds played, with 'player' and
            'card_*' columns.
    Return:
        Dictionary with a list of popular cards for each player and overall.
    """

    unique_cards = df.loc[:, df.columns.str.startswith('card_')].stack().dropna().value_counts()
    mp_cards = {'overall': [{'card': c, 'count': int(n), '%': n/sum(unique_cards.values)*100} for c, n in zip(unique_cards.index, unique_cards.values)]}
    mp_cards['overall'].sort(key = lambda cc: (-cc['count'], cc['card']))

    for player, player_data in df.groupby('player'):
        all_cards = player_data.loc[:, player_data.columns.str.startswith('card_')]

        unique_cards = all_cards.stack().dropna().value_counts()

        mp_cards[player] = [{'card': c, 'count': int(n), '%': n/sum(unique_cards.values)*100} for c, n in zip(unique_cards.index, unique_cards.values)]
        mp_cards[player].sort(key = lambda cc: (-cc['count'], cc['card']))

    return mp_cards

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
        res_table = round_data.loc[:, round_data.columns.str.startswith('result_')].to_numpy()

        if res_table.shape[0] != res_table.shape[1]: # should be square
            print(f"Error in results ({round_number}): not square.")
            return False

        for i in range(res_table.shape[0]):
            for j in range(i+1, res_table.shape[1]):
                if (res_table[i,j], res_table[j,i]) not in valid_results:
                    print(f"Error in results ({round_number}): {i+1} {j+1}: {res_table[i,j]}-{res_table[j,i]}")
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

# find the strongest opponents for a player (top n)
def find_nemesis(df: pd.DataFrame, player: str, n: int =5) -> List[Dict[str, Union[str, float, int]]]:
    """
    Args:
        df (pandas DataFrame): Full match history; 'round', 'player' and
            'result_*' columns.
        player (string): Name of the player.
        n (int): Number of opponents to be returned.
    Return:
        Sorted list of opponents, each as a dictionary with name of the opponent,
        aggregate score and number of matches played.
    """
    data_dict: Dict[str, NDArray[np.int_]] = {}
    for round_data in df.groupby('round', group_keys=False):
        player_names = round_data[1]['player'].to_list()
        results = round_data[1].dropna(axis=1)
        results = results.loc[results['player']==player]
        try: # not everyone in every round
            results = results.loc[:,results.columns.str.startswith('result_')].to_numpy()[0,:]
            for p, r in zip(player_names, results):
                try:
                    data_dict[p][int(r)] += 1
                except:
                    data_dict[p] = np.zeros(7, dtype=int)
                    data_dict[p][int(r)] += 1
        except:
            pass

    del data_dict[player] # remove the target player

    for p in data_dict: # [score, times played]
        data_dict[p] = [np.dot(data_dict[p], [-6,-3,0,0,3,0,6])/np.sum(data_dict[p]), np.sum(data_dict[p])] # [-2,-1,0,0,1,0,2]

    data = [{'player': p, 'score': data_dict[p][0], 'n_matches': int(data_dict[p][1])} for p in data_dict]
    data.sort(key = lambda d: (d['score'], -d['n_matches']))

    return data[:n]

def get_scores(df: pd.DataFrame) -> Dict[str, Dict[str, Union[float, List[Dict[int, float]]]]]:
    """ From pandas DataFrame with the complete history, compute scores for
        every player in terms of % of the possible points in every round.
    Args:
        Pandas DataFrame with 'player', 'round' and '%' columns.
    Return:
        Dictionary of player names, for each a dictionary with the average,
        total and list of scores.
    """

    # aggregated score => a more pandas way to do this?
    #datagroup = data.groupby('player')['%'].agg(['mean', 'sum'])

    scores = {}
    for player, player_data in data[['player', 'round', '%']].groupby('player'):
        scores[player] = {'average': player_data['%'].mean(),
                          'total': player_data['%'].sum(),
                          'list': [{'round': int(sl[1]), 'score': sl[2]} for sl in player_data.to_numpy().tolist()]}
        scores[player]['list'].sort(key = lambda d: d['round'])

    return scores

def compute_Elo_scores(df: pd.DataFrame) -> List[Dict[str, float]]:
    """ Compute Elo ratings for all players, based on history from a pandas
        DataFrame.
    Args:
        Pandas DataFrame with 'player', 'round' and 'result_*' columns.
    Return:
        List of dictionaries with Elo scores for every player for all rounds
        (chronological) .
    """

    def expected_score(rating_opponent: float, rating_player: float) -> float:
        """ Expected score, given the ratings of the opponents, to be compared
            with the actual result of the match.
        Args:
            Elo ratings of the two opponents of a match. (both float)
        Return:
            Expected result of the match. (float)
        """
        return 1 / (1 + 10**((rating_opponent-rating_player)/512))

    start_Elo = 1600
    update_factor = 8

    # initialize list with start_Elo for all players in data "state before the first round"
    Elo = [{player: start_Elo for player in df['player'].unique()}]

    # iterate through rounds to update the scores
    for round, round_data in df.groupby('round'):
        player_list = round_data['player'].to_list()
        results = round_data.loc[:, round_data.columns.str.startswith('result_')].to_numpy()
        results = results[:results.shape[0], :results.shape[0]] # round 65 has additional column 'bonus'
        np.fill_diagonal(results, 1) # fix diagonal values (also important for self vs. self!)
        results = results / (results + results.T) # scale results as score

        update = Elo[-1].copy()
        for player in player_list:
            index = player_list.index(player)
            for opponent in player_list: # also compares each player to themselves, but that's ok
                result = results[index, player_list.index(opponent)]
                update[player] += update_factor * (result - expected_score(Elo[-1][opponent], Elo[-1][player]))

        Elo.append(update)

    return Elo

def count_rounds(df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    """ From a history DataFrame, extract the numbers of rounds each player has played / won.
    Args:
        df (pandas DataFrame): 'player' and 'place' columns.
    Return:
        Dictionary, for each player a dictionary with number of rounds played
        and number of rounds won.
    """
    rounds_played_won = {}
    for player, player_data in data[['player', 'place']].groupby('player'):
        rounds_played_won[player] = {'played': len(player_data),
                                     'won': int(np.sum(player_data['place'] == 1))} # int64 vs JSON

    return rounds_played_won

if __name__ == '__main__':
    data = load_data()

    all_players = data['player'].unique()
    Elo = compute_Elo_scores(data)
    scores = get_scores(data)
    rounds_played_won = count_rounds(data)
    mp_cards = most_played_cards(data)

    with open('data/popular_cards.json', 'w', encoding='utf-8') as file:
        json.dump(mp_cards['overall'][:50], file, ensure_ascii=False, indent=4)

    ### prepare list of all players and round numbers ###
    all_players_sorted = all_players.tolist()
    all_players_sorted.sort(key = lambda p: re.sub(r'[^a-zA-Z0-9]', '', p).lower())
    round_numbers_sorted = sorted(data['round'].unique().tolist(), key = lambda x: -x)
    with open('data/players_rounds_lists.json', 'w', encoding='utf-8') as file: # possibly also with pandas.DataFrame.to_json (?)
        json.dump({'player_names': all_players_sorted, 'round_numbers': round_numbers_sorted}, file, ensure_ascii=False, indent=4)

    ### prepare hall of fame data ###
    table_data = [{'player': p,
                   'score_mean': f"{scores[p]['average']:.2f}",
                   'score_sum': f"{scores[p]['total']:.2f}",
                   'rounds_played': rounds_played_won[p]['played'],
                   'wins': rounds_played_won[p]['won'],
                   'elo': f"{Elo[-1][p]:.2f}"
                  } for p in all_players]

    # winners of every round (a round can have multiple winners)
    round_winners_df = data[['place', 'round', 'player']].loc[data['place']==1].groupby('round')['player'].aggregate(lambda x: list(x))
    round_winners = [{'round': r,
                      'winner': sorted(w, key = lambda x: re.sub(r'[^a-zA-Z0-9]', '', x).lower())
                     } for r, w in zip(round_winners_df.index.to_numpy(dtype=int).tolist(), round_winners_df.to_list())]
    round_winners.sort(key = lambda x: -x['round'])

    with open('data/hall_of_fame.json', 'w', encoding='utf-8') as file: # possibly also with pandas.DataFrame.to_json (?)
        json.dump({'table': table_data, 'rounds': round_winners}, file, ensure_ascii=False, indent=4)

    ### prepare player data ###
    for player in all_players:
        player_data = {'cards': mp_cards[player][:5],
                       'n_rounds_played': rounds_played_won[player]['played'],
                       'n_wins': rounds_played_won[player]['won'],
                       'nemesis': find_nemesis(data, player, 5),
                       'elo': Elo[-1][player],
                       'score_average': scores[player]['average'],
                       'score_total': scores[player]['total'],
                       'elo_list': [e[player] for e in Elo]}

        with open(f"data/players/{player}.json", 'w', encoding='utf-8') as file: # possibly also with pandas.DataFrame.to_json (?)
            json.dump(player_data, file, ensure_ascii=False, indent=4)

    ### prepare round data ###
    with open('data/urls.json') as file:
        urls = json.load(file)

    for round in data['round'].unique():
        data_df = data.loc[data['round']==round]

        players = data_df['player'].to_list()
        deck_list = data_df.loc[:, data_df.columns.str.startswith('card_')].to_numpy().tolist()
        round_data = {'decks': [{'index': i+1, 'player': p, 'cards': [c for c in d if isinstance(c, str)]} for i, (p, d) in enumerate(zip(players, deck_list))]}

        results_list = data_df.loc[:, data_df.columns.str.startswith(('result_', 'sum'))].dropna(how='any', axis=1).to_numpy(dtype=int).tolist()
        round_data['results'] = [{'index': i+1, 'values': l} for i, l in enumerate(results_list)]

        round_data['link'] = urls[str(round)]
        #json['rules'] =
        #json['notes'] =
        #json['banned_cards'] =
        #json['deadline'] =

        with open(f"data/rounds/{round}.json", 'w', encoding='utf-8') as file: # possibly also with pandas.DataFrame.to_json (?)
            json.dump(round_data, file, ensure_ascii=False, indent=4)
