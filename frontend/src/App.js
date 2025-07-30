import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Game from './components/Game';
import StatsPage from './components/StatsPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <h1>🌟 STEM Master</h1>
          <nav className="navbar">
            <Link to="/" className="nav-link">Start Game</Link>
            <Link to="/stats" className="nav-link">My Stats</Link>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Game />} />
          <Route path="/stats" element={<StatsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
