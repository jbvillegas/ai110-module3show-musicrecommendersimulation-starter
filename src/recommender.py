from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert fields to correct types."""
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and explain reasons."""
    score = 0.0
    reasons = []

    # Genre match
    if song.get('genre') == user_prefs.get('genre'):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song.get('mood') == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 1.0 * (1 - abs(energy_song - target_energy))
    score += energy_score
    reasons.append(f"energy close (+{energy_score:.2f})")

    # Tempo similarity
    tempo_song = song.get('tempo_bpm', 0.0)
    target_tempo = user_prefs.get('tempo_bpm', 120.0)
    min_tempo = 50.0
    max_tempo = 200.0
    normalized_tempo_diff = abs(tempo_song - target_tempo) / (max_tempo - min_tempo)
    tempo_score = 0.5 * (1 - normalized_tempo_diff)
    score += tempo_score
    reasons.append(f"tempo close (+{tempo_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Recommend top k songs for user preferences."""
    # Score all songs
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    # Sort by score descending
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    # Return top k as (song, score, reasons)
    return [(song, score, reasons) for song, score, reasons in scored_sorted[:k]]
