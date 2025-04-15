import React, { useEffect, useState } from 'react';

import CardHover from './CardHover';
import formatFloat from './utilities/formatFloat';

const PopularCards = () => {
  const [mpCards, setMpCards] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await import(`./data/popular_cards.json`);

        setMpCards(data.default || data);
      } catch (err) {
        console.error('Popular cards data not found:', err);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      <div>
        <h2> Oft gespielte Karten </h2>

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
    </div>
  );
};

export default PopularCards;
