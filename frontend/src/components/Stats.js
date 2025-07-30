import React from 'react';

function Stats() {
  const username = localStorage.getItem('username');
  const age = localStorage.getItem('age');
  const level = parseInt(localStorage.getItem('level')) || 1;

  let suggestion = "Explore More!";
  if (level >= 1 && level < 3) suggestion = "Try learning basics of Science and Math!";
  else if (level >= 3 && level < 5) suggestion = "You may enjoy problem solving. Look into engineering or analytics.";
  else if (level >= 5) suggestion = "You're great! Consider careers in Data Science, Engineering, or Research!";

  return (
    <div className="App">
      <h1>{username}'s Stats 📊</h1>
      <p>Age: {age}</p>
      <p>Current Level: {level}</p>
      <p><strong>Career Suggestion:</strong> {suggestion}</p>
    </div>
  );
}

export default Stats;
