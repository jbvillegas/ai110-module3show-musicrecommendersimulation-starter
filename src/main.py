import argparse
import logging
from pathlib import Path
from typing import Dict

from src.agent import AgenticStudyAgent
from src.recommender import (
    UserProfile,
    Song,
    Recommender,
    load_songs,
    recommend_songs,
    score_song_genre_first,
    score_song_mood_first,
    score_song_energy_focused,
)
from src.reliability import evaluate_reliability

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def format_recommendation(song: Dict, score: float, reasons: list) -> str:
    lines = [f"{song['title']} by {song['artist']} - Score: {score:.2f}"]
    lines.extend(f"  - {reason}" for reason in reasons)
    return "\n".join(lines)


def run_recommendation_mode(data_path: Path, top_k: int) -> None:
    try:
        songs = load_songs(str(data_path))
    except FileNotFoundError:
        logging.error(f"Song data file not found: {data_path}")
        return

    logging.info(f"Loaded {len(songs)} songs from {data_path}")

    profiles = [
        {
            "name": "High-Energy Pop",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9, "tempo_bpm": 130},
        },
        {
            "name": "Chill Lofi",
            "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.3, "tempo_bpm": 80},
        },
        {
            "name": "Deep Intense Rock",
            "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95, "tempo_bpm": 140},
        },
    ]

    for profile in profiles:
        print(f"\nProfile: {profile['name']}")
        entries = recommend_songs(profile["prefs"], songs, k=top_k)
        print("Top recommendations:")
        for song, score, reasons in entries:
            print(format_recommendation(song, score, reasons))
            print()

    print("--- Genre-first recommendations ---")
    entries = recommend_songs(profiles[0]["prefs"], songs, k=top_k, scoring_fn=score_song_genre_first)
    for song, score, reasons in entries:
        print(format_recommendation(song, score, reasons))
        print()

    print("--- Mood-first recommendations ---")
    entries = recommend_songs(profiles[0]["prefs"], songs, k=top_k, scoring_fn=score_song_mood_first)
    for song, score, reasons in entries:
        print(format_recommendation(song, score, reasons))
        print()

    print("--- Energy-focused recommendations ---")
    entries = recommend_songs(profiles[0]["prefs"], songs, k=top_k, scoring_fn=score_song_energy_focused)
    for song, score, reasons in entries:
        print(format_recommendation(song, score, reasons))
        print()


def run_quiz_mode(topic: str, tone: str) -> None:
    agent = AgenticStudyAgent(notes_dir="notes", tone=tone)
    if not agent.corpus:
        logging.warning("No notes were found in the notes/ folder. The quiz bot will still run but may have no retrieval context.")
    result = agent.run(topic)

    print("Plan:")
    for step in result["plan"]:
        print(f"  - {step}")
    print("\nRetrieved docs:")
    for doc in result["retrieved_docs"]:
        print(f"  - {doc}")
    print("\nGenerated quiz question:")
    print(result["question"])
    print(f"\nValid: {result['valid']}")


def run_reliability_mode(data_path: Path, query: str) -> None:
    try:
        songs = load_songs(str(data_path))
    except FileNotFoundError:
        logging.error(f"Song data file not found: {data_path}")
        return

    song_records = [
        {field: song[field] for field in Song.__dataclass_fields__.keys() if field in song}
        for song in songs
    ]
    recommender = Recommender([Song(**record) for record in song_records])
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    agent = AgenticStudyAgent(notes_dir="notes", tone="friendly")
    metrics = evaluate_reliability(recommender, user, agent, query)

    print("Reliability evaluation:")
    print(f"  Recommendation stability: {metrics['recommendation_consistency']['stable_fraction']:.2f}")
    print(f"  Quiz generation stable: {metrics['quiz_generation_consistency']['stable']}")
    print("  Example quiz question:")
    print(metrics['quiz_generation_consistency']['questions'][0])


def main() -> None:
    parser = argparse.ArgumentParser(description="Music recommender with study bot and reliability checks.")
    parser.add_argument("--mode", choices=["recommend", "quiz", "reliability"], default="recommend")
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--query", type=str, default="music recommendation")
    parser.add_argument("--tone", type=str, default="friendly")
    args = parser.parse_args()

    data_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

    if args.mode == "recommend":
        run_recommendation_mode(data_path, args.top_k)
    elif args.mode == "quiz":
        run_quiz_mode(args.query, args.tone)
    elif args.mode == "reliability":
        run_reliability_mode(data_path, args.query)


if __name__ == "__main__":
    main()
