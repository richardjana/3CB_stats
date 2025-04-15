import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';
import { useParams } from 'react-router-dom';

import CardHover from './CardHover';

const RoundDetails = () => {
  const { number } = useParams();

  const [decks, setDecks] = useState([]);
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!number) return;

    const loadData = async () => {
      try {
        const data = await import(`./data/rounds/${number}.json`);

        setDecks(data.decks);
        setResults(data.results);
      } catch (err) {
        console.error('Round data not found:', err);
      }
    };

    loadData();
  }, [number]);

  return (
    <div>
      <div>
        <h2> Runde: {number} </h2>
        <table className="decks">
          <thead>
            <tr>
              <th>Index</th>
              <th>Spieler</th>
              <th>Deck</th>
            </tr>
          </thead>
          <tbody>
            {decks.map((line, idx) => (
              <tr key={idx}>
                <td>{line.index}</td>
                <td>
                  <Link to={`/player/${line.player}`}>{line.player}</Link>
                </td>
                <td>
                  {line.cards.map((c, index) => (
                    <React.Fragment key={index}>
                      <CardHover cardName={c} />
                      {index < line.cards.length - 1 && ', '}
                    </React.Fragment>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <table className="results_table">
          <thead>
            <tr>
              <th></th>
              {Array.from({ length: results.length }, (_, i) => (
                <th key={i}>{i + 1}</th>
              ))}
              <th>Σ</th>
            </tr>
          </thead>
          <tbody>
            {results.map((res) => (
              <tr key={res.index}>
                <td>{res.index}</td>
                {res.values.map((val, idx) => (
                  <td key={idx}>{String(val).padStart(2, '0')}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RoundDetails;
