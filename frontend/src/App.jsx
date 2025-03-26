import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';

import ApiDocumentation from './ApiDocumentation';
import BannedList from './BannedList';
import Footer from './Footer';
import HallOfFame from './HallOfFame';
import Header from './Header';
import { InfoHoverProvider } from './InfoHoverContext';
import LandingPage from './LandingPage';
import PlayerStats from './PlayerStats';
import RoundDetails from './RoundDetails';

function App() {
  return (
    <div className="wrapper">
      <InfoHoverProvider>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/bannedlist' element={<BannedList />} />
          <Route path='/halloffame' element={<HallOfFame />} />
          <Route path='/player/:name' element={<PlayerStats />} />
          <Route path='/round/:number' element={<RoundDetails />} />
          <Route path='/apidocumentation' element={<ApiDocumentation />} />
        </Routes>
        <Footer />
      </BrowserRouter>
      </InfoHoverProvider>
    </div>
  );
}

export default App;
