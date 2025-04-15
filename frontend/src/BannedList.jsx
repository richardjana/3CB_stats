import React, { useEffect, useState } from 'react';

import CardHover from './CardHover';

const BannedList = () => {
  const [regularList, setRegularList] = useState([]);
  const [introList, setIntroList] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await import(`./data/banned_list.json`);

        setRegularList(data.regular);
        setIntroList(data.introducing);
      } catch (err) {
        console.error('Popular cards data not found:', err);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      <h1>Verbotene Decks</h1>
      <ol>
        <li key="1">
          Decks, die den Gegner mehr als eine Karte pro Zug abwerfen - oder
          sonst irgendwie aus seiner Hand entfernen - lassen können.
        </li>
        <li key="2">
          Decks, die vor dem Ende des ersten Gegnerischen Zuges gewinnen.
        </li>
        <li key="3">
          Decks, die im ersten Zug infinite Mana herstellen können.
        </li>
      </ol>
      <h1>Allgemeine Bannedlist</h1>
      <ul>
        {regularList.map((card, idx) => (
          <li key={idx}>
            <CardHover cardName={card} />
          </li>
        ))}
      </ul>
      <p>Außerdem:</p>
      <ul>
        <li key="1">
          Alle Karten, die nicht Vintage-legal sind (Ante-Karten, Dexterity
          Karten à la <CardHover cardName="Chaos Orb" />, Spaßeditionen...)
        </li>
        <li key="2">
          Karten, die nur unter gewissen Umständen, aber nicht ausschließbar
          mehr als eine Karte discarden lassen können (z.B.{' '}
          <CardHover cardName="Cabal Therapy" />,{' '}
          <CardHover cardName="Balance" />,{' '}
          <CardHover cardName="Restore Balance" /> oder{' '}
          <CardHover cardName="Memoricide" /> etc.)
        </li>
      </ul>
      <h1>"Introducing ..." Bannedlist</h1>
      <ul>
        {introList.map((card, idx) => (
          <li key={idx}>
            <CardHover cardName={card} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BannedList;
