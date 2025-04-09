import Chart from 'chart.js/auto';
import React, { useEffect, useState } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import { Link } from 'react-router';
import { useParams } from 'react-router-dom';

import use3cbApi from './Axios3cbApi';
import CardHover from './CardHover';

const RoundDetails = () => {
  const {number} = useParams()

  const [decks, setDecks] = useState([]);
  const [results, setResults] = useState([]);

  const { data, isLoading, errorMessage } = use3cbApi(`round/${number}`);

  useEffect(() => {
    if (data) {
      setDecks(data.decks);
      setResults(data.results);
    }
  }, [data]);

  if (errorMessage) return <div>Error: {errorMessage}</div>;
  if (!errorMessage && isLoading) return <div>Loading...</div>;

  return (
    <div>
        <div>
          <h2> Runde: {number} </h2>
          <table className='decks'>
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
                  <td><Link to={`/player/${line.player}`}>{line.player}</Link></td>
                  <td>
                    {line.cards.map((c, index) => (
                      <React.Fragment key={index}>
                        <CardHover cardName={c} />
                        {index < line.cards.length - 1 && ", "}
                      </React.Fragment>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <table className='results_table'>
              <thead>
                  <tr>
                      <th></th>
                      {Array.from({ length: results.length }, (_, i) => (<th key={i}>{i+1}</th>))}
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

export default RoundDetails
