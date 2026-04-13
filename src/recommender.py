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
    popularity: float
    release_decade: int
    instrumentalness: float
    mood_tags: str
    language: str

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
                'acousticness': float(row['acousticness']),
                'popularity': float(row['popularity']),
                'release_decade': int(row['release_decade']),
                'instrumentalness': float(row['instrumentalness']),
                'mood_tags': row['mood_tags'],
                'language': row['language']
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and explain reasons."""
    score = 0.0
    reasons = []

    # Genre match (weight halved)
    if song.get('genre') == user_prefs.get('genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Mood match (commented out for feature removal experiment)
    # if song.get('mood') == user_prefs.get('mood'):
    #     score += 1.0
    #     reasons.append("mood match (+1.0)")

    # Energy similarity (weight doubled)
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 2.0 * (1 - abs(energy_song - target_energy))
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

    # Advanced feature scoring
    # Popularity: reward higher popularity (0-100 scaled to 0-1, weight 1.0)
    popularity = song.get('popularity', 50)
    popularity_score = 1.0 * (popularity / 100)
    score += popularity_score
    reasons.append(f"popularity (+{popularity_score:.2f})")

    # Release decade: reward 2010s and 2020s (+0.5), penalize 1980s (-0.5)
    decade = int(song.get('release_decade', 2000))
    if decade >= 2010:
        score += 0.5
        reasons.append("modern decade (+0.5)")
    elif decade == 1980:
        score -= 0.5
        reasons.append("old decade (-0.5)")

    # Mood tags: reward if user mood in mood_tags (+0.5)
    mood_tags = song.get('mood_tags', "").split(',')
    if user_prefs.get('mood') and user_prefs['mood'] in [tag.strip() for tag in mood_tags]:
        score += 0.5
        reasons.append("mood tag match (+0.5)")

    # Instrumentalness: reward highly instrumental songs if user likes acoustic (+0.5 if >0.8)
    if user_prefs.get('likes_acoustic') and float(song.get('instrumentalness', 0)) > 0.8:
        score += 0.5
        reasons.append("instrumental (+0.5)")

    # Language: reward English songs (+0.2)
    if song.get('language', '').lower() == 'english':
        score += 0.2
        reasons.append("English language (+0.2)")

    return score, reasons

def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Genre-first scoring: genre weight highest, others lower."""
    score = 0.0
    reasons = []
    if song.get('genre') == user_prefs.get('genre'):
        score += 2.0
        reasons.append("genre match (+2.0)")
    if song.get('mood') == user_prefs.get('mood'):
        score += 0.5
        reasons.append("mood match (+0.5)")
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 0.5 * (1 - abs(energy_song - target_energy))
    score += energy_score
    reasons.append(f"energy close (+{energy_score:.2f})")
    return score, reasons

def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Mood-first scoring: mood weight highest, others lower."""
    score = 0.0
    reasons = []
    if song.get('mood') == user_prefs.get('mood'):
        score += 2.0
        reasons.append("mood match (+2.0)")
    if song.get('genre') == user_prefs.get('genre'):
        score += 0.5
        reasons.append("genre match (+0.5)")
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 0.5 * (1 - abs(energy_song - target_energy))
    score += energy_score
    reasons.append(f"energy close (+{energy_score:.2f})")
    return score, reasons

def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Energy-focused scoring: energy weight highest, others lower."""
    score = 0.0
    reasons = []
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 2.0 * (1 - abs(energy_song - target_energy))
    score += energy_score
    reasons.append(f"energy close (+{energy_score:.2f})")
    if song.get('genre') == user_prefs.get('genre'):
        score += 0.5
        reasons.append("genre match (+0.5)")
    if song.get('mood') == user_prefs.get('mood'):
        score += 0.5
        reasons.append("mood match (+0.5)")
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, scoring_fn=None) -> List[Tuple[Dict, float, List[str]]]:
    """Recommend top k songs for user preferences using selected scoring function."""
    if scoring_fn is None:
        scoring_fn = score_song
    scored = [(song, *scoring_fn(user_prefs, song)) for song in songs]
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, reasons) for song, score, reasons in scored_sorted[:k]]
