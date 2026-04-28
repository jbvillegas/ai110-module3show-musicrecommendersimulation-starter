import sys
from pathlib import Path
from src.recommender import load_songs, recommend_songs
from src.agent import AgenticStudyAgent
from src.reliability import check_recommendation_consistency, check_quiz_generation_consistency

# Predefined user profiles for recommendation evaluation
profiles = [
    {"name": "High-Energy Pop", "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9, "tempo_bpm": 130}},
    {"name": "Chill Lofi", "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.3, "tempo_bpm": 80}},
    {"name": "Deep Intense Rock", "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95, "tempo_bpm": 140}},
]

quiz_topics = [
    "music recommendation",
    "agentic workflow",
    "retrieval-augmented generation",
]

def main():
    data_path = Path(__file__).resolve().parent / "data" / "songs.csv"
    songs = load_songs(str(data_path))
    print("=== Recommendation Consistency ===")
    for profile in profiles:
        print(f"Profile: {profile['name']}")
        # Use only first 3 songs for stability check
        from src.recommender import Song, UserProfile, Recommender
        song_records = [
            {field: song[field] for field in Song.__dataclass_fields__.keys() if field in song}
            for song in songs
        ]
        recommender = Recommender([Song(**record) for record in song_records])
        user = UserProfile(
            favorite_genre=profile["prefs"]["genre"],
            favorite_mood=profile["prefs"]["mood"],
            target_energy=profile["prefs"].get("energy", 0.5),
            likes_acoustic=False,
            target_tempo_bpm=profile["prefs"].get("tempo_bpm", 120),
        )
        metrics = check_recommendation_consistency(recommender, user, runs=3, top_k=3)
        print(f"  Stable: {metrics['stable_fraction']:.2f} ({metrics['reference_top_ids']})")
    print()

    print("=== Quiz Generation Consistency ===")
    agent = AgenticStudyAgent(notes_dir="notes", tone="friendly")
    for topic in quiz_topics:
        metrics = check_quiz_generation_consistency(agent, topic, runs=3)
        print(f"Topic: {topic}")
        print(f"  Stable: {metrics['stable']}")
        print(f"  Example: {metrics['questions'][0][:80]}{'...' if len(metrics['questions'][0]) > 80 else ''}")
    print()

if __name__ == "__main__":
    main()
