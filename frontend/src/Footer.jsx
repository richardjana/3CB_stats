import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer style={footerStyle}>
      <div style={containerStyle}>
        <p style={textStyle}>
          &copy; {currentYear} Richard Jana.
        </p>
        <p style={textStyle}>
          Card images taken from Scryfall.com
        </p>
        <p style={textStyle}>
          Magic: The Gathering, including card images and mana symbols, is copyright Wizards of the Coast, LLC.
        </p>
      </div>
    </footer>
  );
};

// Inline styles for the footer
const footerStyle = {
  backgroundColor: '#333',
  color: '#fff',
  padding: '20px 0',
  textAlign: 'center',
};

const containerStyle = {
  maxWidth: '1200px',
  margin: '0 auto',
};

const textStyle = {
  margin: 0,
  fontSize: '14px',
};

export default Footer;
