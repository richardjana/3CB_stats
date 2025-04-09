import React, { createContext, useContext } from 'react';

// Create the Tooltip Context
const InfoHoverContext = createContext();

// Create a provider component
export const InfoHoverProvider = ({ children }) => {
  const infoTexts = {
    elo: "Elo-Zahl (<Link to={https://de.wikipedia.org/wiki/Elo-Zahl}>Wikipedia</Link>)",
    score: "als % der möglichen Punkte in je Runde",
  };

  return (
    <InfoHoverContext.Provider value={infoTexts}>
      {children}
    </InfoHoverContext.Provider>
  );
};

// Create a custom hook to use the Tooltip Context
export const useInfoTexts = () => useContext(InfoHoverContext);
