import React, { useState } from 'react';

const CardHover = ({ cardName }) => {
  const [cardImage, setCardImage] = useState(null);
  const [isHovered, setIsHovered] = useState(false);

  const fetchCardImage = async () => {
    try {
      // Fetch card data using the Scryfall API
      const response = await fetch(`https://api.scryfall.com/cards/named?exact=${cardName}`);
      const data = await response.json();

      // Check if the card has multiple prints and get the oldest one
      if (data && data.prints_search_uri) {
        const printResponse = await fetch(data.prints_search_uri);
        const printData = await printResponse.json();

        // Get the last (oldest) print from the array of card prints
        const oldestPrint = printData.data[printData.data.length-1];

        // Set the image from the oldest print
        setCardImage(oldestPrint?.image_uris?.normal || null);
      } else {
        // If no prints are available, fallback to the normal image from the main card
        setCardImage(data?.image_uris?.normal || null);
      }
    } catch (error) {
      console.error("Error fetching card data:", error);
    }
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
    fetchCardImage(); // Fetch the image when hovering
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setCardImage(null); // Optionally, clear the image when not hovering
  };

  return (
    <div
      className="card-container"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <span>{cardName}</span>

      {/* Only show the card image if hovering */}
      {isHovered && cardImage && (
        <div className="card-image">
          <img src={cardImage} alt={cardName} />
        </div>
      )}
    </div>
  );
};

export default CardHover;
