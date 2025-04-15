import React, { useEffect, useState } from 'react';

const CardHover = ({ cardName }) => {
  const [cardImage, setCardImage] = useState(null);
  const [isHovered, setIsHovered] = useState(false);

  cardName = cardName.replace(/&/g, ''); // protect the API URL

  const getCardImageFromLocalStorage = (cardName) => {
    const storedImage = localStorage.getItem(`cardImage_${cardName}`);
    return storedImage ? storedImage : null;
  };

  const saveCardImageToLocalStorage = (cardName, imageUrl) => {
    localStorage.setItem(`cardImage_${cardName}`, imageUrl);
  };

  const fetchCardImage = async () => {
    try {
      // Fetch card data using the Scryfall API
      const response = await fetch(
        `https://api.scryfall.com/cards/named?exact=${cardName}`
      );
      const data = await response.json();

      // Check for multiple prints, get the oldest one
      if (data && data.prints_search_uri) {
        const printResponse = await fetch(data.prints_search_uri);
        const printData = await printResponse.json();

        // Get the last (oldest) print from the array of card prints
        const oldestPrint = printData.data[printData.data.length - 1];
        setCardImage(oldestPrint?.image_uris?.normal || null);
        saveCardImageToLocalStorage(
          cardName,
          oldestPrint?.image_uris?.normal || null
        );
      } else {
        // no prints are available: fallback to the normal image from the main card
        setCardImage(data?.image_uris?.normal || null);
        saveCardImageToLocalStorage(cardName, data?.image_uris?.normal || null);
      }
    } catch (error) {
      console.error('Error fetching card data:', error);
    }
  };

  useEffect(() => {
    // try to get image from local storage first
    const storedImage = getCardImageFromLocalStorage(cardName);
    if (storedImage) {
      setCardImage(storedImage);
    }
  }, [cardName]);

  const handleMouseEnter = () => {
    setIsHovered(true);
    if (!cardImage) {
      // if not already loaded,
      fetchCardImage(); // fetch the image
    }
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setCardImage(null); // clear the image when not hovering
  };

  return (
    <div
      className="card-container"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <span>{cardName}</span>
      {isHovered && cardImage && (
        <div className="card-image">
          <img src={cardImage} alt={cardName} />
        </div>
      )}
    </div>
  );
};

export default CardHover;
