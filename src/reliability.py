from typing import Dict, List

from .agent import AgenticStudyAgent
from .recommender import Recommender, Song, UserProfile


def check_recommendation_consistency(recommender: Recommender, user: UserProfile, runs: int = 5, top_k: int = 3) -> Dict[str, object]:
    history: List[tuple] = []
    for _ in range(runs):
        top_ids = tuple(song.id for song in recommender.recommend(user, k=top_k))
        history.append(top_ids)

    if not history:
        return {"stable_fraction": 0.0, "runs": runs, "top_ids": []}

    reference = history[0]
    stable_count = sum(1 for item in history if item == reference)
    return {
        "stable_fraction": stable_count / runs,
        "runs": runs,
        "reference_top_ids": reference,
        "history": history,
    }


def check_quiz_generation_consistency(agent: AgenticStudyAgent, query: str, runs: int = 5) -> Dict[str, object]:
    questions: List[str] = []
    for _ in range(runs):
        result = agent.run(query)
        questions.append(result["question"])

    stable = all(question == questions[0] for question in questions)
    return {
        "stable": stable,
        "runs": runs,
        "questions": questions,
    }


def evaluate_reliability(recommender: Recommender, user: UserProfile, agent: AgenticStudyAgent, query: str) -> Dict[str, object]:
    return {
        "recommendation_consistency": check_recommendation_consistency(recommender, user),
        "quiz_generation_consistency": check_quiz_generation_consistency(agent, query),
    }
