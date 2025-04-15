import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import './Header.css';

const Header = () => {
  const [roundNumbers, setRoundNumbers] = useState([]);
  const [playerNames, setPlayerNames] = useState([]);
  const [isRoundDropdownOpen, setIsRoundDropdownOpen] = useState(false);
  const [isPlayerDropdownOpen, setIsPlayerDropdownOpen] = useState(false);

  useEffect(() => {
        
        const loadData = async () => {
          try {
            const data = await import(`./data/players_rounds_lists.json`);
    
            setRoundNumbers(data.round_numbers);
            setPlayerNames(data.player_names);
          } catch (err) {
            console.error('Player names and round numbers data not found:', err);
          }
        };
    
        loadData();
      }, []);

  return (
    <header className='header'>
      <div className='container'>
        <div className='logo'>
          <Link to='/' className='link'><h1>3CB Info</h1></Link>
        </div>
        <nav className='nav'>
          <ul className='nav-list'>
            <li className='nav-item'><Link to='/halloffame' className='link'>Hall of Fame</Link></li>

            <li
              className='nav-item'
              onMouseEnter={() => setIsRoundDropdownOpen(true)}
              onMouseLeave={() => setIsRoundDropdownOpen(false)}
            >
              <div className='link'>
                  <span>Runden</span>
                  <i className={`fas fa-caret-down ${isRoundDropdownOpen ? '' : 'rotate'}`} style={{ marginLeft: '5px' }}></i>
              </div>
              {isRoundDropdownOpen && (
                <ul className='dropdown-menu'>
                  {roundNumbers.map((num) => (
                    <li key={num} className='dropdown-item'>
                      <Link to={`/round/${num}`} className='link'>Runde {num}</Link>
                    </li>
                  ))}
                </ul>
              )}
            </li>

            <li
              className='nav-item'
              onMouseEnter={() => setIsPlayerDropdownOpen(true)}
              onMouseLeave={() => setIsPlayerDropdownOpen(false)}
            >
              <div className='link'>
                  <span>Spieler</span>
                  <i className={`fas fa-caret-down ${isPlayerDropdownOpen ? '' : 'rotate'}`} style={{ marginLeft: '5px' }}></i>
              </div>
              {isPlayerDropdownOpen && (
                <ul className='dropdown-menu'>
                  {playerNames.map((p) => (
                    <li key={p} className='dropdown-item'>
                      <Link to={`/player/${p}`} className='link'>{p}</Link>
                    </li>
                  ))}
                </ul>
              )}
            </li>

            <li className='nav-item'><Link to='/bannedlist' className='link'>Bannedlist</Link></li>
            <li className='nav-item'><Link to='/popularcards' className='link'>Oft gespielte Karten</Link></li>
            <li className='nav-item'><Link to='/apidocumentation' className='link'>API</Link></li>

          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
