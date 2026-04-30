

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.recommender import load_songs, recommend_songs
from src.agent import AgenticStudyAgent
import os


app = Flask(__name__)
CORS(app)

# Load songs once at startup
SONGS_PATH = os.path.join(os.path.dirname(__file__), '../data/songs.csv')
songs = load_songs(SONGS_PATH)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    # expects: {"genre": ..., "mood": ..., "energy": ..., "tempo_bpm": ...}
    user_prefs = {
        "genre": data.get("genre", ""),
        "mood": data.get("mood", ""),
        "energy": float(data.get("energy", 0.5)),
        "tempo_bpm": float(data.get("tempo_bpm", 120.0)),
    }
    results = recommend_songs(user_prefs, songs, k=5)
    # Each result: (song_dict, score, reasons)
    formatted = [
        {
            "title": song["title"],
            "artist": song["artist"],
            "reason": "; ".join(reasons)
        }
        for song, score, reasons in results
    ]
    return jsonify(formatted)

@app.route('/quiz', methods=['POST'])
def quiz():
    data = request.json
    # expects: {"query": ..., "tone": ...}
    agent = AgenticStudyAgent(notes_dir="notes", tone=data.get("tone", "friendly"))
    result = agent.run(data.get("query", ""))
    return jsonify({
        "question": result["question"],
        "context": ", ".join(result["retrieved_docs"])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)
