import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../App.css';

function App() {
  const [questionData, setQuestionData] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);
  const [level, setLevel] = useState(1);
  const [stars, setStars] = useState(0);

  useEffect(() => {
    fetchState();
    fetchQuestion();
  }, []);

  const fetchState = async () => {
    const res = await axios.get('http://localhost:5000/api/state');
    setLevel(res.data.level);
    setStars(res.data.stars);
  };

  const fetchQuestion = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:5000/api/question');
      setQuestionData(res.data);
      setFeedback('');
      setUserAnswer('');
    } catch (err) {
      setFeedback("Failed to load question. Try again.");
    }
    setLoading(false);
  };

  const handleSubmit = async () => {
    if (!userAnswer) return alert("Please select an answer!");
    try {
      const res = await axios.post('http://localhost:5000/api/submit', {
        user_answer: userAnswer,
        correct_answer: questionData.correct
      });

      if (res.data.result === 'correct') {
        setFeedback("✅ Correct!");
        setStars(prev => prev + 1);
      } else if (res.data.result === 'level_up') {
        setFeedback("🎉 Level Up!");
        setLevel(res.data.level);
        setStars(0);
      } else {
        setFeedback(`❌ Wrong! The correct answer is ${questionData.correct.toUpperCase()}.\nReason: ${questionData.reason}`);
      }

      setTimeout(fetchQuestion, 3000);
    } catch (err) {
      setFeedback("Error submitting answer.");
    }
  };

  if (loading || !questionData) return <div className="App">Loading...</div>;

  return (
    <div className="App">
      <h1>STEM Master 🚀</h1>
      <h3>Level {level} | Stars: ⭐ {stars}</h3>
      <div className="question-box">
        <p><strong>{questionData.question}</strong></p>
        {questionData.options.map((opt, idx) => (
          <label key={idx} className="option">
            <input
              type="radio"
              name="option"
              value={String.fromCharCode(97 + idx)}
              checked={userAnswer === String.fromCharCode(97 + idx)}
              onChange={(e) => setUserAnswer(e.target.value)}
            />
            {String.fromCharCode(97 + idx)}) {opt}
          </label>
        ))}
      </div>
      <button onClick={handleSubmit} className="submit-btn">Submit</button>
      {feedback && <div className="feedback">{feedback}</div>}
    </div>
  );
}

export default App;
