from dataclasses import dataclass
from typing import Dict, List, Tuple
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
    tempo_bpm: float = 120.0
    valence: float = 0.5
    danceability: float = 0.5
    acousticness: float = 0.0
    popularity: float = 50.0
    release_decade: int = 2020
    instrumentalness: float = 0.0
    mood_tags: str = ""
    language: str = "english"


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
    target_tempo_bpm: float = 120.0


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, *score_song_profile(user, song)) for song in self.songs]
        sorted_songs = sorted(scored, key=lambda item: item[1], reverse=True)
        return [song for song, score, reasons in sorted_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song_profile(user, song)
        summary = "; ".join(reasons) if reasons else "No strong matches found."
        return f"Score: {score:.2f}. {summary}"


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
                'mood_tags': row.get('mood_tags', ''),
                'language': row.get('language', 'english')
            }
            songs.append(song)
    return songs


def score_song_profile(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a dataclass-based song against a user profile."""
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")
    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_score = max(0.0, 2.0 * (1 - abs(song.energy - user.target_energy)))
    score += energy_score
    reasons.append(f"energy closeness (+{energy_score:.2f})")

    tempo_diff = abs(song.tempo_bpm - user.target_tempo_bpm) / 150.0
    tempo_score = max(0.0, 0.5 * (1 - tempo_diff))
    score += tempo_score
    reasons.append(f"tempo closeness (+{tempo_score:.2f})")

    if user.likes_acoustic and song.acousticness > 0.7:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")

    if song.language.lower() == 'english':
        score += 0.2
        reasons.append("English language (+0.2)")

    return score, reasons


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and explain reasons."""
    score = 0.0
    reasons: List[str] = []

    if song.get('genre') == user_prefs.get('genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song.get('mood') == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = max(0.0, 2.0 * (1 - abs(energy_song - target_energy)))
    score += energy_score
    reasons.append(f"energy closeness (+{energy_score:.2f})")

    tempo_song = song.get('tempo_bpm', 0.0)
    target_tempo = user_prefs.get('tempo_bpm', 120.0)
    tempo_diff = abs(tempo_song - target_tempo) / 150.0
    tempo_score = max(0.0, 0.5 * (1 - tempo_diff))
    score += tempo_score
    reasons.append(f"tempo closeness (+{tempo_score:.2f})")

    popularity = song.get('popularity', 50)
    popularity_score = 1.0 * (popularity / 100)
    score += popularity_score
    reasons.append(f"popularity (+{popularity_score:.2f})")

    if song.get('language', '').lower() == 'english':
        score += 0.2
        reasons.append("English language (+0.2)")

    return score, reasons


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []
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
    reasons.append(f"energy closeness (+{energy_score:.2f})")
    return score, reasons


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []
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
    reasons.append(f"energy closeness (+{energy_score:.2f})")
    return score, reasons


def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []
    energy_song = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_score = 2.0 * (1 - abs(energy_song - target_energy))
    score += energy_score
    reasons.append(f"energy closeness (+{energy_score:.2f})")
    if song.get('genre') == user_prefs.get('genre'):
        score += 0.5
        reasons.append("genre match (+0.5)")
    if song.get('mood') == user_prefs.get('mood'):
        score += 0.5
        reasons.append("mood match (+0.5)")
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, scoring_fn=None) -> List[Tuple[Dict, float, List[str]]]:
    if scoring_fn is None:
        scoring_fn = score_song
    scored = [(song, *scoring_fn(user_prefs, song)) for song in songs]
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, reasons) for song, score, reasons in scored_sorted[:k]]
