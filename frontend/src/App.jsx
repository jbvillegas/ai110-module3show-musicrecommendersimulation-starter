import { useState } from 'react';
import './App.css';



function App() {
  const [mode, setMode] = useState('recommend');
  const [input, setInput] = useState({ genre: '', mood: '', query: '', tone: 'friendly' });
  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResults(null);
    if (mode === 'recommend') {
      // Send POST to /recommend
      const payload = {
        genre: input.genre,
        mood: input.mood,
        energy: 0.7, // Optionally add a slider/input for energy
        tempo_bpm: 120.0 // Optionally add a slider/input for tempo
      };
      try {
        const res = await fetch('http://localhost:5050/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        setResults(data);
      } catch (err) {
        setResults([]);
        alert('Failed to fetch recommendations. Is the backend running?');
      }
    } else {
      // Send POST to /quiz
      const payload = {
        query: input.query,
        tone: input.tone
      };
      try {
        const res = await fetch('http://localhost:5050/quiz', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        setResults(data);
      } catch (err) {
        setResults({ question: '', context: '' });
        alert('Failed to fetch quiz question. Is the backend running?');
      }
    }
  };

  return (
    <div className="container">
      <div className="title"><h1>Music Recommender & Study Bot</h1></div>
      
      <div className="mode-switch">
        <button className={mode === 'recommend' ? 'active' : ''} onClick={() => setMode('recommend')}>Recommendation</button>
        <button className={mode === 'quiz' ? 'active' : ''} onClick={() => setMode('quiz')}>Quiz</button>
      </div>
      <form className="input-form" onSubmit={handleSubmit}>
        {mode === 'recommend' ? (
          <>
            <label>
              Genre:
              <input name="genre" value={input.genre} onChange={handleChange} placeholder="e.g. pop" />
            </label>
            <label>
              Mood:
              <input name="mood" value={input.mood} onChange={handleChange} placeholder="e.g. happy" />
            </label>
          </>
        ) : (
          <>
            <label>
              Query:
              <input name="query" value={input.query} onChange={handleChange} placeholder="e.g. music recommendation" />
            </label>
            <label>
              Tone:
              <select name="tone" value={input.tone} onChange={handleChange}>
                <option value="friendly">Friendly</option>
                <option value="professional">Professional</option>
              </select>
            </label>
          </>
        )}
        <button type="submit">Submit</button>
      </form>
      <div className="results">
        {results && mode === 'recommend' && (
          <div>
            <h2>Top Recommendations</h2>
            <ul>
              {results.map((song, idx) => (
                <li key={idx}>
                  <strong>{song.title}</strong> by {song.artist} <br />
                  <span className="reason">{song.reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        {results && mode === 'quiz' && (
          <div>
            <h2>Quiz Question</h2>
            <p><strong>Q:</strong> {results.question}</p>
            <p className="context">{results.context}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
