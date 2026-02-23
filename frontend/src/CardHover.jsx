import React, { useEffect, useState } from 'react';

const CardHover = ({ cardName }) => {
  const [cardImage, setCardImage] = useState(null);
  const [isHovered, setIsHovered] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  cardName = cardName.replace(/&/g, '');

  const getCardImageFromLocalStorage = (cardName) => {
    const storedImage = localStorage.getItem(`cardImage_${cardName}`);
    return storedImage ? storedImage : null;
  };

  const saveCardImageToLocalStorage = (cardName, imageUrl) => {
    localStorage.setItem(`cardImage_${cardName}`, imageUrl);
  };

  const fetchCardImage = async () => {
    try {
      const response = await fetch(
        `https://api.scryfall.com/cards/named?exact=${cardName}`
      );
      const data = await response.json();

      if (data && data.prints_search_uri) {
        const printResponse = await fetch(data.prints_search_uri);
        const printData = await printResponse.json();
        const oldestPrint = printData.data[printData.data.length - 1];

        const image = oldestPrint?.image_uris?.small || null;
        setCardImage(image);
        saveCardImageToLocalStorage(cardName, image);
      } else {
        const image = data?.image_uris?.small || null;
        setCardImage(image);
        saveCardImageToLocalStorage(cardName, image);
      }
    } catch (error) {
      console.error('Error fetching card data:', error);
    }
  };

  useEffect(() => {
    const storedImage = getCardImageFromLocalStorage(cardName);
    if (storedImage) {
      setCardImage(storedImage);
    } else {
      fetchCardImage();
    }
  }, [cardName]);

  const handleMouseMove = (e) => {
    setPosition({
      x: e.clientX + 20, // 20px right
      y: e.clientY + 20, // 20px down
    });
  };

  return (
    <>
      <span
        className="inline-block"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onMouseMove={handleMouseMove}
      >
        {cardName}
      </span>

      {isHovered && cardImage && (
        <div
          className="fixed z-50 pointer-events-none transition-opacity duration-150"
          style={{
            left: position.x,
            top: position.y,
          }}
        >
          <img
            src={cardImage}
            alt={cardName}
            className="block scale-50 origin-top-left" // ~50% smaller
          />
        </div>
      )}
    </>
  );
};

export default CardHover;
