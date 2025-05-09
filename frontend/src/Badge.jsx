import React from 'react';
import './Badge.css';

// Badge component that accepts 'type', 'label', and 'description' as props
const Badge = ({ type, label, description }) => {
  // Mapping badge types to image paths
  const badgeImages = {
    perfect_round: '/images/badge_perfect_round.png',
    streak: '/images/badge_streak.png',
    all_draws: '/images/badge_all_draws.png',
  };

  return (
    <div className="badge-item">
      <img src={badgeImages[type]} alt={label} className="badge-icon" />
      <div className="badge-text">
        <strong>{label}</strong>
        <p>{description}</p>
      </div>
    </div>
  );
};

export default Badge;
