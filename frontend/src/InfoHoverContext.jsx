import React, { createContext, useContext } from 'react';

// Create the Tooltip Context
const InfoHoverContext = createContext();

// Create a provider component
export const InfoHoverProvider = ({ children }) => {
  const infoTexts = {
    elo: "Elo score, starting value 1600, etc.",
    score: "% der möglichen Punkte in jeder Runde - durchschnittlich oder in Summe",
    anotherTooltip: "This is some other tooltip text.",
  };

  return (
    <InfoHoverContext.Provider value={infoTexts}>
      {children}
    </InfoHoverContext.Provider>
  );
};

// Create a custom hook to use the Tooltip Context
export const useInfoTexts = () => useContext(InfoHoverContext);
