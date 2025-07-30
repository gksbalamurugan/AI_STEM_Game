import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const [username, setUsername] = useState('');
  const [age, setAge] = useState('');
  const navigate = useNavigate();

  const handleStart = () => {
    if (!username || !age) return alert("Enter name and age");
    localStorage.setItem('username', username);
    localStorage.setItem('age', age);
    navigate('/game');
  };

  const goToStats = () => navigate('/stats');

  return (
    <div className="App">
      <h1>STEM Master 🚀</h1>
      <input
        type="text"
        placeholder="Enter your name"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <br />
      <input
        type="number"
        placeholder="Enter your age"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />
      <br />
      <button onClick={handleStart}>Start Game</button>
      <button onClick={goToStats}>View Stats</button>
    </div>
  );
}

export default Home;
