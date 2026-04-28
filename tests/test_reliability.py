from src.recommender import Recommender, Song, UserProfile
from src.reliability import check_recommendation_consistency


def make_test_recommender() -> Recommender:
    songs = [
        Song(id=1, title="A", artist="X", genre="pop", mood="happy", energy=0.8),
        Song(id=2, title="B", artist="Y", genre="pop", mood="chill", energy=0.7),
    ]
    return Recommender(songs)


def test_recommendation_consistency_returns_stable_fraction():
    recommender = make_test_recommender()
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    metrics = check_recommendation_consistency(recommender, user, runs=3, top_k=2)

    assert metrics["stable_fraction"] == 1.0
    assert metrics["runs"] == 3
    assert metrics["reference_top_ids"] == (1, 2)
