"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_song_genre_first, score_song_mood_first, score_song_energy_focused


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, reasons = rec
        print(f"{song['title']} - Score: {score:.2f}")
        for reason in reasons:
            print(f"  {reason}")
        print()


    # Diverse user profiles
    profiles = [
        {"name": "High-Energy Pop", "prefs": {"genre": "pop", "mood": "intense", "energy": 0.9}},
        {"name": "Chill Lofi", "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.3}},
        {"name": "Deep Intense Rock", "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95}},
    ]

    for profile in profiles:
        print(f"\nProfile: {profile['name']}")
        recommendations = recommend_songs(profile["prefs"], songs, k=5)
        print("Top recommendations:\n")
        for rec in recommendations:
            song, score, reasons = rec
            print(f"{song['title']} - Score: {score:.2f}")
            for reason in reasons:
                print(f"  {reason}")
            print()


    print("\n--- Genre-First Mode ---")
    recommendations = recommend_songs(user_prefs, songs, k=5, scoring_fn=score_song_genre_first)
    for rec in recommendations:
        song, score, reasons = rec
        print(f"{song['title']} - Score: {score:.2f}")
        for reason in reasons:
            print(f"  {reason}")
        print()

    print("\n--- Mood-First Mode ---")
    recommendations = recommend_songs(user_prefs, songs, k=5, scoring_fn=score_song_mood_first)
    for rec in recommendations:
        song, score, reasons = rec
        print(f"{song['title']} - Score: {score:.2f}")
        for reason in reasons:
            print(f"  {reason}")
        print()

    print("\n--- Energy-Focused Mode ---")
    recommendations = recommend_songs(user_prefs, songs, k=5, scoring_fn=score_song_energy_focused)
    for rec in recommendations:
        song, score, reasons = rec
        print(f"{song['title']} - Score: {score:.2f}")
        for reason in reasons:
            print(f"  {reason}")
        print()


if __name__ == "__main__":
    main()
