import React, { useEffect, useState } from 'react';

import use3cbApi from './Axios3cbApi';
import CardHover from './CardHover';
import formatFloat from './utilities/formatFloat';

const PopularCards = () => {
  const [mpCards, setMpCards] = useState([]);

  const { data, isLoading, errorMessage } = use3cbApi(`popular_cards`);

  useEffect(() => {
    if (data) {
      setMpCards(data);
    }
  }, [data]);

  if (errorMessage) return <div>Error: {errorMessage}</div>;
  if (!errorMessage && isLoading) return <div>Loading...</div>;

  return (
    <div>
      <div>
        <h2> Oft gespielte Karten </h2>

          <table className='mp_cards_table'>
              <tbody>
                {mpCards.map((c, index) => (<tr key={index}>
                                              <td><CardHover cardName={c.card} /></td>
                                              <td>{c.count} ({formatFloat(c['%'])}%)</td>
                                            </tr>))}
              </tbody>
          </table>

      </div>
  </div>);
}

export default PopularCards
