import { useState } from 'react';
import './App.css';

const mockRecommendations = [
  { title: 'Sunrise City', artist: 'Neon Echo', reason: 'genre match, energy closeness' },
  { title: 'Gym Hero', artist: 'Max Pulse', reason: 'energy closeness, tempo closeness' },
  { title: 'Rooftop Lights', artist: 'Indigo Parade', reason: 'genre match, tempo closeness' },
];

const mockQuiz = {
  question: "What is the primary factor the recommender uses to match songs to user preferences?",
  context: "Based on the notes in 'study_notes.md [chunk 0]'..."
};

function App() {
  const [mode, setMode] = useState('recommend');
  const [input, setInput] = useState({ genre: '', mood: '', query: '', tone: 'friendly' });
  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mode === 'recommend') {
      setResults(mockRecommendations);
    } else {
      setResults(mockQuiz);
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
