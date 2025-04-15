import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';
import { useParams } from 'react-router-dom';

import CardHover from './CardHover';
import formatFloat from './utilities/formatFloat';
import InfoHover from './InfoHover';
import LineChart from './LineChart';

const PlayerStats = () => {
  const { name } = useParams();

  const [mpCards, setMpCards] = useState([]);
  const [roundsPlayed, setRoundsPlayed] = useState(0);
  const [roundsWon, setRoundsWon] = useState(0);
  const [scoreAverage, setScoreAverage] = useState(0);
  const [scoreTotal, setScoreTotal] = useState(0);
  const [eloList, setEloList] = useState([]);
  const [elo, setElo] = useState(0);
  const [nemesis, setNemesis] = useState([]);

  useEffect(() => {
    if (!name) return;

    const loadData = async () => {
      try {
        const data = await import(`./data/players/${name}.json`);

        setMpCards(data.cards);
        setRoundsPlayed(data.n_rounds_played);
        setRoundsWon(data.n_wins);
        setScoreAverage(data.score_average);
        setScoreTotal(data.score_total);
        setEloList(data.elo_list);
        setElo(data.elo);
        setNemesis(data.nemesis[0]);
      } catch (err) {
        console.error('Player data not found:', err);
      }
    };

    loadData();
  }, [name]);

  return (
    <div>
      <div>
        <h2> Spieler: {name} </h2>
        <div className="player_stats">
          <h3>Stats</h3>
          <p>{`Gespielte Runden: ${roundsPlayed}`}</p>
          <p>{`Siege: ${roundsWon}`}</p>
          <p>{`Punkte (Summe): ${formatFloat(scoreTotal)}`}</p>
          <p>{`Punkte (Mittel): ${formatFloat(scoreAverage)}`}</p>
          <div>
            Elo <InfoHover type="elo" />: {formatFloat(elo)}
          </div>
        </div>
        <div className="mp_cards">
          <h3>Meistgespielte Karten</h3>
          <table className="mp_cards_table">
            <tbody>
              {mpCards.map((c, index) => (
                <tr key={index}>
                  <td>
                    <CardHover cardName={c.card} />
                  </td>
                  <td>
                    {c.count} ({formatFloat(c['%'])}%)
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="nemesis">
          <h3>Nemesis</h3>
          <p>
            Nemesis:{' '}
            <Link to={`/player/${nemesis['player']}`}>{nemesis['player']}</Link>
          </p>
          <p>{`Begegnungen: ${nemesis['n_matches']}`}</p>
          <p>{`Punkte: ${formatFloat(nemesis['score'])}`}</p>
        </div>
        <div className="elo-chart">
          <h3>
            Elo <InfoHover type="elo" />
          </h3>
          <LineChart data={eloList} />
        </div>
      </div>
    </div>
  );
};

export default PlayerStats;
