import Chart from 'chart.js/auto';
import React, { useEffect, useState } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import { Link } from 'react-router';
import { useParams } from 'react-router-dom';

import use3cbApi from './Axios3cbApi';
import CardHover from './CardHover';
import formatFloat from './utilities/formatFloat';
import InfoHover from './InfoHover';

const PlayerStats = () => {
  const {name} = useParams()

  const [mpCards, setMpCards] = useState([]);
  const [roundsPlayed, setRoundsPlayed] = useState(0);
  const [roundsWon, setRoundsWon] = useState(0);
  const [scoreAverage, setScoreAverage] = useState(0);
  const [scoreTotal, setScoreTotal] = useState(0);
  const [scoreList, setScoreList] = useState([]);
  const [elo, setElo] = useState(0);
  const [nemesis, setNemesis] = useState([]);

  const { data, isLoading, errorMessage } = use3cbApi(`playerstats/${name}`);

  useEffect(() => {
    if (data) {
      setMpCards(data.cards);
      setRoundsPlayed(data.n_rounds_played);
      setRoundsWon(data.n_wins);
      setScoreAverage(data.score_average);
      setScoreTotal(data.score_total);
      setScoreList(data.score_list);
      setElo(data.elo);
      setNemesis(data.nemesis[0]);
    }
  }, [data]);

  return (
    <div>
    {errorMessage && <h2>{errorMessage}</h2>}
    {!errorMessage && isLoading && <h2>Loading data</h2>}
    {!errorMessage && !isLoading && (
      <div>
        <h2> Player: {name} </h2>
        <div className='player_stats'>
            <h3>Stats</h3>
            <p>{`Rounds played: ${roundsPlayed}`}</p>
            <p>{`Rounds won: ${roundsWon}`}</p>
            <p>{`Total score: ${formatFloat(scoreTotal)}`}</p>
            <p>{`Average score: ${formatFloat(scoreAverage)}`}</p>
            <div>Elo <InfoHover type='elo' />: {formatFloat(elo)}</div>
        </div>
        <div className='mp_cards'>
            <h3>Most-played cards</h3>
              <table className='mp_cards_table'>
                  <tbody>
                    {mpCards.map((c, index) => (<tr key={index}>
                                                  <td><CardHover cardName={c.card} /></td>
                                                  <td>{c.count}</td>
                                                </tr>))}
                  </tbody>
              </table>
        </div>
        <div className='nemesis'>
            <h3>Nemesis</h3>
            <p>Nemesis: <Link to={`/player/${nemesis['player']}`}>{nemesis['player']}</Link></p>
            <p>{`Times played: ${nemesis['n_matches']}`}</p>
            <p>{`Score: ${formatFloat(nemesis['score'])}`}</p>
        </div>
      </div>
    )}
  </div>);
}

export default PlayerStats
