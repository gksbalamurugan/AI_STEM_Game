import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './StatsPage.css';

const StatsPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/suggestion')
      .then(res => setData(res.data))
      .catch(err => console.error("Failed to fetch suggestion", err));
  }, []);

  if (!data) return <div className="stats-container">Loading career insights...</div>;

  return (
    <div className="stats-container">
      <h2>📊 Your STEM Journey</h2>
      <div className="stats-card">
        <p><strong>Level:</strong> {data.level}</p>
        <p><strong>Accuracy:</strong> {data.accuracy}%</p>
        <p><strong>Average Time Per Question:</strong> {data.average_time} sec</p>
        <p><strong>Thinking Style:</strong> {data.speed_type}</p>
      </div>

      <div className="suggestion-box">
        <h3>🎯 Career Suggestion</h3>
        <p>{data.career_suggestion}</p>
      </div>
    </div>
  );
};

export default StatsPage;
